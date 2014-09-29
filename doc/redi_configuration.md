# RED-I Configuration

### Required Parameters

The following parameters are required to have a value in **settings.ini**:

 - raw_xml_file
 - translation_table_file
 - form_events_file
 - research_id_to_redcap_id
 - component_to_loinc_code_xml

If any of the parameters listed above is missing then the program will terminate.
A detailed message about the missing parameter will be displayed to the user before the
program terminates as well as written to the log file.

### Conditional Parameters

While the parameters mentioned in the [section above](###Required Parameters)
are always required, the following parameters are only required to have a
value in **settings.ini** when **redi** is not performing a dry run.

 - redcap_uri
 - token
 - redcap_support_receiver_email
 - redcap_support_sender_email
 - smtp_host_for_outbound_mail
 - smtp_port_for_outbound_mail
 - sender_email *(only required when **send_email** is set to **Y**)*
 - receiver_email *(only required when **send_email** is set to **Y**)*

Note: In "dry run" mode the RED-I will not send any data to REDCap.

The following parameters are required only when `--emrdata` is specified on
the command line:

 - emr_sftp_server_hostname
 - emr_sftp_server_username
 - emr_sftp_server_password
 - emr_sftp_project_name
 - emr_data_file

These parameters are essential for establishing a connection with the SFTP 
server to obtain EMR data; so, if they are missing or do not have a value
in settings.ini, then the program will terminate. As with the required 
parameters, a message about this will be displayed to the user before the 
program terminates as well as written to the log file.

### Optional Parameters

Following parameters in settings.ini are optional:

 Parameter Name         | Default Value
 ---------------------- |-------------
 report_file_path       | report.xml
 report_file_path2      | report.html
 input_date_format      | %Y-%m-%d %H:%M:%S
 output_date_format     | %Y-%m-%d
 project                | DEFAULT_PROJECT
 rate_limiter           | 600
 batch_warning_days     | 13

If the above parameters are missing or do not have a value in **settings.ini**
then the corresponding default value is used. Whenever a default value is used,
a message about is written to the log file.

