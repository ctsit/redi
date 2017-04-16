#!/bin/bash
if [ $# -lt 2 ]
then
  echo "Usage: \n\tgenerate_enrollement.sh <number_of_records> <name_of_output_file>"
  exit
fi
NUMBER_OF_RECORDS=$1
ENROLLMENT_DATA_FILE=$2
echo "dm_subjid,redcap_event_name,dm_usubjid,demographics_complete" > $ENROLLMENT_DATA_FILE
for i in $(seq 1 $NUMBER_OF_RECORDS) 
do
  event_name=$i'_arm_'$i
  random_subject_id=`echo $RANDOM % 999 + 1 | bc`
  echo \"$i\",\"$event_name\",\"999-$random_subject_id\",\"2\" >> $ENROLLMENT_DATA_FILE
done
