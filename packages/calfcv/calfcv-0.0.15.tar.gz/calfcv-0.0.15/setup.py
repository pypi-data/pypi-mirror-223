#! /usr/bin/env python
""" The calfcv package setup file.

Remove the old distribution from the calfcv directory
0. rm -r dist

To build and upload a new distribution
1.  Update the version

2. cd to calfcv and build the dist folder with
python setup.py sdist bdist_wheel

3. twine upload dist/*

"""

import codecs

from setuptools import find_packages, setup

from calfcv import _version

DISTNAME = 'calfcv'
DESCRIPTION = 'Coarse approximation linear function with cross validation'
with codecs.open('README.rst', encoding='utf-8-sig') as f:
    LONG_DESCRIPTION = f.read()
MAINTAINER = 'Carlson Research, LLC'
MAINTAINER_EMAIL = 'hrolfrc@gmail.com'
URL = 'https://github.com/hrolfrc/calfcv'
LICENSE = 'new BSD'
DOWNLOAD_URL = 'https://github.com/hrolfrc/calfcv'
VERSION = _version.__version__
INSTALL_REQUIRES = ['numpy', 'scipy', 'scikit-learn']
CLASSIFIERS = ['Intended Audience :: Science/Research',
               'Intended Audience :: Developers',
               'Topic :: Scientific/Engineering :: Artificial Intelligence',
               'Topic :: Scientific/Engineering :: Mathematics',
               'Development Status :: 2 - Pre-Alpha',
               'License :: OSI Approved',
               'Operating System :: OS Independent',
               'Programming Language :: Python :: 3']
EXTRAS_REQUIRE = {
    'tests': [
        'pytest',
        'pytest-cov'],
    'docs': [
        'sphinx',
        'sphinx-gallery',
        'sphinx_rtd_theme',
        'numpydoc',
        'matplotlib'
    ]
}

setup(name=DISTNAME,
      maintainer=MAINTAINER,
      maintainer_email=MAINTAINER_EMAIL,
      description=DESCRIPTION,
      license=LICENSE,
      url=URL,
      version=VERSION,
      download_url=DOWNLOAD_URL,
      long_description=LONG_DESCRIPTION,
      zip_safe=False,  # the package can run out of an .egg file
      classifiers=CLASSIFIERS,
      packages=find_packages(),
      install_requires=INSTALL_REQUIRES,
      extras_require=EXTRAS_REQUIRE)
