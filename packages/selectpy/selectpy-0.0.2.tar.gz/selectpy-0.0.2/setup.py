from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.2'
DESCRIPTION = 'A fully customizable selection menu for python'
LONG_DESCRIPTION = 'A simple python module to integrate a fully customizable select menu in your python projects.'

# Setting up
setup(
    name="selectpy",
    version=VERSION,
    author="Soham P",
    author_email="<sohxmp1204@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['rich', 'yakh'],
    setup_requires=['wheel'],
    keywords=['python', 'select', 'select menu', 'terminal menu', 'python menu', 'python select menu']
)