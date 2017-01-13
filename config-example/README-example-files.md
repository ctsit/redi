# Example Configuration Files

The example configuration files provide here will allow you to execute a test run of data being pushed into a sample REDCap project.To use these files, you will need access to a running REDCap server with the appropriate example project, and an API Token for that project which will allow RED-I access to write to the sample project.

## Getting REDCap

Research Electronic Data Capture (REDCap) is a software package written and distributed by Vanderbilt University.  If you do not already have a access to a REDCap system see http://project-redcap.org/ for details on how to become a consortium partner.

Your institution may already provide you with access to REDCap.  If so you can use that access to create a test project.  With that, some assistance from your technical staff, and a few edits of the example files, you can test REDI.

REDI also includes the ability to create a REDCap server inside a virtual machine running on your own computer.  For more details on that option see ../vagrant/README.md.


## Getting the Right REDCap Project to use these files

This example configuration is based on one of the default REDCap example projects. This project is identified as "Longitudinal Database (1 arm)" in the REDCap template library. In a fresh REDCap installation, (like you will find in a test virtual machine), the project named "Example Database (Longitudinal)" has already been created for you in this template.

## File Descriptions

### settings.ini:

This file contains settings necessary to run RED-I. It contains detailed descriptions of the fields which need to be set before running RED-I.

### research_id_to_redcap_id_map.xml:

This file contains mappings of primary keys of your REDCap system and your custom project. This file is used by RED-I at runtime to map your incoming project's specific IDs to that of the REDCap's IDs.

### translationTable.xml:

This file maps your project specific component id's with REDCap Fields. Change this file to map your project specific component IDs to REDCap Fields.

### formEvents.xml:

This file contains details of the form, events and fields which are updated by running RED-I. If you have any forms to be updated, please add them in this file before running RED-I.

### report.xsl:

This file is used for formatting the final RED-I run report, which is sent to the receiver_email set in the settings.ini

### clinical-component-to-loinc-example.xml:

This file maps your project specific component id's to standard LOINC codes. For every new form added to formEvents.xml make sure that component id's of fields in that form are mapped to standard LOINC codes in this file.

### synthetic-lab-data.csv:

synthetic-lab-data.csv is a sample RED-I input data file.  It is entirely synthetic data created with the R script, makefakedata.

### synthetic-lab-data.xml:

synthetic-lab-data.xml is a sample RED-I input data file.  It is made by processing synthetic-lab-data.csv through some sed filters and csv2xml.py

### enrollment_test_data.csv

enrollment_test_data.csv is a file of enrollment data that must be loaded into the sample REDCap project before RED-I can load data into the project.

### vagrant-data/redi_sample_project_v5.7.4.sql

`vagrant-data/redi_sample_project_v5.7.4.sql` is an SQL dump of our sample project for version 5.7.4 of REDCap. This can be loaded into the MySQL instance running inside the Vagrant Virtual Machine.
