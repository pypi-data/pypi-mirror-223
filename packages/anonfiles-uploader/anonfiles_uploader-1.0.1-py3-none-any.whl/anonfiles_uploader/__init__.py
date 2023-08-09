__author__ = "Ruu3f"
__version__ = "1.0.1"

from os.path import isfile
from aiohttp import ClientSession, FormData, ClientError


async def upload(files):
    """Upload files to anonfiles API and return the short URLs for the uploaded files."""
    async with ClientSession() as session:
        URLs = []
        for file in files:
            if isfile(file):
                with open(file, "rb") as fp:
                    filedata = fp.read()

                data = FormData()
                data.add_field("file", filedata, filename=file)
                try:
                    async with session.post(
                        "https://api.anonfiles.com/upload", data=data, timeout=160
                    ) as resp:
                        resp_json = await resp.json()
                except ClientError as exc:
                    raise Exception("Unable to fetch the response.") from exc
                URLs.append(resp_json["data"]["file"]["url"]["short"])
            else:
                raise FileNotFoundError(f"File not found: {file}")
        return URLs
