import os.path
from setuptools import setup

HERE = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(HERE, "README.md"), encoding="utf8") as fid:
    README = fid.read()

setup(
    name="warpcore",
    version="1.1.3",
    description="Streamlined multi-threaded process acceleration",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/BlackburnHax/warpcore",
    author="Brandon Blackburn",
    author_email="contact@bhax.net",
    license="Apache 2.0",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Natural Language :: English",
    ],
    packages=["warpcore"],
    include_package_data=True,
    install_requires=[],
)
