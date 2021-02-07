"""Test local file."""
from epub2txt.epub2txt import epub2txt


def test_epbu2txt_local():
    filepath = "tests/test.epub"

    res = epub2txt(filepath)
    assert len(res) > 200

    res = epub2txt(filepath, clean=False)
    assert len(res) > 500

    res = epub2txt(filepath, outputlist=True)
    assert len(res) == 4

    res = epub2txt(filepath, outputlist=True, clean=False)
    assert len(res) == 4
