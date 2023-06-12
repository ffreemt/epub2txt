"""Convert epub to text."""
# pylint: disable=invalid-name, too-many-branches, too-many-statements, too-many-locals, broad-except, deprecated-class, line-too-long, c-extension-no-member

from pathlib import Path
from typing import Any, Callable, List, Union

try:
    from collections.abc import Iterable  # python 3.10+
except ImportError:
    from collections import Iterable  # python < 3.10

# the rest
# import io
import tempfile
from itertools import zip_longest

import ebooklib
import httpx
import logzero
from ebooklib import epub
from logzero import logger
from lxml import etree

parser = etree.HTMLParser()


def with_func_attrs(**attrs: Any) -> Callable:
    """Deco with_func_attrs."""

    def with_attrs(fct: Callable) -> Callable:
        for key, val in attrs.items():
            setattr(fct, key, val)
        return fct

    return with_attrs


def flatten_iter(items):
    """Yield items from any nested iterable; see Reference."""
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
            for sub_x in flatten_iter(x):
                yield sub_x
        else:
            yield x


def fillin_title(ilist):
    """Convert NA to chapter title*.

    ['NA', 'NA', 'a', 'NA', 'NA', 'b', 'NA', 'c', 'NA'] =>
    ['NA', 'NA', 'a', 'a*', 'a*', 'b', 'b*', 'c', 'NA']
    """
    lst = ilist[:]
    tf = [*map(lambda x: x != "NA", lst)]

    prev = None
    for i in range(tf.index(True), len(tf) - tf[::-1].index(True)):
        if lst[i] == "NA":
            lst[i] = prev
        else:
            prev = lst[i] + "*"
    return lst


# fmt: off
@with_func_attrs(title="", toc="", toc_titles="", toc_hrefs="", toc_uids="", spine="", metadata="")
def epub2txt(
        filepath: Union[str, Path],
        clean: bool = True,
        outputlist: bool = False,
        debug: bool = False,
) -> Union[str, List[str]]:
    # fmt: on
    """Convert epub to text.

    outputlist: if set to True, output List[str] according to book.spine
    clean: remove blank lines if set to True

    list of ebooklib.epub.EpuNav/ebooklib.epub.EpubHtml
    [book.get_item_with_id(elm) for elm in book.spine]
    """
    if debug:
        logzero.loglevel(10)
    else:
        logzero.loglevel(20)

    # process possible url
    if str(filepath).startswith("http"):
        try:
            resp = httpx.get(filepath, timeout=30, follow_redirects=True)
            resp.raise_for_status()
        except Exception as exc:
            logger.error("httpx.get(%s) exc: %s", filepath, exc)
            raise
        # cont = io.BytesIO(resp.content)
        with tempfile.NamedTemporaryFile(mode='w+b', delete=False) as tfile:
            try:
                tfile.write(resp.content)
            except Exception as exc:
                logger.error(exc)
                raise
            file_name = tfile.name

        try:
            book = epub.read_epub(file_name)
        except Exception as exc:
            logger.error("epub.read_epub(%s) exc: %s", file_name, exc)
            raise
    else:
        filepath = Path(filepath)
        try:
            book = epub.read_epub(filepath)
        except Exception as exc:
            logger.error("epub.read_epub(%s) exc: %s", filepath, exc)
            raise

    _ = [*flatten_iter(book.toc)]
    try:
        epub2txt.toc_titles = [elm.title for elm in _]
        # xhtml files associated with toc titles
        epub2txt.toc_hrefs = [elm.href for elm in _]
    except Exception as exc:
        logger.warning(" toc_title/toc_hrefs exc: %s", exc)

    try:
        epub2txt.toc_uids = [elm.uid for elm in _]
    except Exception as exc:
        logger.warning(" toc_uids exc: %s", exc)

    epub2txt.title = book.title
    epub2txt.toc = [*zip_longest(epub2txt.toc_titles, epub2txt.toc_hrefs, fillvalue="")]

    # list of things packed into epub
    epub2txt.spine = [elm[0] for elm in book.spine]

    # list of ebooklib.epub.EpuNav/ebooklib.epub.EpubHtml
    # [book.get_item_with_id(elm) for elm in epub2txt.spine]

    epub2txt.metadata = [*book.metadata.values()]

    # contents = [book.get_item_with_id(item[0]).content for item in book.spine]
    contents = [elm.content for elm in book.get_items_of_type(ebooklib.ITEM_DOCUMENT)]

    names = [elm.get_name() for elm in book.get_items_of_type(ebooklib.ITEM_DOCUMENT)]

    epub2txt.names = names

    # content/chapter titles
    # remove bookmark #: most toc_hrefs correspond to names
    # _ = [Path(elm).with_suffix('.xhtml').as_posix() for elm in epub2txt.toc_hrefs]
    _ = [elm.rsplit("#", 1)[0] for elm in epub2txt.toc_hrefs]
    name2title = dict(zip(_, epub2txt.toc_titles))

    _ = [name2title.get(name, "NA") for name in names]
    try:
        epub2txt.content_titles = fillin_title(_)
    except Exception:
        epub2txt.content_titles = _

    # texts = [pq(content).text() for content in contents]

    # Using XPath to find text
    # root = etree.XML(content)
    # tree = etree.ElementTree(root)
    # text = tree.xpath("string()")   # pq(content).text()

    texts = []
    for content in contents:
        # root = etree.XML(content)
        root = etree.XML(content, parser=parser)
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
