#!/usr/bin/env bash

# some reasonable defaults
export SHARED_FOLDER=/vagrant

# environment utils
cp $SHARED_FOLDER/aliases /home/vagrant/.bash_aliases

# Install libraries used by python
apt-get update
apt-get install -y python-setuptools libxml2 libxslt1-dev

# Install utils
apt-get install -y vim ack-grep

# The user provides a copy of the redcap binary folder as a zip file
REDCAP_ZIP_FILE=redcap.zip

# configure MySQL to start every time
update-rc.d mysql defaults

# Create a new redcap database called redcap with associated user
# Delete any existing user
mysql -ppassword <<EOF
drop database if exists redcap;
create database redcap;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ANSI';
USE redcap ;
DROP PROCEDURE IF EXISTS redcap.drop_user_if_exists ;
DELIMITER $$
CREATE PROCEDURE redcap.drop_user_if_exists()
BEGIN
  DECLARE foo BIGINT DEFAULT 0 ;
  SELECT COUNT(*)
  INTO foo
    FROM mysql.user
      WHERE User = 'redcap' and  Host = 'localhost';
   IF foo > 0 THEN
         DROP USER 'redcap'@'localhost' ;
  END IF;
END ;$$
DELIMITER ;
CALL redcap.drop_user_if_exists() ;
DROP PROCEDURE IF EXISTS redcap.drop_users_if_exists ;
SET SQL_MODE=@OLD_SQL_MODE
EOF

# create the user redcap and grant it full access to DB redcap
mysql -ppassword <<EOF
drop database if exists redcap;
create database redcap;
create user 'redcap'@'localhost';
grant SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, ALTER, EXECUTE  on redcap.* to 'redcap'@'localhost' identified by 'password';
EOF

# load initial REDCap data
SCRATCH_SQL=/tmp/scratch.sql
if [ -f $SCRATCH_SQL ]; then
  rm $SCRATCH_SQL
fi

echo "SET foreign_key_checks = 0;" > $SCRATCH_SQL
cat $SHARED_FOLDER/projectDataBootstrap.sql >> $SCRATCH_SQL
echo "SET foreign_key_checks = 1;" >> $SCRATCH_SQL
echo "Executing queries from: $SHARED_FOLDER/projectDataBootstrap.sql this will take a few minutes"
mysql -ppassword redcap < $SCRATCH_SQL

# Add patches
export SQL_PATCHES=/vagrant/sqlPatches
if [ -d "$SQL_PATCHES" ];then
	files=$(ls -v $SQL_PATCHES/*.sql)
	for i in $files;do
		echo "Executing sql file $i"
		mysql -ppassword redcap < $i
	done
fi



if [ ! -e "$SHARED_FOLDER/$REDCAP_ZIP_FILE" ]; then
   echo "Expecting the redcap binary files as a zip file: 'redcap.zip'"
   exit 1
fi

# Extract the binaries to the destination folder
# Note: use `-o` option to overwrite existing files
rm -rf /var/www/*

unzip $SHARED_FOLDER/$REDCAP_ZIP_FILE -d /var/www/

REDCAP_VERSION_DETECTED=`ls /var/www/redcap | grep redcap_v | cut -d 'v' -f2`
echo "$REDCAP_ZIP_FILE content indicates Redcap version: $REDCAP_VERSION_DETECTED"


# adjust ownership so apache can write to the temp folders
chown -R www-data.root /var/www/redcap/edocs/
chown -R www-data.root /var/www/redcap/temp/

# Delete default Apache index file fron /var/www/ so the developers can see both apps
rm -f /var/www/index.html

version_less_then() {
   if [ "$1" = '`echo -e "$1\n$2" | sort -V | head -n1`' ]; then
      return 1
   else
     return 0
   fi
}

# edit redcap database config file (This needs to be done after extraction of zip files)
echo "Setting the connection variables in: /var/www/redcap/database.php"
echo '$hostname   = "localhost";' >> /var/www/redcap/database.php
echo '$db         = "redcap";'    >> /var/www/redcap/database.php
echo '$username   = "redcap";'    >> /var/www/redcap/database.php
echo '$password   = "password";'  >> /var/www/redcap/database.php
echo '$salt   = "abc";'  >> /var/www/redcap/database.php

# Check if the apache server is actually serving the redcap files
echo "Checking if redcap application is running..."
curl -s http://localhost/redcap/ | grep -i 'Welcome\|Critical Error'

echo "Please try to login as user 'admin' and password: 'password'"

# echo "To view all users run the query: select * from redcap.redcap_auth"
# show tables with `utf8_general_ci` collation
#mysql -uroot -ppassword -e "select table_schema, table_name, table_collation from information_schema.tables WHERE table_schema = 'redcap' AND table_collation = 'utf8_general_ci' "

