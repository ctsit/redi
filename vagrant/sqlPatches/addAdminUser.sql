# create basic user admin with password of 'password', security question of 'nickname' with answer of 'jane'
REPLACE INTO `redcap_user_information`
   (username, user_email, user_firstname, user_lastname, user_inst_id, super_user, user_firstvisit, allow_create_db )
 VALUES
   ('admin','jane_doe@example.org','Jane','Doe','ESU',1,'2013-07-26 11:18:08',1);

REPLACE INTO `redcap_auth`
   (username,password,temp_pwd, password_question, password_answer)
VALUES
   ('admin',md5('password'),0,1,md5('jane'));

# give full access to my project
# Note: the list of forms below need to be modified to match the form list on your project
# Note: the API token below is bogus.  It might work as-is, but this key is untested.

REPLACE INTO `redcap_user_rights` 
(project_id
, username
, expiration
, group_id
, lock_record
 
, lock_record_multiform
, lock_record_customize
, data_export_tool
, data_import_tool
, data_comparison_tool

, data_logging
, file_repository
, double_data
, user_rights
, data_access_groups

, graphical
, reports
, design
, calendar

, data_entry
, api_token

, api_export
, api_import
, record_create
, record_rename
, record_delete

, dts
, participants
, data_quality_design
, data_quality_execute
, random_setup

, random_dashboard
, random_perform)
VALUES (
   12,'admin',NULL,NULL,1,
   1,1,1,1,1,
   1,1,1,0,1,
   1,1,1,1,
   '[demographics,1][inclusion_exclusion,1][key_medical_history,1][substance_use,1][il28b_hcv_genotypes,1][fibrosis_staging,1][cbc,1][chemistry,1][inr,1][hcv_rna_results,1][interferon_administration,1][ribavirin_administration,1][daa_administration,1][adverse_events,1][prescription_conmeds,1][early_discontinuation_eot,1][derived_values_baseline,1][derived_values,1]',
   '121212',
   1,1,1,1,1,
   0,1,1,1,3,
   0,0);
