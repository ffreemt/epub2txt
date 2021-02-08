# epub2txt [![Codacy Badge](https://app.codacy.com/project/badge/Grade/05c422da73a14c23b87b0657af9c8df7)](https://www.codacy.com/gh/ffreemt/epub2txt/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ffreemt/epub2txt&amp;utm_campaign=Badge_Grade)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/epub2txt.svg)](https://badge.fury.io/py/epub2txt)

Convert epub to txt with additonal utils

<!--- Refer to dualtext-epub\der_fanger_de_en.py
		__main__.py refer to tmx2epub.__main__
--->

## Installation

```bash
pip install epub2txt
# pip install epub2txt -U  # to upgrade
```

## Usage

### From command line

```bash
# convert test.epub to test.txt
epub2txt -f test.epub

# browse for epub file, txt file will be in the same directory as the epub file
epub2txt

# show epub book info: title and toc
epub2txt -i

# show more epub book info: title, toc, metadata, spine (list of stuff packed into the epub)
epub2txt -i

# show epub2txt version

```

### `python` code

```python
from epub2txt import epub2txt
# from a url to epub
url = "https://github.com/ffreemt/tmx2epub/raw/master/tests/1.tmx.epub"
res = epub2txt(url)

# from a local epub file
filepath = r"tests\test.epub"
res = epub2txt(filepath)

```

## TODO
*   Extract a single chapter
