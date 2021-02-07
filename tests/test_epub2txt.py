"""Test # from epub2txt.epub2txt import __version__."""
from epub2txt import __version__


def test_version():
    assert __version__[:3] == "0.1.0"[:3]
