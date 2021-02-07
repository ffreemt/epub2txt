# epub2txt [![Codacy Badge](https://app.codacy.com/project/badge/Grade/0bef74fe4381412ab1172a06a93ad01e)](https://www.codacy.com/gh/ffreemt/epub2txt/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ffreemt/epub2txt&amp;utm_campaign=Badge_Grade)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

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

```python
from epub2txt import epub2txt

# from a url to epub
url = "https://github.com/ffreemt/tmx2epub/raw/master/tests/1.tmx.epub"
res = epub2txt(url)

# from a local epub file
filepath = r"tests\test.epub"
res = epub2txt(filepath)

```