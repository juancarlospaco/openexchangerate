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


"""Generic Setup.py.
ALL THE CONFIG LIVES IN SETUP.CFG,PLEASE EDIT THERE,KEEP IT SIMPLE AND CLEAN."""


import atexit

from setuptools import setup


##############################################################################
# EDIT HERE


MODULES2CYTHONIZE = ("openexchangerate.py", )


##############################################################################
# Dont touch below


def post_install_cythonize():
    """Compile *.PY to *.SO with Cython,delete *.PYC,*.C,*.PY if sucessful."""
    import sys
    import os
    from pathlib import Path
    from shutil import which, rmtree
    from subprocess import run
    try:
        from site import getsitepackages
        site_packages = getsitepackages()[0]
    except (ImportError, Exception):
        from distutils.sysconfig import get_python_lib
        site_packages = get_python_lib()
    gcc, cythoniz = which("gcc"), which("cythonize")
    if gcc and cythoniz and site_packages and sys.platform.startswith("linux"):
        for py_file in [(Path(site_packages) / f) for f in MODULES2CYTHONIZE]:
            if py_file.is_file() and os.access(py_file, os.W_OK):
                comand = f"{cythoniz} -3 --inplace --force {py_file}"
                try:
                    run(comand, shell=True, timeout=99, check=True)
                except Exception as error:
                    print(error)
                else:
                    print(f"CREATED Binary file: {py_file.with_suffix('.so')}")
                    if py_file.with_suffix(".c").is_file():
                        py_file.with_suffix(".c").unlink()  # is C Obfuscated.
                    if py_file.is_file():
                        print(f"DELETED unused file: {py_file}")
                        py_file.unlink()  # Because *.SO exist and is faster.
                rmtree(py_file.parent / "__pycache__", ignore_errors=True)
    else:
        print("GCC & Cython not found, install GCC & Cython for Speed up.")


atexit.register(post_install_cythonize)


setup(py_modules=["openexchangerate"])
