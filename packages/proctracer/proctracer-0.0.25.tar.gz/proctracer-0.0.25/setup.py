"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import find_packages, setup

import os
import re
from os import path


# The tests utils are used by conan-package-tools
here = path.abspath(path.dirname(__file__))
excluded_test_packages = ["proctracer.test.{}*".format(d)
                         for d in os.listdir(os.path.join(here, "proctracer/test"))
                         if os.path.isdir(os.path.join(here, "proctracer/test", d)) and d != "utils"]


def get_requires(filename):
    requirements = []
    with open(filename, "rt") as req_file:
        for line in req_file.read().splitlines():
            if not line.strip().startswith("#"):
                requirements.append(line)
    return requirements


def load_version():
    """ Loads a file content """
    filename = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                            "proctracer", "__init__.py"))
    with open(filename, "rt") as version_file:
        conan_init = version_file.read()
        version = re.search(r"__version__ = '([0-9a-z.-]+)'", conan_init).group(1)
        return version


def generate_long_description_file():
    this_directory = path.abspath(path.dirname(__file__))
    with open(path.join(this_directory, 'README.md')) as f:
        long_description = f.read()
    return long_description


project_requirements = get_requires("proctracer/requirements.txt")
#dev_requirements = get_requires("proctracer/requirements_dev.txt")
excluded_packages = []
exclude = excluded_test_packages + excluded_packages


setup(
    name='proctracer',
    python_requires='>=3.6',
    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=load_version(),  # + ".rc1",

    description='/proc Tracer',
    long_description=generate_long_description_file(),
    long_description_content_type='text/markdown',

    # The project's main homepage.
    url='https://github.com/david-kracht/proctracer',
    project_urls={
        'Documentation': 'https://github.com/david-kracht/proctracer',
        'Source': 'https://github.com/david-kracht/proctracer.git',
        'Tracker': 'https://github.com/david-kracht/proctracer/issues',
    },

    # Author details
    author='David Kracht',
    author_email='dave.kracht@gmail.com',

    # Choose your license
    license='BSD-3',
    license_files = ('LICENSE.md',), 

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],

    # What does your project relate to?
    keywords=['package', 'proc ', 'trace'],

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=exclude),

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=project_requirements,

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        #'dev': dev_requirements,
        #'test': dev_requirements,
    },

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={
        'proctracer': ['*.txt'],
    },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    # data_files=[('my_data', ['data/data_file'])],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'proctracer=proctracer.proctracer:main',
        ],
    },
)
