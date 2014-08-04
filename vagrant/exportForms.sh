#!/bin/bash

batch=$1
forms="demographics chemistry cbc inr hcv_rna_results"
if [ ! -e $batch ]; then
    mkdir $batch
fi


for form in $forms
    do
      ../bin/utils/redcap_records.py --token=121212 --url=http://localhost:8998/redcap/api/ --forms=$form > $batch/$form.csv
    done
