from distutils.core import setup

setup(
    name='REDI',
    version='0.9.1-hcv-open-source',
    author='Christopher P Barnes, Philip Chase, Nicholas Rejack',
    author_email='cpb@ufl.edu, pbc@ufl.edu, nrejack@ufl.edu',
    packages=['bin/'],
    scripts=['bin/redi.py'],
    url='',
    license='LICENSE',
    description='REDCap Electronic Data Importer',
    long_description=open('README.md').read(),
    install_requires=[
        "requests >= 2.2.1",
        "lxml >= 3.2.4",
    ],
)
