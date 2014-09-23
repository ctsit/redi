#!/bin/bash
# This script can be used to find differences in config files

REF_SETTINGS=reference_settings.ini
NEW_SETTINGS=new_settings.ini

usage() {
   echo "Compares two files but ignore empty lines and lines starting with #"
   echo "	Usage: $0 <settings_file_1> <settings_file_2>"
}

if [ "$#" != 2 ]; then
   usage
   exit 0
fi

grep -v ^\# $1 | grep -v ^$ | sort > $REF_SETTINGS
grep -v ^\# $2 | grep -v ^$ | sort > $NEW_SETTINGS
colordiff $REF_SETTINGS $NEW_SETTINGS

rm $REF_SETTINGS $NEW_SETTINGS
