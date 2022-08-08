import setuptools

required_packages = ["aiohttp",
                     "aiofiles"
                     ]


setuptools.setup(
    name="sms-activate-api",
    version="1.0",
    author="Rehman Ali",
    author_email="rehmanali.9442289@gmail.com",
    description="An async python wrapper for official sms-activate.org API.",
    url="https://github.com/rehmanali1337/sms-activate-api",
    packages=setuptools.find_packages(),
    install_requires=required_packages
)
