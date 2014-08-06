from setuptools import setup, find_packages

INSTALL_REQUIRES = [
    "requests >= 2.2.1",
    "lxml >= 3.3.5",
]

setup(
    name='REDI',
    version='0.9.1',
    author='Christopher P Barnes, Philip Chase, Nicholas Rejack',
    author_email='cpb@ufl.edu, pbc@ufl.edu, nrejack@ufl.edu',
    packages=find_packages(exclude=['test']),
    include_package_data=True,
    package_data = {
        'bin'   : ['utils/*.xsl', 'utils/*.xsd'],
        'redi'  : ['README.md'],
    },
    url='http://it.ctsi.ufl.edu/about/',
    license='BSD 3-Clause',
    description='REDCap Electronic Data Importer',
    long_description=open('README.md').read(),
    install_requires=INSTALL_REQUIRES,
    entry_points={
            'console_scripts': [
                'redi = bin.redi:main',
                ],
            },
    test_suite='test.TestSuite',
    tests_require=[] + INSTALL_REQUIRES,
)
