[![PyPI](https://img.shields.io/pypi/v/anonfiles_uploader)](https://pypi.org/project/anonfiles_uploader)
[![Downloads](https://static.pepy.tech/badge/anonfiles_uploader)](https://pypi.org/project/anonfiles_uploader)
[![Status](https://img.shields.io/pypi/status/anonfiles_uploader)](https://pypi.org/project/anonfiles_uploader)

# anonfiles_uploader
Easily upload files to anonfiles.

## Get started:

```
python -m pip install -U anonfiles_uploader
```

## Example:

```python
from anonfiles_uploader import upload 
from asyncio import run

files = ["file1.txt", "file2.txt"]
try:
    URLs = run(upload(files))
    for URL in URLs:
        print(URL)
except Exception as e:
    print(e)
```
