from setuptools import setup, find_packages
from rave import __version__, __author__

with open("README.md", "r") as stream:
    long_description = stream.read()

setup(
    name=__name__,
    version=__version__,
    url="https://github.com/kyvio/rave.py",
    download_url="https://github.com/kyvio/rave.py/archive/refs/heads/main.zip",
    description="Unofficial Python wrapper for Rave API ✨.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=__author__,
    license="MIT",
    keywords=[
        "rave.py",
        "rave",
        "ravepy",
        "raveio",
        "rave.io",
        "api.red.wemesh.ca",
        "wemesh",
        "rave-api",
        "rave-wrapper",
        "bov",
        "bovo",
        "bovonos",
        "kyvio"

    ],
    include_package_data=True,
    install_requires=[
        "requests",
    ],
    setup_requires=["wheel"],
    packages=find_packages(),
)
