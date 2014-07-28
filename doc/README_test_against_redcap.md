
Steps
===

1) Create a project using instructions from
   https://github.com/ctsit/research-subject-mapper/blob/master/doc/Person_Index_Loading_Instructions/Person_Index_Loading_Instructions.md

   Optionally you can get a local copy of the project:
      git clone https://github.com/ctsit/research-subject-mapper


   The goal of step 1 is to get an API key like: EF5A6625C9C3911AA350C33807C12152
   which can be used to retrive data from RedCAP by running a script

2) Enter data for 5 persons using the RedCAP web interface


3) Verify manually (optional) that the data is saved to the database:

(root@localhost) [redcap]> select project_id, project_name, arm_id, arm_num, arm_name, event_id, form_name, record, group_concat(field_name, ' : ', value)   from redcap_events_forms natural join redcap_events_metadata natural join redcap_events_arms natural join redcap_projects natural join redcap_data where form_name = 'person_identifiers' group by record order by record;
+------------+-----------------------------+--------+---------+----------+----------+--------------------+----------+-------------------------------------------------------------------------------------------------------------------------+
| project_id | project_name                | arm_id | arm_num | arm_name | event_id | form_name          | record   | group_concat(field_name, ' : ', value)                                                                                  |
+------------+-----------------------------+--------+---------+----------+----------+--------------------+----------+-------------------------------------------------------------------------------------------------------------------------+
|         20 | hcv_person_index_asura_test |     21 |       1 | Arm 1    |      110 | person_identifiers | 999-1111 | study_subject_number_verifier_value : 1947,person_identifiers_complete : 2,study_subject_number : 999-1111,mrn : 123321 |
|         20 | hcv_person_index_asura_test |     21 |       1 | Arm 1    |      110 | person_identifiers | 999-1212 | study_subject_number_verifier_value : 1948,mrn : 234432,person_identifiers_complete : 2,study_subject_number : 999-1212 |
|         20 | hcv_person_index_asura_test |     21 |       1 | Arm 1    |      110 | person_identifiers | 999-1234 | study_subject_number_verifier_value : 1945,mrn : 123456,person_identifiers_complete : 2,study_subject_number : 999-1234 |
|         20 | hcv_person_index_asura_test |     21 |       1 | Arm 1    |      110 | person_identifiers | 999-3211 | study_subject_number_verifier_value : 1949,mrn : 345543,person_identifiers_complete : 2,study_subject_number : 999-3211 |
|         20 | hcv_person_index_asura_test |     21 |       1 | Arm 1    |      110 | person_identifiers | 999-6789 | study_subject_number_verifier_value : 1946,mrn : 654321,person_identifiers_complete : 2,study_subject_number : 999-6789 |
+------------+-----------------------------+--------+---------+----------+----------+--------------------+----------+-------------------------------------------------------------------------------------------------------------------------+
5 rows in set (0.00 sec)


