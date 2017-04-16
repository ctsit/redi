#!/bin/bash
##############################################################################
#                                                                           ##
#    generate_fake_records.sh                                               ##  
#         Script to generate fake records.                                  ##
#                                                                           ##
#    Expected input:                                                        ##
#         <#records> - number of records to create                          ##
#         <enrollment_file> - specify the name of the enrollment file here. ##
#                             this is typically enrollment_test_data.csv    ##
#         <input_xml> - Specify the name of raw.xml. typically it is raw.xml##
#                                                                           ##
#     NOTE: This script pull the subject_ids from REDCap and then generates ##
#           the input(raw.xml) and enrollement_test_data.csv based on these ##
#           reference ids obtained from REDCap.                             ##
##############################################################################
if [ $# -lt 3 ]
then
  echo "Usage: \n\tgenerate_fake_records.sh <#records> <enrollment_file> <input_xml>"
  echo "eg.,: ./generate_fake_records.sh 10 enrollment_test_data.csv raw.xml"
  exit
fi
NUMBER_OF_RECORDS=$1
ENROLLMENT_DATA_FILE=$2
INPUT_FILE=$3
SUBJECT_IDS=()
##################### Get all possible subject ids from Redcap #####################
REFERENCE_IDS=($(curl -F token=121212 -F overwriteBehavior=normal -F content=record -F \
  format=json -F type=flat http://localhost:8998/redcap/api/ | \
  python -m json.tool | grep "dm_usubjid\"" | \
  tr -d ' "dm_usubjid:,' | sed '/^$/d'))
############# END - Get all possible subject ids from Redcap #######################

###################### ID management #######################
if [ ${#REFERENCE_IDS[@]} -gt $NUMBER_OF_RECORDS ] || [ ${#REFERENCE_IDS[@]} -eq $NUMBER_OF_RECORDS ]
then
  i=0
  for id in ${REFERENCE_IDS[@]}
  do
    if [ $i == $NUMBER_OF_RECORDS ]
    then
      break
    fi
    SUBJECT_IDS+=($id)
    i=$(($i+1))
  done
elif [ ${#REFERENCE_IDS[@]} -lt $NUMBER_OF_RECORDS ]
then
  ##### use up all the reference ids from redcap ########
  for id in ${REFERENCE_IDS[@]}
  do
    SUBJECT_IDS+=($id)
  done
  ####### generate some random ones for the remaining ###
  RANDOM_RECORDS_COUNT=$(($NUMBER_OF_RECORDS - ${#REFERENCE_IDS[@]}))
  for i in $(seq 1 $RANDOM_RECORDS_COUNT)
  do
    random_subject_id=`echo $RANDOM % 999 + 1 | bc`
    # some padding
    if [ ${#random_subject_id} -eq 2 ]
    then
      random_subject_id=0$random_subject_id
    elif [ ${#random_subject_id} -eq 1 ]
    then
      random_subject_id=00$random_subject_id
    fi
    SUBJECT_IDS+=('999-0'$random_subject_id)
  done
fi
echo ${REFERENCE_IDS[@]}
echo "#######################"
echo ${SUBJECT_IDS[@]}
############## END - ID management #########################

############ Generate Enrollment data CSV ##################
ENROLLMENT_STRING="dm_subjid,redcap_event_name,dm_usubjid,demographics_complete"
for i in $(seq 1 $NUMBER_OF_RECORDS)
do
  event_name=$i'_arm_1'
  temp_string="\"$i\",\"$event_name\",\"${SUBJECT_IDS[$i-1]}\",\"2\""
  ENROLLMENT_STRING="$ENROLLMENT_STRING\n$temp_string"
done
echo -e $ENROLLMENT_STRING > $ENROLLMENT_DATA_FILE
########### END - Generate Enrollment data CSV #############

################# Generate input file ######################
INPUT_STRING="<?xml version=\"1.0\" encoding=\"utf8\"?>"
INPUT_STRING="$INPUT_STRING\n<study>"
component_id=1111110
for subject_id in ${SUBJECT_IDS[@]}
do
  component_id=$(($component_id+5))
  INPUT_STRING="$INPUT_STRING\n\t<subject>\n"
  INPUT_STRING="$INPUT_STRING\t\t<NAME>FAKE NAME</NAME>\n
                \t\t<COMPONENT_ID>$component_id</COMPONENT_ID>\n
                \t\t<ORD_VALUE>2.2</ORD_VALUE>\n
                \t\t<REFERENCE_LOW>1.8</REFERENCE_LOW>\n
                \t\t<REFERENCE_HIGH>7.8</REFERENCE_HIGH>\n
                \t\t<REFERENCE_UNIT>thou/cu mm</REFERENCE_UNIT>\n
                \t\t<SPECIMN_TAKEN_TIME>2112-11-14 01:01:00</SPECIMN_TAKEN_TIME>\n
                \t\t<RESULT_DATE>2112-11-20 00:00:00</RESULT_DATE>\n"
  INPUT_STRING="$INPUT_STRING\t\t<STUDY_ID>$subject_id</STUDY_ID>"
  INPUT_STRING="$INPUT_STRING\n\t</subject>"
done
INPUT_STRING="$INPUT_STRING\n</study>"
echo -e $INPUT_STRING > $INPUT_FILE
########### END - Generate input file ######################
