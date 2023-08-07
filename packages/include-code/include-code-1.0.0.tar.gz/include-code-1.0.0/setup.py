import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "include-code",
    version = "1.0.0",
    packages = ["include_code"],
    entry_points = {
        "console_scripts": ['include-code=include_code.include_code:main']
    },
    install_requires = [
        'urllib3<2.0', # To suppress the OpenSSL warning
        'requests',
        'panflute'
    ],
    author = "Kevin Della Schiava",
    author_email = "dellaschiavak@gmail.com",
    description = ("A pandoc filter to easily include remote code into markdown"),
    license = "BSD",
    keywords = "pandoc filter documentation",
    long_description=read('README.md'),
)
