from setuptools import setup, find_packages
from sms_activate_api._metadata import __version__

required_packages = ["aiohttp", "aiofiles"]


setup(
    name="sms-activate-api",
    version=__version__,
    author="Rehman Ali",
    author_email="rehmanali.9442289@gmail.com",
    description="An async python wrapper for official sms-activate.org API.",
    url="https://github.com/rehmanali1337/sms-activate-api",
    packages=find_packages(),
    install_requires=required_packages,
)
