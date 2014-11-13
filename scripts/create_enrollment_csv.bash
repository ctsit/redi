#!/bin/bash
#
# Generates subject enrollment records which can be used with the Sample #
# Project.
#
# Example:
#
#   bash add_subjects.bash 10 > ../config-example/enrollment_test_data.csv
#

echo "record_id,redcap_event_name,c2826694,c1301894,c2985782,c0806020,enrollment_complete"

for i in $(seq 1 $1)
do
	echo "\"$i\",\"1_arm_1\",\"$i\",\"${i}007\",\"2112-01-03\",\"2113-01-01\",2";
done

