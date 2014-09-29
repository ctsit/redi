# RED-I Project

![DOI](https://zenodo.org/badge/doi/10.5281/zenodo.10014.png ".")

CONTENTS OF THIS FILE
---------------------

 * [Introduction](##Introduction)
 * [How to Install RED-I](##How to Install RED-I)
 * [How to Test RED-I with a Sample Project]()
 * [How to Configure RED-I for a New Project]()
 * [How to Contribute]()

## Introduction

The REDCap Electronic Data Importer (RED-I) is a tool to automate the process
of loading clinical data from Electronic Medical Records (EMRs) into
[REDCap](http://www.project-redcap.org/) Study data capture systems. RED-I is
a general purpose tool for REDCap data importing suitable for use on any study
in any REDCap system. It uses XML lookups to translate data stored in comma
separated values (CSV) files and uploads it to a REDCAP Server using the
REDCap API. The tool allows study data to be securely uploaded from clinical
reporting systems, error checked, and uploaded into REDCap. It provides the
investigator with feedback on upload success in the form of summary reporting
of the data upload process.


## How to Install RED-I

From source:

    $ git clone https://github.com/ctsit/redi.git redi
    $ cd redi
    $ make
    $ make install

Reference [README-install](doc/README-install.md) for more installation details.

## How to Test RED-I with a Sample Project


## How to Configure RED-I for a New Project

To use RED-I in production you will have to edit the 'settings.ini' file
with values matching your environment.

## How to Contribute

 * Fork the source-code
 * Create a branch (`git checkout -b my_branch`)
 * Commit your changes (`git commit -am "Details about feature/bug fixes in the commit"`)
 * Push to the branch (`git push origin my_branch`)
 * Open a pull request
