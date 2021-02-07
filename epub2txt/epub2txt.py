"""Convert epub to text."""
# pylint:

from typing import List, Union

from pathlib import Path
import httpx
import io
from lxml import etree
from ebooklib import epub

from logzero import logger


def epub2txt(
    filepath: Union[str, Path], clean: bool = True, outputlist: bool = False,
) -> Union[str, List[str]]:
    """Convert epub to text.

    spine: if set to True, output List[str] according to book.spine
    clean: remove blank lines if set to True
    """

    # process possible url

    if filepath.__str__().startswith("http"):
        try:
            resp = httpx.get(filepath, timeout=30)
            resp.raise_for_status()
        except Exception as exc:
            logger.error("httpx.get(%s) exc: %s", filepath, exc)
            raise
        cont = io.BytesIO(resp.content)

        try:
            book = epub.read_epub(cont)
        except Exception as exc:
            logger.error("epub.read_epub(cont) exc: %s", exc)
            raise
    else:
        filepath = Path(filepath)
        try:
            book = epub.read_epub(filepath)
        except Exception as exc:
            logger.error("epub.read_epub(%s) exc: %s", filepath, exc)
            raise

    contents = [book.get_item_with_id(item[0]).content for item in book.spine]
    # texts = [pq(content).text() for content in contents]

    # Using XPath to find text
    # root = etree.XML(content)
    # tree = etree.ElementTree(root)
    # text = tree.xpath("string()")   # pq(content).text()

    texts = []
    for content in contents:
        root = etree.XML(content)
        tree = etree.ElementTree(root)
        text = tree.xpath("string()")
        texts.append(text)

    if clean:
        temp = []
        for text in texts:
            _ = [elm.strip() for elm in text.splitlines() if elm.strip()]
            temp.append("\n".join(_))
        texts = temp

    if outputlist:
        return texts

    return "\n".join(texts)
