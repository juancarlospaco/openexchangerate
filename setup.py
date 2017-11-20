#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#
# To generate DEB package from Python Package:
# sudo pip3 install stdeb
# python3 setup.py --verbose --command-packages=stdeb.command bdist_deb
#
#
# To generate RPM package from Python Package:
# sudo apt-get install rpm
# python3 setup.py bdist_rpm --verbose --fix-python --binary-only
#
#
# To generate EXE MS Windows from Python Package (from MS Windows only):
# python3 setup.py bdist_wininst --verbose
#
#
# To generate PKGBUILD ArchLinux from Python Package (from PyPI only):
# sudo pip3 install git+https://github.com/bluepeppers/pip2arch.git
# pip2arch.py PackageNameHere
#
#
# To Upload to PyPI by executing:
# sudo pip install --upgrade pip setuptools wheel virtualenv
# python3 setup.py bdist_egg bdist_wheel --universal sdist --formats=zip upload --sign


"""Setup.py for Python, as Generic as possible."""


import os
import re

from setuptools import setup


##############################################################################
# EDIT HERE


MODULE_PATH = os.path.join(os.path.dirname(__file__), "openexchangerate.py")
DESCRIPTION = """OpenExchangeRates API client for Python 3.7+,
worldwide exchange prices + Bitcoin price,
can calculate base price locally offline with free api key,
can be used as context manager or iterator, namedtuple and dict outputs."""


##############################################################################
# Dont touch below


try:
    with open(str(MODULE_PATH), "r", encoding="utf-8-sig") as source_code_file:
        SOURCE = source_code_file.read()
except Exception:
    with open(str(MODULE_PATH),  "r") as source_code_file:
        SOURCE = source_code_file.read()


def find_this(search, source=SOURCE):
    """Take a string and a filename path string and return the found value."""
    print("Searching for {what}.".format(what=search))
    if not search or not source:
        print("Not found on source: {what}.".format(what=search))
        return ""
    return str(re.compile(r'.*__{what}__ = "(.*?)"'.format(
        what=search), re.S).match(source).group(1)).strip()


print("Starting build of setuptools.setup().")


##############################################################################
# EDIT HERE


setup(

    name="openexchangerate",
    version=find_this("version"),

    description="OpenExchangeRates API client for Python 3.7+.",
    long_description=DESCRIPTION,

    url=find_this("url"),
    license=find_this("license"),

    author=find_this("author"),
    author_email=find_this("email"),
    maintainer=find_this("maintainer"),
    maintainer_email=find_this("email"),

    include_package_data=True,
    zip_safe=True,

    tests_require=['isort', 'prospector', 'pre-commit', 'pre-commit-hooks'],
    python_requires='>=3.6',

    py_modules=["openexchangerate"],

    keywords="bitcoin price exchange_prices openexchangerates minimalism",

    classifiers=[

        'Development Status :: 5 - Production/Stable',

        'Environment :: Console',
        'Environment :: X11 Applications',
        'Environment :: No Input/Output (Daemon)',
        'Environment :: Other Environment',

        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Other Audience',

        'Natural Language :: English',

        'License :: OSI Approved :: GNU General Public License (GPL)',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',

        'Operating System :: OS Independent',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',

        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',

        'Programming Language :: Python :: Implementation :: CPython',

        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',

    ],
)


print("Finished build of setuptools.setup().")
