# RED-I Project 

![DOI](https://zenodo.org/badge/doi/10.5281/zenodo.10014.png ".")

The REDCap Electronic Data Importer (RED-I) is a tool to automate the process of loading clinical data from EMRs into REDCap Study data capture systems. RED-I is a general purpose tool for REDCap data importing suitable for use on any study in any REDCap system. It uses XML lookups to translate csv into REDCap format eav. The tool allows study data to be securely uploaded from clinical reporting systems, error checked, and uploaded into REDCap.  It provides the investigator with feedback on upload success in the form of summary reporting of the data upload process.  

## Directory layout 
	
    redi : This is the common repository for RED-I. This repository contains generic artifacts
    ├── CHANGELOG - log of changes to the REDI project
    ├── bin  : This folder consists of all the python modules for this repo
    ├── config-example  : This folder will consist of the configuration files specific to this repo
    ├── doc  : This folder contains the documentation such as installation instructions, process flow specific to this repo
    ├── log  : This folder has the log files that are generated during the run
    └── test  : This folder has the test modules and test suite for this repo

Installation
-----------

    git clone <repository_access_url> <your_project_name>
    cd <your_project_name>
    cp config-example config

Adapt the example config folder to your needs.

Reference doc/README-install.md for more installation details.
Configuration docs have not yet been written.


Usage
-----

    $python <project_root_path>/bin/redi.py

Testing
-------

To run the tests:

    $ python <project_root_path>/test/TestSuite.py


Contributing
------------

1. Fork it.
2. Create a branch (`git checkout -b my_branch`)
3. Commit your changes (`git commit -am "Add blah blah blah"`)
4. Push to the branch (`git push origin my_branch`)
5. Open a pull request
6. Enjoy a refreshing Diet Coke (diet only) and wait
