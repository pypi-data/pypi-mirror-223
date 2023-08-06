from pathlib import Path

from setuptools import setup, find_packages

setup(
    name="telebirrTxChecker",
    version="0.0.4",
    packages=find_packages(),
    url="https://github.com/wizkiye/TelebirrPaymentProcessor",
    license="MIT",
    author="Kidus",
    author_email="wizkiye@gmail.com",
    description="asynchronous telebirr transaction checker",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    install_requires=["httpx", "bs4", "lxml"],
)
