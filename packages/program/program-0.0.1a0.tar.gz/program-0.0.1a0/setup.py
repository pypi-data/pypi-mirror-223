import os
import re
import codecs
from setuptools import setup, find_packages

def find_version(*file_path):
    '''Read in the version from the package'''

    # get the file contents
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, *file_path), "r") as fp:
        version_file = fp.read()

    # extract the version string
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name="program",
    version=find_version("code", "__init__.py"),
    url="https://github.com/slundberg/code",
    author="Scott Lundberg",
    author_email="scott@scottlundberg.com",
    description="A new way to code.",
    long_description=".",
    packages=find_packages(exclude=["notebooks", "client"]),
    package_data={"code": ["resources/*"]},
    install_requires=[
        "numpy",
    ],
    extras_require={
        'docs': [
            'ipython',
            'numpydoc',
            'sphinx_rtd_theme',
            'sphinx',
            'nbsphinx'
        ],
        'test': [
            'pytest',
            'pytest-cov'
        ]
    }
)
