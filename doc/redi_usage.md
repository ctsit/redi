# RED-I Usage

Currently the RED-I application can be only executed from the command line:

`$ redi`

## Optional command-line arguments:

 - -h, --help: show the help message
 - -c: Specify the path to the configuration folder.

        $ redi -c /Users/admin/redi-config

    Default path for config folder is **<path-to-data-directory>/config**.
    For "data directory" refer --datadir.

 - -k, --keep: Prevents deletion of the output files generated during
   data processing.

        $ redi -k

    When this parameter is provided, the output files are stored in 
    **<project_root_path>/out/out_\<timestamp>**.

    The timestamp has the format: **YYYY_MM_DD-HH_MM_SS**.

    If the parameter is not provided, the output files are stored in a
    temporary folder during the execution of **redi** and then deleted
    along with the temporary folder once **redi** finishes execution.

 - -d, --dryrun : Performs a dry run.

        $ redi --dryrun

    When this parameter is provided, all data transformations are
    performed and execution stops after writing out the final data set to 
    **<project_root_path>/out/out_\<timestamp>**.

    The purpose of this switch is to assist developers in performing a dry run
    of `redi`. Data will not be written to the REDCap server nor will emails 
    be sent.

    If `-d` is used, `--keep=yes` is implied; therefore, you do not need to
    specify it or provide any path for storing the output files.

    By default, this parameter is disabled.

 - -e, --emrdata: Runs the script for fetching EMR data.

        $ redi --emrdata

    When this parameter us provided, a connection will be established with the
    sftp server mentioned in the settings.ini file in the config folder and EMR
    data required for the execution of **redi** will be downloaded.

    Following parameters need to be set in config/settings.ini before using this option:
    - emr_sftp_server_hostname = URL of the SFTP Server
    - emr_sftp_server_username
    - emr_sftp_server_password
    - emr_sftp_project_name = folder on the SFTP server containing the EMR data
    - emr_data_file = file containing the EMR data

    By default, this parameter is disabled.

 - -r, --resume: Resumes a previously stopped run of `redi`.

    ***WARNING!!!*** This is used in a very specific case. Use with caution.

    Once **redi** has completed processing, it sends its data to configured 
    REDCap Server. Each transaction is initially marked as *unsent* and only
    after a response from the REDCap Server is it changed to *sent*. 
    If you stop **redi** from running during this time, it is possible to 
    resume where it left off by specifying the `--resume` switch.

    Do not use `--resume` for a first run; it will fail. Using `--resume`
    once a run has completed is unsupported, but won't do much other than
    send the email the report again.

    The development team is looking to make this a more robust and safer
    feature in the future.

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
