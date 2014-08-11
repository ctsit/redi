#!/usr/bin/env bash

# some reasonable defaults
SHARED_FOLDER=/vagrant

# The user provides a copy of the redcap binary folder as a zip file
REDCAP_ZIP_FILE=redcap.zip
REDCAP_VERSION=5.7.4
REDCAP_SCHEMA_FILE=projectDataBootstrap.sql

# import helper functions
. bootstrap_functions.sh

# verify availability of redcap.zip
if [ ! -e "$SHARED_FOLDER/$REDCAP_ZIP_FILE" ]; then
   echo "Expecting the redcap binary files as a zip file: '$REDCAP_ZIP_FILE'"
   exit 1
fi


# call helper functions from `bootstrap_functions.sh`
extract_redcap
create_redcap_user
create_redcap_tables
patch_redcap_tables
update_redcap_connection_settings
run_environment_updates
check_redcap_status

