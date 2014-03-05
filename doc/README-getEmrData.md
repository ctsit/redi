# Using getEmrData.sh

getEmrData.sh is a shell script that will move data between local configuration directories and a remote sftp server.  It uploads the subject map to the server, downloads the log, downloads the emr data and then re-uploads the log file.

usage

	bin/utils/getEmrData.sh <your_project_name> <your_sftp_uri>
