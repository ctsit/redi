RED-I Configuration
===================

Required Parameters
~~~~~~~~~~~~~~~~~~~

The following parameters are required to have a value in
**settings.ini**:

-  raw\_xml\_file
-  translation\_table\_file
-  form\_events\_file
-  research\_id\_to\_redcap\_id
-  component\_to\_loinc\_code\_xml

If any of the parameters listed above is missing then the program will
terminate. A detailed message about the missing parameter will be
displayed to the user before the program terminates as well as written
to the log file.

Conditional Parameters
~~~~~~~~~~~~~~~~~~~~~~

While the parameters mentioned in the `section
above <###Required%20Parameters>`__ are always required, the following
parameters are only required to have a value in **settings.ini** when
**redi** is not performing a dry run.

-  redcap\_uri
-  token
-  redcap\_support\_receiver\_email
-  redcap\_support\_sender\_email
-  smtp\_host\_for\_outbound\_mail
-  smtp\_port\_for\_outbound\_mail
-  sender\_email *(only required when **send\_email** is set to **Y**)*
-  receiver\_email *(only required when **send\_email** is set to
   **Y**)*

Note: In "dry run" mode the RED-I will not send any data to REDCap.

The following parameters are required only when ``--emrdata`` is
specified on the command line:

-  emr\_sftp\_server\_hostname
-  emr\_sftp\_server\_username
-  emr\_sftp\_server\_password
-  emr\_sftp\_project\_name
-  emr\_data\_file

These parameters are essential for establishing a connection with the
SFTP server to obtain EMR data; so, if they are missing or do not have a
value in settings.ini, then the program will terminate. As with the
required parameters, a message about this will be displayed to the user
before the program terminates as well as written to the log file.

Optional Parameters
~~~~~~~~~~~~~~~~~~~

Following parameters in settings.ini are optional:

+------------------------+---------------------+
| Parameter Name         | Default Value       |
+========================+=====================+
| report\_file\_path     | report.xml          |
+------------------------+---------------------+
| report\_file\_path2    | report.html         |
+------------------------+---------------------+
| input\_date\_format    | %Y-%m-%d %H:%M:%S   |
+------------------------+---------------------+
| output\_date\_format   | %Y-%m-%d            |
+------------------------+---------------------+
| project                | DEFAULT\_PROJECT    |
+------------------------+---------------------+
| rate\_limiter          | 600                 |
+------------------------+---------------------+
| batch\_warning\_days   | 13                  |
+------------------------+---------------------+

If the above parameters are missing or do not have a value in
**settings.ini** then the corresponding default value is used. Whenever
a default value is used, a message about is written to the log file.
