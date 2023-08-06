from setuptools import setup, find_packages
import codecs
import os

VERSION="0.0.2"
DESCRIPTION="A python module which has a function validate(), which validates the terraform files in a particular directory"

setup(
    name="t_val",
    version=VERSION,
    author="M Vidyaa Shankar",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[]
)