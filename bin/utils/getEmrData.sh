#!/bin/bash
# Draft script to connect to an ftp site, get raw EMR data, get log file, 
# and return the possibly modified log file to the FTP server.

# Fix the path on Macs to allow Brewed Gnu Utilities to be the default
export PATH="/usr/local/opt/coreutils/libexec/gnubin:/usr/local/bin:$PATH"

PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && cd ../../ && pwd )"

if [ "$1" = "" ] ; then 
    echo "Please supply the project name"
    exit
else
    PROJECT_NAME=$1
fi

if [ "$2" = "" ] ; then 
    echo "Please supply the URI of the sFTP server"
    exit
else
    URI=$2
fi

MYTEMP=`mktemp -d`

cd $MYTEMP
lftp $URI -e "cd $PROJECT_NAME; get log.txt; get output.csv; bye"
cp output.csv $PROJECT_ROOT/config/raw.txt
cp log.txt $PROJECT_ROOT/log/log.txt

# process data
# Add commands to run other progs here.

# report log data back to EMR staff
cp $PROJECT_ROOT/log/log.txt log.txt
lftp $2 -e "cd $PROJECT_NAME; put log.txt; bye"

# clean up the mess we made
cd $PROJECT_ROOT
rm -rf $MYTEMP

cat $PROJECT_ROOT/config/raw.txt | sed -e "s/&/\&amp;/g; s/</\&lt; /g; s/>/\&gt; /g; " > $PROJECT_ROOT/config/rawEscaped.txt 
$PROJECT_ROOT/bin/utils/csv2xml.py --input-encoding=cp1252  --output-encoding=utf8 --header \
  --delimiter=,  --xml-declaration -tstudy -rsubject --output-file=$PROJECT_ROOT/config/raw.xml \
  $PROJECT_ROOT/config/rawEscaped.txt

rm $PROJECT_ROOT/config/rawEscaped.txt 
