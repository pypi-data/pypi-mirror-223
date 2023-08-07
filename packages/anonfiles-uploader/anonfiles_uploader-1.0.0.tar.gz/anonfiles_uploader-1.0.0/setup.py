from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    README = f.read()

setup(
    name="anonfiles_uploader",
    version="1.0.0",
    description="Easily upload files to anonfiles.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Ruu3f/anonfiles_uploader",
    author="Ruu3f",
    license="GPLv2",
    keywords=[
        "anonfiles",
        "file-upload",
        "file-hosting",
        "api-wrapper",
        "anonymous-file-upload",
        "anonymous-file-hosting",
    ],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    install_requires=[
        "aiohttp",
    ],
    project_urls={
        "Source": "https://github.com/Ruu3f/anonfiles_uploader",
    },
)
