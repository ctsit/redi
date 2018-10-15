"""
RED-I Setup

Please read the documentation in README.md!

Quick install:

    $ make egg
    $ sudo easy_install dist/REDI*.egg

Prerequisites on Debian Wheezy:

  apt-get install python-setuptools python-dev libxml2 libxslt1-dev

"""

from setuptools import setup, find_packages

setup(
    name='redi',
    use_scm_version=True,
    author='CTS-IT at the University of Florida',
    author_email='ctsit@ctsi.ufl.edu',
    packages=find_packages(exclude=['test']),
    include_package_data=True,
    package_data={
        'redi': ['utils/*.xsl', 'utils/*.xsd']
    },
    url='https://github.com/ctsit/redi',
    download_url = 'https://github.com/ctsit/redi/releases/tag/0.15.5',
    keywords = ['EMR', 'EHR', 'REDCap', 'Clinical Data'],
    license='BSD 3-Clause',
    description='REDCap Electronic Data Importer',
    long_description=open('README.md').read(),
    install_requires=[
        "requests >= 2.5.1",
        "lxml >= 3.3.5",
        "PyCap >= 1.0",
        "pysftp >= 0.2.8",
        "docopt >= 0.6.2",
        "pycrypto >= 2.6.1",
        "redcap_cli >= 0.1.0",
        "setuptools_scm >= 1.10.1"
    ],
    entry_points={
        'console_scripts': [
            'redi = redi.redi:main',
        ],
    },
    test_suite='test.TestSuite',
    tests_require=[
        "mock >= 1.0.1",
        "sftpserver >= 0.2",
    ],
    setup_requires=[
        "nose >= 1.0",
        "nosexcover >= 1.0.10",
        "setuptools_scm >= 1.10.1"
    ],
)
