#!/usr/bin/env bash


# echo "To view all users run the query: select * from redcap.redcap_auth"
# show tables with `utf8_general_ci` collation
#mysql -uroot -ppassword -e "select table_schema, table_name, table_collation from information_schema.tables WHERE table_schema = 'redcap' AND table_collation = 'utf8_general_ci' "



function run_environment_updates() {
   # environment utils
   cp $SHARED_FOLDER/aliases /home/vagrant/.bash_aliases
   cp $SHARED_FOLDER/vimrc /home/vagrant/.vimrc

   # Install libraries used by python
   apt-get update
   apt-get install -y python-setuptools libxml2 libxslt1-dev python-dev

   # Install utils
   apt-get install -y vim ack-grep
   apt-get install -y sqlite3

   # configure MySQL to start every time
   update-rc.d mysql defaults

   # Install mcrypt package for PHP
   apt-get install -y php5-mcrypt
}

function extract_redcap() {
   # Extract the binaries to the destination folder
   # Note: use `-o` option to overwrite existing files
   rm -rf /var/www/*

   unzip -q $REDCAP_ZIP_FILE -d /var/www/

   REDCAP_VERSION_DETECTED=`ls /var/www/redcap | grep redcap_v | cut -d 'v' -f2 | sort -n | tail -n 1`
   echo "$REDCAP_ZIP_FILE content indicates Redcap version: $REDCAP_VERSION_DETECTED"
  
   # copy the plugin files to the redcap version detected
   PLUGINS_DESTINATION_FOLDER="/var/www/redcap/plugins/redi"
   mkdir -p $PLUGINS_DESTINATION_FOLDER
   echo "Copying RED-I REDCap plugins to $PLUGINS_DESTINATION_FOLDER"
   cp $SHARED_FOLDER/plugins/* $PLUGINS_DESTINATION_FOLDER

   # adjust ownership so apache can write to the temp folders
   chown -R www-data.root /var/www/redcap/edocs/
   chown -R www-data.root /var/www/redcap/temp/

   # Delete default Apache index file fron /var/www/ so the developers can see both apps
   rm -f /var/www/index.html
}

function drop_redcap_user() {
   echo 'exec drop_redcap_user'
   mysql -ppassword <<SQL
DROP PROCEDURE IF EXISTS mysql.drop_user_if_exists ;
DELIMITER $$
CREATE PROCEDURE mysql.drop_user_if_exists()
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
CALL mysql.drop_user_if_exists() ;
DROP PROCEDURE IF EXISTS mysql.drop_users_if_exists ;
SQL
}

function create_redcap_user() {
   # Delete old user if it exists
   drop_redcap_user

   echo 'exec create_redcap_user'
   # create the user redcap and grant it full access to DB redcap
   mysql -ppassword <<SQL
DROP DATABASE IF EXISTS redcap;
CREATE DATABASE redcap;

CREATE USER
   'redcap'@'localhost';
GRANT
   SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, ALTER, EXECUTE, CREATE VIEW, SHOW VIEW
ON
   redcap.*
TO
   'redcap'@'localhost'
IDENTIFIED BY
   'password';
SQL
}

function create_redcap_tables_from_custom_file() {
   echo "Using existing file: '$REDCAP_SCHEMA_FILE' to create tables and import project data"
   # load initial REDCap data
   SCRATCH_SQL=/tmp/scratch.sql
   if [ -f $SCRATCH_SQL ]; then
      rm $SCRATCH_SQL
   fi

   echo "SET foreign_key_checks = 0;" > $SCRATCH_SQL
   cat $REDCAP_SCHEMA_FILE >> $SCRATCH_SQL
   echo "SET foreign_key_checks = 1;" >> $SCRATCH_SQL
   echo "Rewriting DEFINER for all views to redcap@localhost"
   sed -e "s/DEFINER=\`.\+\`@\`[0-9.]\+\`/DEFINER=\`redcap\`@\`localhost\`/g;" -i $SCRATCH_SQL
   echo "Executing queries from: $REDCAP_SCHEMA_FILE this will take a few minutes"
   mysql -uredcap -ppassword redcap < $SCRATCH_SQL
}


# Create tables from sql files distributed with redcap under
#  redcap_vA.B.C/Resources/sql/
#
# @see install.php for details
function create_redcap_tables_from_distribution() {
   SQL_DIR=/var/www/redcap/redcap_v$REDCAP_VERSION_DETECTED/Resources/sql/
   mysql -ppassword redcap < $SQL_DIR/install.sql
   mysql -ppassword redcap < $SQL_DIR/install_data.sql
   mysql -ppassword redcap -e "UPDATE redcap.redcap_config SET value = '$REDCAP_VERSION_DETECTED' WHERE field_name = 'redcap_version' "

   files=$(ls -v $SQL_DIR/create_demo_db*.sql)
      for i in $files;do
         echo "Executing sql file $i"
         mysql -ppassword redcap < $i
      done
}

function create_redcap_tables() {
   echo 'create_redcap_tables'

   if [ -f $REDCAP_SCHEMA_FILE ]; then
      create_redcap_tables_from_custom_file
      patch_redcap_tables
   else
      create_redcap_tables_from_distribution
   fi
}

function patch_redcap_tables() {
   # Add patches
   SQL_PATCHES=/vagrant/sqlPatches
   if [ -d "$SQL_PATCHES" ];then
      files=$(ls -v $SQL_PATCHES/*.sql)
      for i in $files;do
         echo "Executing sql file $i"
         mysql -ppassword redcap < $i
      done
   fi
}

function update_redcap_connection_settings() {
   # edit redcap database config file (This needs to be done after extraction of zip files)
   echo "Setting the connection variables in: /var/www/redcap/database.php"
   echo '$hostname   = "localhost";' >> /var/www/redcap/database.php
   echo '$db         = "redcap";'    >> /var/www/redcap/database.php
   echo '$username   = "redcap";'    >> /var/www/redcap/database.php
   echo '$password   = "password";'  >> /var/www/redcap/database.php
   echo '$salt   = "abc";'  >> /var/www/redcap/database.php
}

function check_redcap_status() {
   # Check if the apache server is actually serving the redcap files
   echo "Checking if redcap application is running..."
   curl -s http://localhost/redcap/ | grep -i 'Welcome\|Critical Error'
   echo "Please try to login to REDCap as user 'admin' and password: 'password'"
}

version_less_then() {
   if [ "$1" = '`echo -e "$1\n$2" | sort -V | head -n1`' ]; then
      return 1
   else
     return 0
   fi
}


