
Intro
====

The redcapdbm.php script allows to perform basic maintenance 
of the RedCap database.

Please run 
	php redcapdbm.php -h 

to get a list of supported actions.

Background
====

From the "Other Functionality" page (ProjectSetup/other_functionality.php)
the admin can erase all data related to a project.

The click on "Erase all data" button creates an ajax request with the following format:
   
   $.get(app_path_webroot+'ProjectGeneral/erase_project_data.php', { pid: pid, action: 'erase_data' }


The code executed is a series of delete queries
   $q5 = mysql_query("update redcap_edocs_metadata set delete_date = '".NOW."' where project_id = $project_id and doc_id in ($fileFieldEdocIds)");
   // Delete project data
   $q1 = mysql_query("delete from redcap_data where project_id = $project_id");
   // Delete calendar events
   $q2 = mysql_query("delete from redcap_events_calendar where project_id = $project_id");
   // Delete logged events (only delete data-related logs?)
   $q3 = mysql_query("delete from redcap_log_event where project_id = $project_id and event in ('UPDATE', 'INSERT', 'DELETE', 'DATA_EXPORT', 'DOC_UPLOAD', 'DOC_DELETE', 'OTHER')");
   // Delete docs
   $q4 = mysql_query("delete from redcap_docs where project_id = $project_id");
   // Delete locking data
   $q6 = mysql_query("delete from redcap_locking_data where project_id = $project_id");
   // Delete esignatures
   $q10 = mysql_query("delete from redcap_esignatures where project_id = $project_id");
   // Delete survey-related info (response tracking, emails, participants) but not actual survey structure
   //$q7 = mysql_query("delete from redcap_surveys_participants where survey_id in (0, $survey_ids)");

   $q8 = mysql_query("delete from redcap_surveys_emails where survey_id in (0, $survey_ids)");
   $q9 = mysql_query("delete from redcap_surveys_response where participant_id in (0, $participant_ids)");


The helper functions `pre_query` and `log_event`
are defined in `Config/init_functions.php`


MySQL tables referencing the `project_id` column
================================================

select TABLE_SCHEMA, TABLE_NAME,COLUMN_NAME, DATA_TYPE from COLUMNS where COLUMN_NAME = 'project_id';
+--------------+----------------------------------------+-------------+-----------+
| TABLE_SCHEMA | TABLE_NAME                             | COLUMN_NAME | DATA_TYPE |
+--------------+----------------------------------------+-------------+-----------+
| redcap       | redcap_actions                         | project_id  | int       |
| redcap       | redcap_dashboard_concept_codes         | project_id  | int       |
| redcap       | redcap_data                            | project_id  | int       |
| redcap       | redcap_data_access_groups              | project_id  | int       |
| redcap       | redcap_data_quality_rules              | project_id  | int       |
| redcap       | redcap_data_quality_status             | project_id  | int       |
| redcap       | redcap_docs                            | project_id  | int       |
| redcap       | redcap_edocs_metadata                  | project_id  | int       |
| redcap       | redcap_esignatures                     | project_id  | int       |
| redcap       | redcap_events_arms                     | project_id  | int       |
| redcap       | redcap_events_calendar                 | project_id  | int       |
| redcap       | redcap_external_links                  | project_id  | int       |
| redcap       | redcap_external_links_exclude_projects | project_id  | int       |
| redcap       | redcap_library_map                     | project_id  | int       |
| redcap       | redcap_locking_data                    | project_id  | int       |
| redcap       | redcap_locking_labels                  | project_id  | int       |
| redcap       | redcap_log_event                       | project_id  | int       |
| redcap       | redcap_log_view                        | project_id  | int       |
| redcap       | redcap_metadata                        | project_id  | int       |
| redcap       | redcap_metadata_archive                | project_id  | int       |
| redcap       | redcap_metadata_prod_revisions         | project_id  | int       |
| redcap       | redcap_metadata_temp                   | project_id  | int       |
| redcap       | redcap_project_checklist               | project_id  | int       |
| redcap       | redcap_projects                        | project_id  | int       |
| redcap       | redcap_projects_external               | project_id  | varchar   |
| redcap       | redcap_pub_matches                     | project_id  | int       |
| redcap       | redcap_randomization                   | project_id  | int       |
| redcap       | redcap_standard_map                    | project_id  | int       |
| redcap       | redcap_standard_map_audit              | project_id  | int       |
| redcap       | redcap_surveys                         | project_id  | int       |
| redcap       | redcap_surveys_response_values         | project_id  | int       |
| redcap       | redcap_user_rights                     | project_id  | int       |
+--------------+----------------------------------------+-------------+-----------+


Testing scenario
========

- Before running script

+-----------------------------+----------+
| tableName                   | rowCount |
+-----------------------------+----------+
| redcap_projects             |        4 |
| redcap_data                 |       20 |
| redcap_events_calendar      |        0 |
| redcap_log_event            |       15 |
| redcap_docs                 |        0 |
| redcap_locking_data         |        0 |
| redcap_esignatures          |        0 |
| redcap_surveys              |        2 |
| redcap_surveys_participants |        1 |
| redcap_surveys_emails       |        0 |
| redcap_surveys_response     |        2 |
+-----------------------------+----------+

- After running script

total rows deleted: 32

+-----------------------------+----------+
| tableName                   | rowCount |
+-----------------------------+----------+
| redcap_projects             |        4 |
| redcap_data                 |        0 |
| redcap_events_calendar      |        0 |
| redcap_log_event            |        6 |
| redcap_docs                 |        0 |
| redcap_locking_data         |        0 |
| redcap_esignatures          |        0 |
| redcap_surveys              |        2 |
| redcap_surveys_participants |        0 |
| redcap_surveys_emails       |        0 |
| redcap_surveys_response     |        0 |
+-----------------------------+----------+

