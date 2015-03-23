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
    version='0.13.2',
    author='https://www.ctsi.ufl.edu/research/study-development/informatics-consulting/',
    author_email='ctsit@ctsi.ufl.edu',
    packages=find_packages(exclude=['test']),
    include_package_data=True,
    package_data={
        'redi': ['utils/*.xsl', 'utils/*.xsd']
    },
    url='https://github.com/ctsit/redi',
    download_url = 'https://github.com/ctsit/redi/releases/tag/0.13.1',
    keywords = ['EMR', 'EHR', 'REDCap', 'Clinical Data'],
    license='BSD 3-Clause',
    description='REDCap Electronic Data Importer',
    long_description=open('README.md').read(),
    install_requires=[
        "requests >= 2.2.1",
        "lxml >= 3.3.5",
        "PyCap >= 1.0",
        "pysftp >= 0.2.8",
        "docopt >= 0.6.2",
    ],
    entry_points={
        'console_scripts': [
            'redi = redi.redi:main',
        ],
    },
    test_suite='test.TestSuite',
    tests_require=[
        "mock >= 1.0",
        "sftpserver >= 0.2",
    ],
    setup_requires=[
        "nose >= 1.0",
        "nosexcover >= 1.0.10",
    ],
)
