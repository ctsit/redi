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

    Optional command line arguments:

    1. -c : To specify the path to config folder.

            E.g.: $python <project_root_path>/bin/redi.py -c /Users/admin/redi-config

            Default path for config folder is <project_root_path>/config

    2. -k : To keep the output files generated during data processing.

            E.g.: $python <project_root_path>/bin/redi.py -k yes

            When this parameter is provided, the output files are stored in <project_root_path>/out/out_<timestamp>.
            The timestamp has the format: YYYY_MM_DD-HH_MM_SS
            If the parameter is not provided, the output files are stored in a temporary folder during the execution of redi.py and then deleted along with the temporary folder once redi.py finishes execution.

    3. -d : To execute redi.py in dry run state.

            E.g.: $python <project_root_path>/bin/redi.py -d

            When this parameter is provided, all data transformations are performed and execution stops after writing out the final data set to <project_root_path>/out/out_<timestamp>.
            The purpose of this switch is to assist developers in performing a dry run of redi.py without involving the REDCap server and sending of email.
            If -d is used then we do not need to use -k in addition to it or provide any path for storing the output files.
            By default, this parameter is disabled.

    4. -e : To run the script for fetching EMR data.

            E.g.: $python <project_root_path>/bin/redi.py -e yes

            When this parameter us provided, a connection will be established with the sftp server mentioned in the settings.ini file in the config folder and EMR data required for the execution of redi.py will be downloaded.
            Following parameters need to be set in config/settings.ini before using this option:
            - emr_sftp_server_hostname = URI of sftp server
            - emr_sftp_server_username
            - emr_sftp_server_password
            - emr_sftp_project_name = folder on the sftp server containing the EMR data
            - emr_data_file = file containing the EMR data
            - emr_log_file = file to be used for logging
            By default, this parameter is disabled. It is also disabled if redi is executing in dry run state

About required and optional configuration parameters
----------------------------------------------------

Following parameters are required to have a value in settings.ini:
 - raw_xml_file
 - translation_table_file
 - form_events_file
 - research_id_to_redcap_id
 - component_to_loinc_code_xml

The program will terminate if they are missing or do not have a value in setings.ini. A message about this will be displayed to the user before the program terminates. The same is also written to the log file.
The above parameters are required irrespective of the state in which redi is executing (normal state or dry run state).

Following parameters are required to have a value in settings.ini when redi is executing in the normal state:
 - redcap_uri
 - token
 - redcap_server
 - redcap_support_receiver_email
 - redcap_support_sender_email
 - smtp_host_for_outbound_mail
 - smtp_port_for_outbound_mail
 - sender_email (if parameter send_email = Y)
 - receiver_email (if parameter send_email = Y)

The program will terminate if they are missing or do not have a value in setings.ini. A message about this will be displayed to the user before the program terminates. The same is also written to the log file.
If the program is executing in dry state then the above parameters are optional

Following parameters are required if we run redi with -e command line argument:
 - emr_sftp_server_hostname
 - emr_sftp_server_username
 - emr_sftp_server_password
 - emr_sftp_project_name
 - emr_data_file
 - emr_log_file

These parameters are essential for establishing connection with the sftp server to obtain EMR data, so if they are missing or do not have a value in settings.ini, then the program will terminate. A message about this will be displayed to the user before the program terminates. The same is also written to the log file.

Following parameters in settings.ini are optional:
 NAME                   DEFAULT VALUE
 system_log_file        redi_log/redi.log
 report_file_path       report.xml
 input_date_format      %Y-%m-%d %H:%M:%S
 output_date_format     %Y-%m-%d
 report_file_path2      report.html
 project                DEFAULT_PROJECT
 rate_limiter           600
 batch_warning_days     13

If the above parameters are missing or do not have a value in settings.ini then the corresponding default value is used and program continues with execution. A message about default value being used is written to the log file.

Testing
-------
1. Go to the vagrant folder and remove the old virtual machine (VM) instance:

   `$ cd vagrant && vagrant destroy`

2. Start a fresh VM:

    `$ vagrant up`

3. To run the tests:

    $ python <project_root_path>/test/TestSuite.py

Note: One of test cases, `TestGenerateOutput`, requires a running REDCap instance. If there is no running REDCap instance details in settings.ini this test case fails. This is a known issue and will be handled in future releases.

@TODO: A sample redcap project and test dataset need to be added.

Contributing
------------

1. Fork it.
2. Create a branch (`git checkout -b my_branch`)
3. Commit your changes (`git commit -am "Add blah blah blah"`)
4. Push to the branch (`git push origin my_branch`)
5. Open a pull request
6. Enjoy a refreshing Diet Coke (diet only) and wait
