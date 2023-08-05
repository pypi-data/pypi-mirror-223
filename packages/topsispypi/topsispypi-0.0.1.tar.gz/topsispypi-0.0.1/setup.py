from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'A Topsis Package'

# Setting up
setup(
    name="topsispypi",
    version=VERSION,
    author="Tanishq Singla",
    author_email="<tanishqsingla08@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=["numpy", "pandas", "sys"],
    keywords=['python', 'video', 'stream', 'video stream', 'camera stream', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)