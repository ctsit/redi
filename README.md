# RED-I Project

![DOI](https://zenodo.org/badge/doi/10.5281/zenodo.10014.png ".")

CONTENTS OF THIS FILE
---------------------

 * [Introduction](#Introduction)
 * [How to Install RED-I](#How to Install RED-I)
 * [How to Test RED-I with a Sample Project](#How to Test RED-I with a Sample Project)
 * [How to Configure RED-I for a New Project](#How to Configure RED-I for a New Project)
 * [How to Contribute](#How to Contribute)

## Introduction

The REDCap Electronic Data Importer (RED-I) is a tool which is used to automate
the process of loading clinical data from Electronic Medical Records (EMR)
systems into [REDCap](http://www.project-redcap.org/) Study data capture systems.
RED-I is a general purpose tool for REDCap data importing suitable for use on
any study in any REDCap system. It uses XML lookups to translate data stored in
comma separated values (CSV) files and uploads it to a REDCAP Server using the
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

Please refer to [README-install](doc/README-install.md) for more help with
installation.

## How to Test RED-I with a Sample Project

Now that you installed the RED-I application you are probably wondering how
to configure it to help you with data translation and import tasks.
The good news is that you do not have to change any configuration file to test
RED-I -- we provide examples of working files for you:

 * [settings.ini](config-example/settings.ini)
 * [redi_sample_project_v5.7.4.sql](config-example/vagrant-data/redi_sample_project_v5.7.4.sql)
 * [Vagrantfile](vagrant/Vagrantfile)

These files make it very easy to see how RED-I imports data from a
[csv file](config-example/synthetic-lab-data.csv) into a local instance of REDCap.

Please refer to the [Testing RED-I with a sample REDCap Project](vagrant/README.md)
for more details on how to run RED-I against a locally-running virtual machine.

Note: You will need to obtain your own copy of the REDCap since
[the license terms](https://redcap.vanderbilt.edu/consortium/participate.php)
prevent us from including the code in an open source project.

## How to Configure RED-I for a New Project

To use RED-I in production you will have to edit the 'settings.ini' file
with values matching your environment.

Please refer to the [RED-I Configuration](doc/redi_configuration.md)
for more details about the meaning of each parameter in 'settings.ini' file.

Please refer to the [Add new REDCap Project and API Key](doc/add_new_redcap_project.md)
document for more details about new project setup.

Please refer to the [advanced usage guide](doc/redi_usage.md) for more details
about supported command line arguments.

## How to Contribute

 * Fork the source-code
 * Create a branch (`git checkout -b my_branch`)
 * Commit your changes (`git commit -am "Details about feature/bug fixes in the commit"`)
 * Push to the branch (`git push origin my_branch`)
 * Open a pull request and we will accept it as long as it passes through our
 [code review procedure](doc/code-review-checklist.md)
