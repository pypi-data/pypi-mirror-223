# anonfiles_uploader
Easily upload files to anonfiles.

## Get started:

```
python -m pip install -U anonfiles_uploader
```

## Example:

```python
import anonfiles_uploader
from asyncio import run

files = ["file1.txt", "file2.txt"]
try:
    URLs = run(anonfiles_uploader.upload(files))
    for URL in URLs:
        print(URL)
except Exception as e:
    print(e)
```
