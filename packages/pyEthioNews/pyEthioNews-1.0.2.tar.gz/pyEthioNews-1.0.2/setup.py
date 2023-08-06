from setuptools import setup, find_packages


def read(fname):
    with open(fname) as f:
        return f.read()


setup(
    name="pyEthioNews",
    version="1.0.2",
    url="https://github.com/wizkiye/pyEthioNewsApi",
    license="MIT",
    author="https://github.com/wizkiye",
    author_email="wizkiye@gmail.com",
    description="Ethiopian News Scraper",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    install_requires=[
        "httpx",
        "bs4",
    ],
    packages=find_packages(),
)
