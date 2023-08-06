#!/usr/bin/python3
# -*- coding:Utf-8 -*-

import setuptools

# from distutils import util

with open("../README.pypi.rst", "r") as fh:
    long_description = fh.read()

VERSION = "0.3"
DESCRIPTION = "Read, create and update Scribus .sla files."

REQUIRED = ['lxml', 'svg.path']

# pyscribus_path = util.convert_path('pyscribus')
# subp_file = util.convert_path('pyscribus/file')
# subp_model = util.convert_path('pyscribus/model')

setuptools.setup(
    name="pyscribus",
    version=VERSION,
    author="Étienne Nadji",
    author_email="etnadji@eml.cc",
    description=DESCRIPTION,
    long_description=long_description,

    packages=setuptools.find_packages(),

    # package_dir={'':'source/pyscribus'},
    # packages=setuptools.find_packages("source", include=["pyscribus"]),

    # package_dir={
        # 'pyscribus': pyscribus_path,
        # 'pyscribus.file': subp_file,
        # 'pyscribus.model': subp_model,
    # },
    # packages=['pyscribus', 'pyscribus.file', 'pyscribus.model'],

    # packages=setuptools.find_packages("pyscribus"),

    # package_dir={"":".", "pyscribus.model": "pyscribus/model", "pyscribus.file": "pyscribus/file"},

    # package_dir={"":"."},
    # packages=setuptools.find_packages(),

    platforms='any',
    license="GNU Affero General Public License v3 or later (AGPLv3+)",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Text Processing :: Markup :: XML",
        "Intended Audience :: Developers"
    ],
    project_urls={
        "Documentation": "https://etnadji.fr/pyscribus",
        "Source Code": "https://framagit.org/etnadji/pyscribus",
        "Issue tracker": "https://framagit.org/etnadji/pyscribus/-/issues"
    },
    python_requires='>=3.8',
    install_requires=REQUIRED,
    keywords=["scribus", "sla"],
)

# vim:set shiftwidth=4 softtabstop=4 spl=en:
