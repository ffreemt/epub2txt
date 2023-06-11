"""Test http."""
# from epub2txt.epub2txt import epub2txt
from epub2txt import epub2txt


def test_epub2txt_http():
    """Test epub2txt_http."""
    # url = "https://github.com/ffreemt/tmx2epub/raw/master/tests/1.tmx.epub"
    url = "https://github.com/ffreemt/epub2txt/raw/master/tests/1.tmx.epub"

    res = epub2txt(url)
    assert len(res) > 220000

    res = epub2txt(url, clean=False)
    assert len(res) > 280000

    res = epub2txt(url, outputlist=True)
    assert len(res) == 3
