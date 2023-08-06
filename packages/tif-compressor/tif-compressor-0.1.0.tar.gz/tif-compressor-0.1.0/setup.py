'''
Copyright 1999 Illinois Institute of Technology

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL ILLINOIS INSTITUTE OF TECHNOLOGY BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Except as contained in this notice, the name of Illinois Institute
of Technology shall not be used in advertising or otherwise to promote
the sale, use or other dealings in this Software without prior written
authorization from Illinois Institute of Technology.
'''

## Setup file to compile the sources and install the package on your system
# ==========================================
from distutils.core import setup
from setuptools import find_packages
from tif_compressor import __version__
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy, sys

# Build the main package, with script etc...
# ==========================================
setup(
    name = 'tif-compressor',
    packages = find_packages(),
    version = __version__,
    description = 'TIFF Compressor-Decompressor',
    author = 'BioCAT',
    author_email = 'biocat@lethocerus.biol.iit.edu',
    url = 'https://github.com/biocatiit',
    keywords = ['tiff', 'lzw', 'compressor', 'decompressor', 'biocat'],
    classifiers = ['Development Status :: 3 - Alpha',
                   'Environment :: X11 Applications :: Qt',
                   'Intended Audience :: Science/Research',
                   'Natural Language :: English',
                   'Operating System :: Other OS',
                   'Programming Language :: Python',
                   'Programming Language :: Cython',
                   'Topic :: Scientific/Engineering :: Bio-Informatics'],
    install_requires=['numpy',
                      'fabio',
                      'pillow',
                      'h5py',
                      'Cython'],
    entry_points={
        'console_scripts': [
            'tif-compressor=tif_compressor.main:main',
        ],
    },
    cmdclass = {'build_ext': build_ext},
    include_dirs=[numpy.get_include()],
    include_package_data=True
)

