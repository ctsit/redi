# RED-I Project

![DOI](https://zenodo.org/badge/doi/10.5281/zenodo.10014.png ".")

The REDCap Electronic Data Importer (RED-I) is a tool to automate the process of loading clinical data from Electronic Medical Records (EMRs) into [REDCap](http://www.project-redcap.org/) Study data capture systems. RED-I is a general purpose tool for REDCap data importing suitable for use on any study in any REDCap system. It uses XML lookups to translate data stored in comma separated values (CSV) files and uploads it to a REDCAP Server using the REDCap API. The tool allows study data to be securely uploaded from clinical reporting systems, error checked, and uploaded into REDCap. It provides the investigator with feedback on upload success in the form of summary reporting of the data upload process.


## Directory Layout

    redi : This is the common repository for RED-I. This repository contains generic artifacts
    ├── CHANGELOG : Log of changes to the RED-I project
    ├── bin/ : Contains the Python modules
    ├── config-example/ : Example configuration files
    ├── doc/ : Contains documentation such as installation instructions and process flow
    ├── README.md : This README markdown file
    ├── scripts/ : Contains useful scripts to developers
    └── test/ : Contains the test modules and test suite


## Installation

From source:

    $ git clone https://github.com/ctsit/redi.git redi
    $ cd redi
    $ make
    $ make install

Reference [README-install](doc/README-install.md) for more installation details.


## Configuration

Adapt the example configuration folder and the **settings.ini** to fit your needs.

### Required Parameters

The following parameters are required to have a value in **settings.ini**:

 - raw_xml_file
 - translation_table_file
 - form_events_file
 - research_id_to_redcap_id
 - component_to_loinc_code_xml

The program will terminate if they are missing or do not have a value in **settings.ini**. A message about this will be displayed to the user before the program terminates as well as written to the log file.

### Conditional Parameters

Whereas the aforementioned parameters are always required, the following parameters are only required to have a value in **settings.ini** when **redi** is not performing a dry run:

 - redcap_uri
 - token
 - redcap_server
 - redcap_support_receiver_email
 - redcap_support_sender_email
 - smtp_host_for_outbound_mail
 - smtp_port_for_outbound_mail
 - sender_email *(only required when **send_email** is set to **Y**)*
 - receiver_email *(only required when **send_email** is set to **Y**)*

The program will terminate if they are missing or do not have a value in **settings.ini**. A message about this will be displayed to the user before the program terminates as well as written to the log file.

The following parameters are required only when `--emrdata=yes` is specified on the command line:

 - emr_sftp_server_hostname
 - emr_sftp_server_username
 - emr_sftp_server_password
 - emr_sftp_project_name
 - emr_data_file

These parameters are essential for establishing a connection with the SFTP server to obtain EMR data; so, if they are missing or do not have a value in settings.ini, then the program will terminate. As with the required parameters, a message about this will be displayed to the user before the program terminates as well as written to the log file.

### Optional Parameters

Following parameters in settings.ini are optional:

 Parameter Name         |Default Value
 ---------------------- |-------------
 report_file_path       |report.xml
 report_file_path2      |report.html
 input_date_format      |%Y-%m-%d %H:%M:%S
 output_date_format     |%Y-%m-%d
 project                |DEFAULT_PROJECT
 rate_limiter           |600
 batch_warning_days     |13

If the above parameters are missing or do not have a value in **settings.ini** then the corresponding default value is used. Whenever a default value is used, a message about is written to the log file.


## Usage

`$ redi`

Optional command-line arguments:

 - -h, --help: show the help message
 - -c: Specify the path to the configuration folder.

        $ redi -c /Users/admin/redi-config

    Default path for config folder is **<path-to-data-directory>/config**.
    For "data directory" refer --datadir.

 - -k, --keep: Prevents deletion of the output files generated during data processing.

        $ redi -k yes

    When this parameter is provided, the output files are stored in **<project_root_path>/out/out_\<timestamp>**.

    The timestamp has the format: **YYYY_MM_DD-HH_MM_SS**.

    If the parameter is not provided, the output files are stored in a temporary folder during the execution of **redi** and then deleted along with the temporary folder once **redi** finishes execution.

 - -d, --dryrun : Performs a dry run.

        $ redi --dryrun

    When this parameter is provided, all data transformations are performed and execution stops after writing out the final data set to **<project_root_path>/out/out_\<timestamp>**.

    The purpose of this switch is to assist developers in performing a dry run of `redi`. Data will not be written to the REDCap server nor will emails be sent.

    If `-d` is used, `--keep=yes` is implied; therefore, you do not need to specify it or provide any path for storing the output files.

    By default, this parameter is disabled.

 - -e, --emrdata: Runs the script for fetching EMR data.

        $ redi --emrdata=yes

    When this parameter us provided, a connection will be established with the sftp server mentioned in the settings.ini file in the config folder and EMR data required for the execution of **redi** will be downloaded.

    Following parameters need to be set in config/settings.ini before using this option:
    - emr_sftp_server_hostname = URL of the SFTP Server
    - emr_sftp_server_username
    - emr_sftp_server_password
    - emr_sftp_project_name = folder on the SFTP server containing the EMR data
    - emr_data_file = file containing the EMR data

    By default, this parameter is disabled.

 - -r, --resume: Resumes a previously stopped run of `redi`.

    ***WARNING!!!*** This is used in a very specific case. Use with caution.

    Once **redi** has completed processing, it sends its data to configured REDCap Server. Each transaction is initially marked as *unsent* and only after a response from the REDCap Server is it changed to *sent*. If you stop **redi** from running during this time, it is possible to resume where it left off by specifying the `--resume` switch.

    Do not use `--resume` for a first run; it will fail. Using `--resume` once a run has completed is unsupported, but won't do much other than send the email the report again.

    The development team is looking to make this a more robust and safer feature in the future.

 - --datadir: Specify path to the data directory

    $ redi --datadir /Users/admin/redi_output

    The data directory is the directory that will store the following:
     - log file
     - SQLite database used for storing checksums
     - intermediate output files which are required for debugging and used by the resume logic
     - configuration directory (unless a different path for this is specified by the user)

    By default, the data directory is assumed to be the current working directory.
    Using this switch, one can run multiple instances of redi simultaneously.

 - -v, --verbose: increase verbosity of output

    $ redi --verbose

 - --skip-blanks: skip blank events when sending event data to RedCAP

    $ redi --skip-blanks

## Testing

To run all tests:

    $ make tests

Some tests may require a REDCap instance to pass.

1. Go to the vagrant folder and remove the old virtual machine (VM) instance:

        $ cd vagrant && vagrant destroy

2. Start a fresh VM:

        $ vagrant up

3. To run the tests:

        $ make tests


## Contributing

1. Fork it.
2. Create a branch (`git checkout -b my_branch`)
3. Commit your changes (`git commit -am "Add blah blah blah"`)
4. Push to the branch (`git push origin my_branch`)
5. Open a pull request
6. Enjoy a refreshing Diet Coke (diet only) and wait
