/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
DROP TABLE IF EXISTS `redcap_actions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_actions` (
  `action_id` int(10) NOT NULL AUTO_INCREMENT,
  `project_id` int(10) DEFAULT NULL,
  `survey_id` int(10) DEFAULT NULL,
  `action_trigger` enum('MANUAL','ENDOFSURVEY','SURVEYQUESTION') COLLATE utf8_unicode_ci DEFAULT NULL,
  `action_response` enum('NONE','EMAIL','STOPSURVEY','PROMPT') COLLATE utf8_unicode_ci DEFAULT NULL,
  `custom_text` text COLLATE utf8_unicode_ci,
  `recipient_id` int(10) DEFAULT NULL COMMENT 'FK user_information',
  PRIMARY KEY (`action_id`),
  UNIQUE KEY `survey_recipient_id` (`survey_id`,`recipient_id`),
  KEY `project_id` (`project_id`),
  KEY `recipient_id` (`recipient_id`),
  CONSTRAINT `redcap_actions_ibfk_3` FOREIGN KEY (`survey_id`) REFERENCES `redcap_surveys` (`survey_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `redcap_actions_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `redcap_projects` (`project_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `redcap_actions_ibfk_2` FOREIGN KEY (`recipient_id`) REFERENCES `redcap_user_information` (`ui_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_actions` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_actions` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_auth`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_auth` (
  `username` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `password` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'MD5 hash of user''s password',
  `temp_pwd` int(1) NOT NULL DEFAULT '0' COMMENT 'Flag to force user to re-enter password',
  `password_question` int(10) DEFAULT NULL COMMENT 'PK of question',
  `password_answer` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'MD5 hash of answer to password recovery question',
  `password_question_reminder` datetime DEFAULT NULL COMMENT 'When to prompt user to set up security question',
  PRIMARY KEY (`username`),
  KEY `password_question` (`password_question`),
  CONSTRAINT `redcap_auth_ibfk_1` FOREIGN KEY (`password_question`) REFERENCES `redcap_auth_questions` (`qid`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_auth` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_auth` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_auth_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_auth_history` (
  `username` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `password` varchar(50) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `timestamp` datetime DEFAULT NULL,
  KEY `username_password` (`username`,`password`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='Stores last 5 passwords';
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_auth_history` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_auth_history` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_auth_questions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_auth_questions` (
  `qid` int(10) NOT NULL AUTO_INCREMENT,
  `question` text COLLATE utf8_unicode_ci,
  PRIMARY KEY (`qid`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_auth_questions` DISABLE KEYS */;
INSERT INTO `redcap_auth_questions` VALUES (1,'What was your childhood nickname?'),(2,'In what city did you meet your spouse/significant other?'),(3,'What is the name of your favorite childhood friend?'),(4,'What street did you live on in third grade?'),(5,'What is your oldest sibling\'s birthday month and year? (e.g., January 1900)'),(6,'What is the middle name of your oldest child?'),(7,'What is your oldest sibling\'s middle name?'),(8,'What school did you attend for sixth grade?'),(9,'What was your childhood phone number including area code? (e.g., 000-000-0000)'),(10,'What is your oldest cousin\'s first and last name?'),(11,'What was the name of your first stuffed animal?'),(12,'In what city or town did your mother and father meet?'),(13,'Where were you when you had your first kiss?'),(14,'What is the first name of the boy or girl that you first kissed?'),(15,'What was the last name of your third grade teacher?'),(16,'In what city does your nearest sibling live?'),(17,'What is your oldest brother\'s birthday month and year? (e.g., January 1900)'),(18,'What is your maternal grandmother\'s maiden name?'),(19,'In what city or town was your first job?'),(20,'What is the name of the place your wedding reception was held?'),(21,'What is the name of a college you applied to but didn\'t attend?');
/*!40000 ALTER TABLE `redcap_auth_questions` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_config` (
  `field_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `value` text COLLATE utf8_unicode_ci,
  PRIMARY KEY (`field_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='Stores global settings';
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_config` DISABLE KEYS */;
INSERT INTO `redcap_config` VALUES ('allow_create_db_default','1'),('amazon_s3_bucket',''),('amazon_s3_key',''),('amazon_s3_secret',''),('api_enabled','1'),('auth_meth_global','none'),('auto_prod_changes','2'),('auto_report_stats','1'),('auto_report_stats_last_sent','2000-01-01'),('autologout_timer','30'),('certify_text_create',''),('certify_text_prod',''),('data_entry_trigger_enabled','1'),('display_nonauth_projects','1'),('display_project_logo_institution','0'),('display_today_now_button','1'),('doc_to_edoc_transfer_complete','1'),('dts_enabled_global','0'),('edoc_field_option_enabled','1'),('edoc_path',''),('edoc_storage_option','0'),('edoc_upload_max',''),('email_domain_whitelist',''),('enable_edit_prod_events','1'),('enable_edit_survey_response','1'),('enable_http_compression','1'),('enable_plotting','2'),('enable_plotting_survey_results','1'),('enable_projecttype_forms','1'),('enable_projecttype_singlesurvey','1'),('enable_projecttype_singlesurveyforms','1'),('enable_url_shortener','1'),('enable_user_whitelist','0'),('file_attachment_upload_max',''),('file_repository_enabled','1'),('file_repository_upload_max',''),('footer_links',''),('footer_text',''),('google_translate_enabled','0'),('googlemap_key',''),('grant_cite',''),('headerlogo',''),('helpfaq_custom_text',''),('homepage_contact',''),('homepage_contact_email',''),('homepage_custom_text',''),('homepage_grant_cite',''),('identifier_keywords','name, street, address, city, county, precinct, zip, postal, date, phone, fax, mail, ssn, social security, mrn, dob, dod, medical, record, id, age'),('institution',''),('language_global','English'),('login_autocomplete_disable','0'),('login_custom_text',''),('login_logo',''),('logout_fail_limit','5'),('logout_fail_window','15'),('my_profile_enable_edit','1'),('openid_provider_name',''),('openid_provider_url',''),('page_hit_threshold_per_minute','600'),('password_history_limit','0'),('password_recovery_custom_text',''),('password_reset_duration','0'),('project_contact_email',''),('project_contact_name',''),('project_contact_prod_changes_email',''),('project_contact_prod_changes_name',''),('project_language','English'),('proxy_hostname',''),('pub_matching_email_days','7'),('pub_matching_email_limit','3'),('pub_matching_email_subject',''),('pub_matching_email_text',''),('pub_matching_emails','0'),('pub_matching_enabled','0'),('pub_matching_institution','Vanderbilt\nMeharry'),('randomization_global','1'),('realtime_webservice_custom_text',''),('realtime_webservice_data_fetch_interval','24'),('realtime_webservice_display_info_project_setup','1'),('realtime_webservice_global_enabled','0'),('realtime_webservice_source_system_custom_name',''),('realtime_webservice_stop_fetch_inactivity_days','7'),('realtime_webservice_url_data',''),('realtime_webservice_url_metadata',''),('realtime_webservice_url_user_access',''),('realtime_webservice_user_rights_super_users_only','1'),('redcap_base_url',''),('redcap_base_url_display_error_on_mismatch','1'),('redcap_last_install_date','2014-09-16'),('redcap_version','5.7.4'),('sendit_enabled','1'),('sendit_upload_max',''),('shared_library_enabled','1'),('shibboleth_logout',''),('shibboleth_username_field','none'),('site_org_type',''),('superusers_only_create_project','0'),('superusers_only_move_to_prod','1'),('suspend_users_inactive_days','180'),('suspend_users_inactive_send_email','1'),('suspend_users_inactive_type',''),('system_offline','0'),('system_offline_message',''),('temp_files_last_delete','2014-09-17 14:49:59'),('user_access_dashboard_custom_notification',''),('user_access_dashboard_enable','1');
/*!40000 ALTER TABLE `redcap_config` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_crons`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_crons` (
  `cron_id` int(10) NOT NULL AUTO_INCREMENT,
  `cron_name` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Unique name for each job',
  `cron_description` text COLLATE utf8_unicode_ci,
  `cron_enabled` enum('ENABLED','DISABLED') COLLATE utf8_unicode_ci DEFAULT 'ENABLED',
  `cron_frequency` int(10) DEFAULT NULL COMMENT 'seconds',
  `cron_max_run_time` int(10) DEFAULT NULL COMMENT 'max # seconds a cron should run',
  `cron_instances_max` int(2) NOT NULL DEFAULT '1' COMMENT 'Number of instances that can run simultaneously',
  `cron_instances_current` int(2) NOT NULL DEFAULT '0' COMMENT 'Current number of instances running',
  `cron_last_run_start` datetime DEFAULT NULL,
  `cron_last_run_end` datetime DEFAULT NULL,
  `cron_times_failed` int(2) NOT NULL DEFAULT '0' COMMENT 'After X failures, set as Disabled',
  `cron_external_url` text COLLATE utf8_unicode_ci COMMENT 'URL to call for custom jobs not defined by REDCap',
  PRIMARY KEY (`cron_id`),
  UNIQUE KEY `cron_name` (`cron_name`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='List of all jobs to be run by universal cron job';
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_crons` DISABLE KEYS */;
INSERT INTO `redcap_crons` VALUES (1,'PubMed','Query the PubMed API to find publications associated with PIs in REDCap, and store publication attributes and PI/project info. Emails will then be sent to any PIs that have been found to have publications in PubMed, and (if applicable) will be asked to associate their publication to a REDCap project.','DISABLED',86400,7200,1,0,NULL,NULL,0,NULL),(2,'RemoveTempAndDeletedFiles','Delete all files from the REDCap temp directory, and delete all edoc and Send-It files marked for deletion.','ENABLED',120,600,1,0,NULL,NULL,0,NULL),(3,'ExpireSurveys','For any surveys where an expiration timestamp is set, if the timestamp <= NOW, then make the survey inactive.','ENABLED',120,600,1,0,NULL,NULL,0,NULL),(4,'SurveyInvitationEmailer','Mailer that sends any survey invitations that have been scheduled.','ENABLED',60,1800,5,0,NULL,NULL,0,NULL),(5,'DeleteProjects','Delete all projects that are scheduled for permanent deletion','ENABLED',300,1200,1,0,NULL,NULL,0,NULL),(6,'ClearIPCache','Clear all IP addresses older than X minutes from the redcap_ip_cache table.','ENABLED',180,60,1,0,NULL,NULL,0,NULL),(7,'ExpireUsers','For any users whose expiration timestamp is set, if the timestamp <= NOW, then suspend the user\'s account and set expiration time back to NULL.','ENABLED',120,600,1,0,NULL,NULL,0,NULL),(8,'WarnUsersAccountExpiration','For any users whose expiration timestamp is set, if the expiration time is less than X days from now, then email the user to warn them of their impending account expiration.','ENABLED',86400,600,1,0,NULL,NULL,0,NULL),(9,'SuspendInactiveUsers','For any users whose last login time exceeds the defined max days of inactivity, auto-suspend their account (if setting enabled).','ENABLED',86400,600,1,0,NULL,NULL,0,NULL),(10,'ReminderUserAccessDashboard','At a regular interval, email all users to remind them to visit the User Access Dashboard page. Enables the ReminderUserAccessDashboardEmail cron job.','ENABLED',86400,600,1,0,NULL,NULL,0,NULL),(11,'ReminderUserAccessDashboardEmail','Email all users in batches to remind them to visit the User Access Dashboard page. Will disable itself when done.','DISABLED',60,1800,5,0,NULL,NULL,0,NULL),(12,'DDPQueueRecordsAllProjects','Queue records that are ready to be fetched from the external source system via the DDP service.','ENABLED',300,600,1,0,NULL,NULL,0,NULL),(13,'DDPFetchRecordsAllProjects','Fetch data from the external source system for records already queued by the DDP service.','ENABLED',60,1800,10,0,NULL,NULL,0,NULL),(14,'PurgeCronHistory','Purges all rows from the crons history table that are older than one week.','ENABLED',86400,600,1,0,NULL,NULL,0,NULL);
/*!40000 ALTER TABLE `redcap_crons` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_crons_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_crons_history` (
  `ch_id` int(10) NOT NULL AUTO_INCREMENT,
  `cron_id` int(10) DEFAULT NULL,
  `cron_run_start` datetime DEFAULT NULL,
  `cron_run_end` datetime DEFAULT NULL,
  `cron_run_status` enum('PROCESSING','COMPLETED','FAILED') COLLATE utf8_unicode_ci DEFAULT NULL,
  `cron_info` text COLLATE utf8_unicode_ci COMMENT 'Any pertinent info that might be logged',
  PRIMARY KEY (`ch_id`),
  KEY `cron_id` (`cron_id`),
  KEY `cron_run_start` (`cron_run_start`),
  KEY `cron_run_end` (`cron_run_end`),
  CONSTRAINT `redcap_crons_history_ibfk_1` FOREIGN KEY (`cron_id`) REFERENCES `redcap_crons` (`cron_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='History of all jobs run by universal cron job';
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_crons_history` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_crons_history` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_dashboard_ip_location_cache`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_dashboard_ip_location_cache` (
  `ip` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `latitude` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `longitude` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `city` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `region` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `country` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`ip`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_dashboard_ip_location_cache` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_dashboard_ip_location_cache` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_data` (
  `project_id` int(10) NOT NULL DEFAULT '0',
  `event_id` int(10) DEFAULT NULL,
  `record` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `field_name` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `value` text COLLATE utf8_unicode_ci,
  KEY `event_id` (`event_id`),
  KEY `project_field` (`project_id`,`field_name`),
  KEY `proj_record_field` (`project_id`,`record`,`field_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_data` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_data_access_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_data_access_groups` (
  `group_id` int(10) NOT NULL AUTO_INCREMENT,
  `project_id` int(10) DEFAULT NULL,
  `group_name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`group_id`),
  KEY `project_id` (`project_id`),
  CONSTRAINT `redcap_data_access_groups_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `redcap_projects` (`project_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_data_access_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_data_access_groups` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_data_quality_resolutions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_data_quality_resolutions` (
  `res_id` int(10) NOT NULL AUTO_INCREMENT,
  `status_id` int(10) DEFAULT NULL COMMENT 'FK from data_quality_status',
  `ts` datetime DEFAULT NULL COMMENT 'Date/time added',
  `user_id` int(10) DEFAULT NULL COMMENT 'Current user',
  `response_requested` int(1) NOT NULL DEFAULT '0' COMMENT 'Is a response requested?',
  `response` enum('DATA_MISSING','TYPOGRAPHICAL_ERROR','CONFIRMED_CORRECT','WRONG_SOURCE','OTHER') COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Response category if user responded to query',
  `comment` text COLLATE utf8_unicode_ci COMMENT 'Text for comment',
  `current_query_status` enum('OPEN','CLOSED','VERIFIED','DEVERIFIED') COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Current query status of thread',
  `upload_doc_id` int(10) DEFAULT NULL COMMENT 'FK of uploaded document',
  PRIMARY KEY (`res_id`),
  KEY `doc_id` (`upload_doc_id`),
  KEY `status_id` (`status_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `redcap_data_quality_resolutions_ibfk_1` FOREIGN KEY (`status_id`) REFERENCES `redcap_data_quality_status` (`status_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `redcap_data_quality_resolutions_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `redcap_user_information` (`ui_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `redcap_data_quality_resolutions_ibfk_3` FOREIGN KEY (`upload_doc_id`) REFERENCES `redcap_edocs_metadata` (`doc_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_data_quality_resolutions` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_data_quality_resolutions` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_data_quality_rules`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_data_quality_rules` (
  `rule_id` int(10) NOT NULL AUTO_INCREMENT,
  `project_id` int(10) DEFAULT NULL,
  `rule_order` int(3) DEFAULT '1',
  `rule_name` text COLLATE utf8_unicode_ci,
  `rule_logic` text COLLATE utf8_unicode_ci,
  `real_time_execute` int(1) NOT NULL DEFAULT '0' COMMENT 'Run in real-time on data entry forms?',
  PRIMARY KEY (`rule_id`),
  KEY `project_id` (`project_id`),
  CONSTRAINT `redcap_data_quality_rules_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `redcap_projects` (`project_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_data_quality_rules` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_data_quality_rules` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_data_quality_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_data_quality_status` (
  `status_id` int(10) NOT NULL AUTO_INCREMENT,
  `rule_id` int(10) DEFAULT NULL COMMENT 'FK from data_quality_rules table',
  `pd_rule_id` int(2) DEFAULT NULL COMMENT 'Name of pre-defined rules',
  `non_rule` int(1) DEFAULT NULL COMMENT '1 for non-rule, else NULL',
  `project_id` int(11) DEFAULT NULL,
  `record` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `event_id` int(10) DEFAULT NULL,
  `field_name` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Only used if field-level is required',
  `status` int(2) DEFAULT NULL COMMENT 'Current status of discrepancy',
  `exclude` int(1) NOT NULL DEFAULT '0' COMMENT 'Hide from results',
  `query_status` enum('OPEN','CLOSED','VERIFIED','DEVERIFIED') COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Status of data query',
  `assigned_user_id` int(10) DEFAULT NULL COMMENT 'UI ID of user assigned to query',
  PRIMARY KEY (`status_id`),
  UNIQUE KEY `rule_record_event` (`rule_id`,`record`,`event_id`),
  UNIQUE KEY `pd_rule_proj_record_event_field` (`pd_rule_id`,`record`,`event_id`,`field_name`,`project_id`),
  UNIQUE KEY `nonrule_proj_record_event_field` (`non_rule`,`project_id`,`record`,`event_id`,`field_name`),
  KEY `event_id` (`event_id`),
  KEY `pd_rule_proj_record_event` (`pd_rule_id`,`record`,`event_id`,`project_id`),
  KEY `project_query_status` (`project_id`,`query_status`),
  KEY `assigned_user_id` (`assigned_user_id`),
  CONSTRAINT `redcap_data_quality_status_ibfk_4` FOREIGN KEY (`assigned_user_id`) REFERENCES `redcap_user_information` (`ui_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `redcap_data_quality_status_ibfk_1` FOREIGN KEY (`rule_id`) REFERENCES `redcap_data_quality_rules` (`rule_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `redcap_data_quality_status_ibfk_2` FOREIGN KEY (`event_id`) REFERENCES `redcap_events_metadata` (`event_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `redcap_data_quality_status_ibfk_3` FOREIGN KEY (`project_id`) REFERENCES `redcap_projects` (`project_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_data_quality_status` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_data_quality_status` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_ddp_log_view`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_ddp_log_view` (
  `ml_id` int(10) NOT NULL AUTO_INCREMENT,
  `time_viewed` datetime DEFAULT NULL COMMENT 'Time the data was displayed to the user',
  `user_id` int(10) DEFAULT NULL COMMENT 'PK from user_information table',
  `project_id` int(10) DEFAULT NULL,
  `source_id` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'ID value from source system (e.g. MRN)',
  PRIMARY KEY (`ml_id`),
  KEY `source_id` (`source_id`),
  KEY `project_id` (`project_id`),
  KEY `user_project` (`user_id`,`project_id`),
  KEY `time_viewed` (`time_viewed`),
  CONSTRAINT `redcap_ddp_log_view_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `redcap_projects` (`project_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `redcap_ddp_log_view_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `redcap_user_information` (`ui_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_ddp_log_view` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_ddp_log_view` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_ddp_log_view_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_ddp_log_view_data` (
  `ml_id` int(10) DEFAULT NULL COMMENT 'PK from ddp_log_view table',
  `source_field` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Field name from source system',
  `source_timestamp` datetime DEFAULT NULL COMMENT 'Date of service from source system',
  `md_id` int(10) DEFAULT NULL COMMENT 'PK from ddp_records_data table',
  KEY `ml_id` (`ml_id`),
  KEY `source_timestamp` (`source_timestamp`),
  KEY `md_id` (`md_id`),
  KEY `source_field` (`source_field`),
  CONSTRAINT `redcap_ddp_log_view_data_ibfk_1` FOREIGN KEY (`ml_id`) REFERENCES `redcap_ddp_log_view` (`ml_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `redcap_ddp_log_view_data_ibfk_2` FOREIGN KEY (`md_id`) REFERENCES `redcap_ddp_records_data` (`md_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_ddp_log_view_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_ddp_log_view_data` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_ddp_mapping`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_ddp_mapping` (
  `map_id` int(10) NOT NULL AUTO_INCREMENT,
  `external_source_field_name` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Unique name of field mapped from external data source',
  `is_record_identifier` int(1) DEFAULT NULL COMMENT '1=Yes, Null=No',
  `project_id` int(10) DEFAULT NULL,
  `event_id` int(10) DEFAULT NULL,
  `field_name` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `temporal_field` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'REDCap date field',
  `preselect` enum('MIN','MAX','FIRST','LAST') COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Preselect a source value for temporal fields only',
  PRIMARY KEY (`map_id`),
  UNIQUE KEY `project_identifier` (`project_id`,`is_record_identifier`),
  UNIQUE KEY `project_field_event_source` (`project_id`,`event_id`,`field_name`,`external_source_field_name`),
  KEY `field_name` (`field_name`),
  KEY `event_id` (`event_id`),
  KEY `external_source_field_name` (`external_source_field_name`),
  KEY `temporal_field` (`temporal_field`),
  CONSTRAINT `redcap_ddp_mapping_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `redcap_projects` (`project_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `redcap_ddp_mapping_ibfk_2` FOREIGN KEY (`event_id`) REFERENCES `redcap_events_metadata` (`event_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_ddp_mapping` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_ddp_mapping` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_ddp_preview_fields`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_ddp_preview_fields` (
  `project_id` int(10) NOT NULL,
  `field1` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `field2` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `field3` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `field4` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `field5` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`project_id`),
  CONSTRAINT `redcap_ddp_preview_fields_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `redcap_projects` (`project_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_ddp_preview_fields` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_ddp_preview_fields` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_ddp_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_ddp_records` (
  `mr_id` int(10) NOT NULL AUTO_INCREMENT,
  `project_id` int(10) DEFAULT NULL,
  `record` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL COMMENT 'Time of last data fetch',
  `item_count` int(10) DEFAULT NULL COMMENT 'New item count (as of last viewing)',
  `fetch_status` enum('QUEUED','FETCHING') COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Current status of data fetch for this record',
  PRIMARY KEY (`mr_id`),
  UNIQUE KEY `project_record` (`project_id`,`record`),
  KEY `project_updated_at` (`updated_at`,`project_id`),
  KEY `project_id_fetch_status` (`fetch_status`,`project_id`),
  CONSTRAINT `redcap_ddp_records_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `redcap_projects` (`project_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_ddp_records` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_ddp_records` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_ddp_records_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_ddp_records_data` (
  `md_id` int(10) NOT NULL AUTO_INCREMENT,
  `map_id` int(10) NOT NULL COMMENT 'PK from ddp_mapping table',
  `mr_id` int(10) DEFAULT NULL COMMENT 'PK from ddp_records table',
  `source_timestamp` datetime DEFAULT NULL COMMENT 'Date of service from source system',
  `source_value` text COLLATE utf8_unicode_ci COMMENT 'Encrypted data value from source system',
  `adjudicated` int(1) NOT NULL DEFAULT '0' COMMENT 'Has source value been adjudicated?',
  `exclude` int(1) NOT NULL DEFAULT '0' COMMENT 'Has source value been excluded?',
  PRIMARY KEY (`md_id`),
  KEY `map_id_timestamp` (`map_id`,`source_timestamp`),
  KEY `map_id_mr_id_timestamp_value` (`map_id`,`mr_id`,`source_timestamp`,`source_value`(255)),
  KEY `mr_id_adjudicated` (`mr_id`,`adjudicated`),
  KEY `mr_id_exclude` (`mr_id`,`exclude`),
  CONSTRAINT `redcap_ddp_records_data_ibfk_1` FOREIGN KEY (`map_id`) REFERENCES `redcap_ddp_mapping` (`map_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `redcap_ddp_records_data_ibfk_2` FOREIGN KEY (`mr_id`) REFERENCES `redcap_ddp_records` (`mr_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='Cached data values from web service';
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_ddp_records_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_ddp_records_data` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_docs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_docs` (
  `docs_id` int(11) NOT NULL AUTO_INCREMENT,
  `project_id` int(10) NOT NULL DEFAULT '0',
  `docs_date` date DEFAULT NULL,
  `docs_name` text COLLATE utf8_unicode_ci,
  `docs_size` double DEFAULT NULL,
  `docs_type` text COLLATE utf8_unicode_ci,
  `docs_file` longblob,
  `docs_comment` text COLLATE utf8_unicode_ci,
  `docs_rights` text COLLATE utf8_unicode_ci,
  `export_file` int(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`docs_id`),
  KEY `docs_name` (`docs_name`(128)),
  KEY `project_id_export_file` (`project_id`,`export_file`),
  KEY `project_id_comment` (`project_id`,`docs_comment`(128)),
  CONSTRAINT `redcap_docs_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `redcap_projects` (`project_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_docs` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_docs` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_docs_to_edocs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_docs_to_edocs` (
  `docs_id` int(11) NOT NULL COMMENT 'PK redcap_docs',
  `doc_id` int(11) NOT NULL COMMENT 'PK redcap_edocs_metadata',
  PRIMARY KEY (`docs_id`,`doc_id`),
  KEY `doc_id` (`doc_id`),
  CONSTRAINT `redcap_docs_to_edocs_ibfk_2` FOREIGN KEY (`doc_id`) REFERENCES `redcap_edocs_metadata` (`doc_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `redcap_docs_to_edocs_ibfk_1` FOREIGN KEY (`docs_id`) REFERENCES `redcap_docs` (`docs_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_docs_to_edocs` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_docs_to_edocs` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_edocs_metadata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_edocs_metadata` (
  `doc_id` int(10) NOT NULL AUTO_INCREMENT,
  `stored_name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'stored name',
  `mime_type` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `doc_name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `doc_size` int(10) DEFAULT NULL,
  `file_extension` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `project_id` int(10) DEFAULT NULL,
  `stored_date` datetime DEFAULT NULL COMMENT 'stored date',
  `delete_date` datetime DEFAULT NULL COMMENT 'date deleted',
  `date_deleted_server` datetime DEFAULT NULL COMMENT 'When really deleted from server',
  PRIMARY KEY (`doc_id`),
  KEY `project_id` (`project_id`),
  KEY `date_deleted` (`delete_date`,`date_deleted_server`),
  CONSTRAINT `redcap_edocs_metadata_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `redcap_projects` (`project_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_edocs_metadata` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_edocs_metadata` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_esignatures`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_esignatures` (
  `esign_id` int(11) NOT NULL AUTO_INCREMENT,
  `project_id` int(10) DEFAULT NULL,
  `record` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `event_id` int(10) DEFAULT NULL,
  `form_name` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `username` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`esign_id`),
  UNIQUE KEY `proj_rec_event_form` (`project_id`,`record`,`event_id`,`form_name`),
  KEY `username` (`username`),
  KEY `event_id` (`event_id`),
  CONSTRAINT `redcap_esignatures_ibfk_2` FOREIGN KEY (`event_id`) REFERENCES `redcap_events_metadata` (`event_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `redcap_esignatures_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `redcap_projects` (`project_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_esignatures` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_esignatures` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_events_arms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_events_arms` (
  `arm_id` int(10) NOT NULL AUTO_INCREMENT,
  `project_id` int(10) NOT NULL DEFAULT '0',
  `arm_num` int(2) NOT NULL DEFAULT '1',
  `arm_name` varchar(50) COLLATE utf8_unicode_ci NOT NULL DEFAULT 'Arm 1',
  PRIMARY KEY (`arm_id`),
  UNIQUE KEY `proj_arm_num` (`project_id`,`arm_num`),
  CONSTRAINT `redcap_events_arms_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `redcap_projects` (`project_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_events_arms` DISABLE KEYS */;
INSERT INTO `redcap_events_arms` VALUES (1,1,1,'Arm 1'),(2,2,1,'Drug A'),(3,2,2,'Drug B'),(4,3,1,'Arm 1'),(5,4,1,'Drug A'),(6,5,1,'Arm 1'),(7,6,1,'Arm 1'),(8,7,1,'Arm 1'),(9,8,1,'Arm 1'),(10,9,1,'Arm 1'),(11,10,1,'Arm 1'),(12,11,1,'Arm 1'),(13,12,1,'Arm 1');
/*!40000 ALTER TABLE `redcap_events_arms` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_events_calendar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_events_calendar` (
  `cal_id` int(10) NOT NULL AUTO_INCREMENT,
  `record` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `project_id` int(10) DEFAULT NULL,
  `event_id` int(10) DEFAULT NULL,
  `baseline_date` date DEFAULT NULL,
  `group_id` int(10) DEFAULT NULL,
  `event_date` date DEFAULT NULL,
  `event_time` varchar(5) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'HH:MM',
  `event_status` int(2) DEFAULT NULL COMMENT 'NULL=Ad Hoc, 0=Due Date, 1=Scheduled, 2=Confirmed, 3=Cancelled, 4=No Show',
  `note_type` int(2) DEFAULT NULL,
  `notes` text COLLATE utf8_unicode_ci,
  `extra_notes` text COLLATE utf8_unicode_ci,
  PRIMARY KEY (`cal_id`),
  KEY `project_date` (`project_id`,`event_date`),
  KEY `project_record` (`project_id`,`record`),
  KEY `event_id` (`event_id`),
  KEY `group_id` (`group_id`),
  CONSTRAINT `redcap_events_calendar_ibfk_3` FOREIGN KEY (`group_id`) REFERENCES `redcap_data_access_groups` (`group_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `redcap_events_calendar_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `redcap_projects` (`project_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `redcap_events_calendar_ibfk_2` FOREIGN KEY (`event_id`) REFERENCES `redcap_events_metadata` (`event_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='Calendar Data';
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_events_calendar` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_events_calendar` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_events_forms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_events_forms` (
  `event_id` int(10) NOT NULL DEFAULT '0',
  `form_name` varchar(100) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  UNIQUE KEY `event_form` (`event_id`,`form_name`),
  CONSTRAINT `redcap_events_forms_ibfk_1` FOREIGN KEY (`event_id`) REFERENCES `redcap_events_metadata` (`event_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_events_forms` DISABLE KEYS */;
INSERT INTO `redcap_events_forms` VALUES (2,'baseline_data'),(2,'contact_info'),(2,'demographics'),(3,'patient_morale_questionnaire'),(4,'patient_morale_questionnaire'),(4,'visit_blood_workup'),(4,'visit_lab_data'),(4,'visit_observed_behavior'),(5,'patient_morale_questionnaire'),(6,'patient_morale_questionnaire'),(6,'visit_blood_workup'),(6,'visit_lab_data'),(6,'visit_observed_behavior'),(7,'patient_morale_questionnaire'),(8,'patient_morale_questionnaire'),(8,'visit_blood_workup'),(8,'visit_lab_data'),(8,'visit_observed_behavior'),(9,'completion_data'),(9,'completion_project_questionnaire'),(9,'patient_morale_questionnaire'),(9,'visit_blood_workup'),(9,'visit_observed_behavior'),(10,'baseline_data'),(10,'contact_info'),(10,'demographics'),(11,'contact_info'),(12,'patient_morale_questionnaire'),(13,'patient_morale_questionnaire'),(13,'visit_blood_workup'),(13,'visit_lab_data'),(13,'visit_observed_behavior'),(14,'patient_morale_questionnaire'),(15,'patient_morale_questionnaire'),(15,'visit_blood_workup'),(15,'visit_lab_data'),(15,'visit_observed_behavior'),(16,'completion_data'),(16,'completion_project_questionnaire'),(16,'patient_morale_questionnaire'),(16,'visit_blood_workup'),(16,'visit_lab_data'),(16,'visit_observed_behavior'),(17,'contact_info'),(19,'baseline_data'),(19,'contact_info'),(19,'demographics'),(20,'patient_morale_questionnaire'),(21,'patient_morale_questionnaire'),(21,'visit_blood_workup'),(21,'visit_lab_data'),(21,'visit_observed_behavior'),(22,'patient_morale_questionnaire'),(23,'patient_morale_questionnaire'),(23,'visit_blood_workup'),(23,'visit_lab_data'),(23,'visit_observed_behavior'),(24,'patient_morale_questionnaire'),(25,'patient_morale_questionnaire'),(25,'visit_blood_workup'),(25,'visit_lab_data'),(25,'visit_observed_behavior'),(26,'completion_data'),(26,'completion_project_questionnaire'),(26,'patient_morale_questionnaire'),(26,'visit_blood_workup'),(26,'visit_observed_behavior'),(32,'participant_info_survey'),(32,'prescreening_survey'),(33,'participant_morale_questionnaire'),(34,'participant_morale_questionnaire'),(35,'participant_morale_questionnaire'),(36,'participant_morale_questionnaire'),(37,'completion_data'),(39,'cbc'),(39,'chemistry'),(39,'enrollment'),(40,'cbc'),(40,'chemistry'),(41,'cbc'),(41,'chemistry'),(42,'cbc'),(42,'chemistry'),(43,'cbc'),(43,'chemistry'),(44,'cbc'),(44,'chemistry'),(45,'cbc'),(45,'chemistry'),(46,'cbc'),(46,'chemistry'),(47,'cbc'),(47,'chemistry'),(48,'cbc'),(48,'chemistry'),(49,'cbc'),(49,'chemistry'),(50,'cbc'),(50,'chemistry'),(51,'cbc'),(51,'chemistry'),(52,'cbc'),(52,'chemistry'),(53,'cbc'),(53,'chemistry'),(54,'cbc'),(54,'chemistry'),(55,'cbc'),(55,'chemistry'),(56,'cbc'),(56,'chemistry'),(57,'cbc'),(57,'chemistry'),(58,'cbc'),(58,'chemistry'),(59,'cbc'),(59,'chemistry'),(60,'cbc'),(60,'chemistry'),(61,'cbc'),(61,'chemistry'),(62,'cbc'),(62,'chemistry'),(63,'cbc'),(63,'chemistry'),(64,'cbc'),(64,'chemistry'),(65,'cbc'),(65,'chemistry'),(66,'cbc'),(66,'chemistry'),(67,'cbc'),(67,'chemistry'),(68,'cbc'),(68,'chemistry');
/*!40000 ALTER TABLE `redcap_events_forms` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_events_metadata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_events_metadata` (
  `event_id` int(10) NOT NULL AUTO_INCREMENT,
  `arm_id` int(10) NOT NULL DEFAULT '0' COMMENT 'FK for events_arms',
  `day_offset` float NOT NULL DEFAULT '0' COMMENT 'Days from Start Date',
  `offset_min` float NOT NULL DEFAULT '0',
  `offset_max` float NOT NULL DEFAULT '0',
  `descrip` varchar(64) COLLATE utf8_unicode_ci NOT NULL DEFAULT 'Event 1' COMMENT 'Event Name',
  `external_id` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`event_id`),
  KEY `external_id` (`external_id`),
  KEY `arm_dayoffset_descrip` (`arm_id`,`day_offset`,`descrip`),
  KEY `day_offset` (`day_offset`),
  KEY `descrip` (`descrip`),
  CONSTRAINT `redcap_events_metadata_ibfk_1` FOREIGN KEY (`arm_id`) REFERENCES `redcap_events_arms` (`arm_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_events_metadata` DISABLE KEYS */;
INSERT INTO `redcap_events_metadata` VALUES (1,1,0,0,0,'Event 1',NULL),(2,2,0,0,0,'Enrollment',NULL),(3,2,1,0,0,'Dose 1',NULL),(4,2,3,0,0,'Visit 1',NULL),(5,2,8,0,0,'Dose 2',NULL),(6,2,10,0,0,'Visit 2',NULL),(7,2,15,0,0,'Dose 3',NULL),(8,2,17,0,0,'Visit 3',NULL),(9,2,30,0,0,'Final visit',NULL),(10,3,0,0,0,'Enrollment',NULL),(11,3,5,0,0,'Deadline to opt out of study',NULL),(12,3,7,0,0,'First dose',NULL),(13,3,10,2,2,'First visit',NULL),(14,3,13,0,0,'Second dose',NULL),(15,3,15,2,2,'Second visit',NULL),(16,3,20,2,2,'Final visit',NULL),(17,3,30,0,0,'Deadline to return feedback',NULL),(18,4,0,0,0,'Event 1',NULL),(19,5,0,0,0,'Enrollment',NULL),(20,5,1,0,0,'Dose 1',NULL),(21,5,3,0,0,'Visit 1',NULL),(22,5,8,0,0,'Dose 2',NULL),(23,5,10,0,0,'Visit 2',NULL),(24,5,15,0,0,'Dose 3',NULL),(25,5,17,0,0,'Visit 3',NULL),(26,5,30,0,0,'Final visit',NULL),(27,6,0,0,0,'Event 1',NULL),(28,7,0,0,0,'Event 1',NULL),(29,8,0,0,0,'Event 1',NULL),(30,9,0,0,0,'Event 1',NULL),(31,10,0,0,0,'Event 1',NULL),(32,11,0,0,0,'Initial Data',NULL),(33,11,1,0,0,'Week 1',NULL),(34,11,8,0,0,'Week 2',NULL),(35,11,15,0,0,'Week 3',NULL),(36,11,22,0,0,'Week 4',NULL),(37,11,30,0,0,'Final Data',NULL),(38,12,0,0,0,'Event 1',NULL),(39,13,0,0,0,'1',NULL),(40,13,1,0,0,'2',NULL),(41,13,2,0,0,'3',NULL),(42,13,3,0,0,'4',NULL),(43,13,4,0,0,'5',NULL),(44,13,5,0,0,'6',NULL),(45,13,6,0,0,'7',NULL),(46,13,7,0,0,'8',NULL),(47,13,8,0,0,'9',NULL),(48,13,9,0,0,'10',NULL),(49,13,10,0,0,'11',NULL),(50,13,11,0,0,'12',NULL),(51,13,12,0,0,'13',NULL),(52,13,13,0,0,'14',NULL),(53,13,14,0,0,'15',NULL),(54,13,15,0,0,'16',NULL),(55,13,16,0,0,'17',NULL),(56,13,17,0,0,'18',NULL),(57,13,18,0,0,'19',NULL),(58,13,19,0,0,'20',NULL),(59,13,20,0,0,'21',NULL),(60,13,21,0,0,'22',NULL),(61,13,22,0,0,'23',NULL),(62,13,23,0,0,'24',NULL),(63,13,24,0,0,'25',NULL),(64,13,25,0,0,'26',NULL),(65,13,26,0,0,'27',NULL),(66,13,27,0,0,'28',NULL),(67,13,28,0,0,'29',NULL),(68,13,29,0,0,'30',NULL);
/*!40000 ALTER TABLE `redcap_events_metadata` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_external_links`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_external_links` (
  `ext_id` int(10) NOT NULL AUTO_INCREMENT,
  `project_id` int(10) DEFAULT NULL,
  `link_order` int(5) NOT NULL DEFAULT '1',
  `link_url` text COLLATE utf8_unicode_ci,
  `link_label` text COLLATE utf8_unicode_ci,
  `open_new_window` int(10) NOT NULL DEFAULT '0',
  `link_type` enum('LINK','POST_AUTHKEY','REDCAP_PROJECT') COLLATE utf8_unicode_ci NOT NULL DEFAULT 'LINK',
  `user_access` enum('ALL','DAG','SELECTED') COLLATE utf8_unicode_ci NOT NULL DEFAULT 'ALL',
  `append_record_info` int(1) NOT NULL DEFAULT '0' COMMENT 'Append record and event to URL',
  `append_pid` int(1) NOT NULL DEFAULT '0' COMMENT 'Append project_id to URL',
  `link_to_project_id` int(10) DEFAULT NULL,
  PRIMARY KEY (`ext_id`),
  KEY `project_id` (`project_id`),
  KEY `link_to_project_id` (`link_to_project_id`),
  CONSTRAINT `redcap_external_links_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `redcap_projects` (`project_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `redcap_external_links_ibfk_2` FOREIGN KEY (`link_to_project_id`) REFERENCES `redcap_projects` (`project_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_external_links` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_external_links` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_external_links_dags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_external_links_dags` (
  `ext_id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(10) NOT NULL DEFAULT '0',
  PRIMARY KEY (`ext_id`,`group_id`),
  KEY `group_id` (`group_id`),
  CONSTRAINT `redcap_external_links_dags_ibfk_2` FOREIGN KEY (`group_id`) REFERENCES `redcap_data_access_groups` (`group_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `redcap_external_links_dags_ibfk_1` FOREIGN KEY (`ext_id`) REFERENCES `redcap_external_links` (`ext_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_external_links_dags` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_external_links_dags` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_external_links_exclude_projects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_external_links_exclude_projects` (
  `ext_id` int(11) NOT NULL AUTO_INCREMENT,
  `project_id` int(10) NOT NULL DEFAULT '0',
  PRIMARY KEY (`ext_id`,`project_id`),
  KEY `project_id` (`project_id`),
  CONSTRAINT `redcap_external_links_exclude_projects_ibfk_2` FOREIGN KEY (`project_id`) REFERENCES `redcap_projects` (`project_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `redcap_external_links_exclude_projects_ibfk_1` FOREIGN KEY (`ext_id`) REFERENCES `redcap_external_links` (`ext_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='Projects to exclude for global external links';
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_external_links_exclude_projects` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_external_links_exclude_projects` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_external_links_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_external_links_users` (
  `ext_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  PRIMARY KEY (`ext_id`,`username`),
  KEY `username` (`username`),
  CONSTRAINT `redcap_external_links_users_ibfk_1` FOREIGN KEY (`ext_id`) REFERENCES `redcap_external_links` (`ext_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_external_links_users` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_external_links_users` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_ip_banned`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_ip_banned` (
  `ip` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `time_of_ban` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`ip`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_ip_banned` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_ip_banned` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_ip_cache`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_ip_cache` (
  `ip_hash` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `timestamp` timestamp NULL DEFAULT NULL,
  KEY `timestamp` (`timestamp`),
  KEY `ip_hash` (`ip_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_ip_cache` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_ip_cache` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_library_map`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_library_map` (
  `project_id` int(10) NOT NULL DEFAULT '0',
  `form_name` varchar(100) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `type` int(11) NOT NULL DEFAULT '0' COMMENT '1 = Downloaded; 2 = Uploaded',
  `library_id` int(10) NOT NULL DEFAULT '0',
  `upload_timestamp` datetime DEFAULT NULL,
  `acknowledgement` text COLLATE utf8_unicode_ci,
  `acknowledgement_cache` datetime DEFAULT NULL,
  PRIMARY KEY (`project_id`,`form_name`,`type`,`library_id`),
  KEY `library_id` (`library_id`),
  KEY `form_name` (`form_name`),
  KEY `type` (`type`),
  CONSTRAINT `redcap_library_map_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `redcap_projects` (`project_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_library_map` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_library_map` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_locking_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_locking_data` (
  `ld_id` int(11) NOT NULL AUTO_INCREMENT,
  `project_id` int(10) DEFAULT NULL,
  `record` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `event_id` int(10) DEFAULT NULL,
  `form_name` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `username` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`ld_id`),
  UNIQUE KEY `proj_rec_event_form` (`project_id`,`record`,`event_id`,`form_name`),
  KEY `username` (`username`),
  KEY `event_id` (`event_id`),
  CONSTRAINT `redcap_locking_data_ibfk_2` FOREIGN KEY (`event_id`) REFERENCES `redcap_events_metadata` (`event_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `redcap_locking_data_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `redcap_projects` (`project_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_locking_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_locking_data` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_locking_labels`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_locking_labels` (
  `ll_id` int(11) NOT NULL AUTO_INCREMENT,
  `project_id` int(11) DEFAULT NULL,
  `form_name` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `label` text COLLATE utf8_unicode_ci,
  `display` int(1) NOT NULL DEFAULT '1',
  `display_esignature` int(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`ll_id`),
  UNIQUE KEY `project_form` (`project_id`,`form_name`),
  CONSTRAINT `redcap_locking_labels_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `redcap_projects` (`project_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_locking_labels` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_locking_labels` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_log_event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_log_event` (
  `log_event_id` int(11) NOT NULL AUTO_INCREMENT,
  `project_id` int(10) NOT NULL DEFAULT '0',
  `ts` bigint(14) DEFAULT NULL,
  `user` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ip` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `page` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `event` enum('UPDATE','INSERT','DELETE','SELECT','ERROR','LOGIN','LOGOUT','OTHER','DATA_EXPORT','DOC_UPLOAD','DOC_DELETE','MANAGE','LOCK_RECORD','ESIGNATURE') COLLATE utf8_unicode_ci DEFAULT NULL,
  `object_type` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  `sql_log` mediumtext COLLATE utf8_unicode_ci,
  `pk` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `event_id` int(10) DEFAULT NULL,
  `data_values` text COLLATE utf8_unicode_ci,
  `description` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `legacy` int(1) NOT NULL DEFAULT '0',
  `change_reason` text COLLATE utf8_unicode_ci,
  PRIMARY KEY (`log_event_id`),
  KEY `user` (`user`),
  KEY `user_project` (`project_id`,`user`),
  KEY `object_type` (`object_type`),
  KEY `ts` (`ts`),
  KEY `event_project` (`event`,`project_id`),
  KEY `description` (`description`),
  KEY `pk` (`pk`)
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_log_event` DISABLE KEYS */;
INSERT INTO `redcap_log_event` VALUES (48,12,20140917145144,'site_admin','10.0.2.2','Design/edit_field.php','MANAGE','redcap_metadata','insert into redcap_metadata values (12, \'cbc_taken_date\', NULL, \'cbc\', NULL, \'7\', NULL, NULL, \'text\', \'Date Taken\', NULL, NULL, \'date_ymd\', NULL, NULL, \'soft_typed\', NULL, \'1\', NULL, 0, NULL, NULL, NULL, NULL, NULL)','cbc_taken_date',NULL,'field_name = \'cbc_taken_date\'','Create project field',0,NULL),(49,12,20140917145215,'site_admin','10.0.2.2','Design/edit_field.php','MANAGE','redcap_metadata','insert into redcap_metadata values (12, \'chemistry_taken_date\', NULL, \'chemistry\', NULL, \'19\', NULL, NULL, \'text\', \'Date Taken\', NULL, NULL, \'date_ymd\', NULL, NULL, \'soft_typed\', NULL, \'1\', NULL, 0, NULL, NULL, NULL, NULL, NULL)','chemistry_taken_date',NULL,'field_name = \'chemistry_taken_date\'','Create project field',0,NULL);
/*!40000 ALTER TABLE `redcap_log_event` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_log_view`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_log_view` (
  `log_view_id` int(11) NOT NULL AUTO_INCREMENT,
  `ts` timestamp NULL DEFAULT NULL,
  `user` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `event` enum('LOGIN_SUCCESS','LOGIN_FAIL','LOGOUT','PAGE_VIEW') COLLATE utf8_unicode_ci DEFAULT NULL,
  `ip` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `browser_name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `browser_version` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `full_url` text COLLATE utf8_unicode_ci,
  `page` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `project_id` int(10) DEFAULT NULL,
  `event_id` int(10) DEFAULT NULL,
  `record` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `form_name` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `miscellaneous` text COLLATE utf8_unicode_ci,
  `session_id` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`log_view_id`),
  KEY `ts` (`ts`),
  KEY `ip` (`ip`),
  KEY `event` (`event`),
  KEY `browser_name` (`browser_name`),
  KEY `browser_version` (`browser_version`),
  KEY `page` (`page`),
  KEY `session_id` (`session_id`),
  KEY `user_project` (`user`,`project_id`),
  KEY `project_event_record` (`project_id`,`event_id`,`record`)
) ENGINE=InnoDB AUTO_INCREMENT=134 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_log_view` DISABLE KEYS */;
INSERT INTO `redcap_log_view` VALUES (1,'2014-09-16 15:30:25','site_admin','PAGE_VIEW','::1','unknown','unknown','http://localhost/redcap/','redcap/index.php',NULL,NULL,NULL,NULL,NULL,'n7n4bbgvbnv09urc5f6atpak26'),(2,'2014-09-16 15:31:53','site_admin','PAGE_VIEW','10.0.2.2','chrome','37.0','http://localhost:8998:8998/redcap/','redcap/index.php',NULL,NULL,NULL,NULL,NULL,'r1a1r2fb6o1vr50fmuivn7lia6'),(3,'2014-09-16 15:31:55','site_admin','PAGE_VIEW','10.0.2.2','chrome','37.0','http://localhost:8998:8998/redcap/index.php?action=create','redcap/index.php',NULL,NULL,NULL,NULL,NULL,'r1a1r2fb6o1vr50fmuivn7lia6'),(4,'2014-09-16 15:31:57','site_admin','PAGE_VIEW','10.0.2.2','chrome','37.0','http://localhost:8998:8998/redcap/index.php?action=myprojects','redcap/index.php',NULL,NULL,NULL,NULL,NULL,'r1a1r2fb6o1vr50fmuivn7lia6'),(5,'2014-09-16 15:32:06','site_admin','PAGE_VIEW','10.0.2.2','chrome','37.0','http://localhost:8998:8998/redcap/index.php?action=create','redcap/index.php',NULL,NULL,NULL,NULL,NULL,'r1a1r2fb6o1vr50fmuivn7lia6'),(6,'2014-09-16 15:32:31','site_admin','PAGE_VIEW','10.0.2.2','chrome','37.0','http://localhost:8998:8998/redcap/redcap_v5.7.4/ProjectGeneral/create_project.php','ProjectGeneral/create_project.php',NULL,NULL,NULL,NULL,NULL,'r1a1r2fb6o1vr50fmuivn7lia6'),(93,'2014-09-16 15:52:29','site_admin','PAGE_VIEW','10.0.2.2','chrome','37.0','http://localhost:8998:8998/redcap/redcap_v5.7.4/ControlCenter/user_api_tokens.php?action=createToken&api_username=site_admin&api_pid=12&goto_proj=1','ControlCenter/user_api_tokens.php',NULL,NULL,NULL,NULL,NULL,'r1a1r2fb6o1vr50fmuivn7lia6'),(94,'2014-09-16 15:52:29','site_admin','PAGE_VIEW','10.0.2.2','chrome','37.0','http://localhost:8998:8998/redcap/redcap_v5.7.4/ControlCenter/user_api_ajax.php?action=tokensByUser&username=','ControlCenter/user_api_ajax.php',NULL,NULL,NULL,NULL,NULL,'r1a1r2fb6o1vr50fmuivn7lia6'),(95,'2014-09-16 15:52:29','site_admin','PAGE_VIEW','10.0.2.2','chrome','37.0','http://localhost:8998:8998/redcap/redcap_v5.7.4/ControlCenter/user_api_ajax.php?action=tokensByProj&project_id=&controlCenterView=1','ControlCenter/user_api_ajax.php',NULL,NULL,NULL,NULL,NULL,'r1a1r2fb6o1vr50fmuivn7lia6'),(96,'2014-09-16 15:52:29','site_admin','PAGE_VIEW','10.0.2.2','chrome','37.0','http://localhost:8998:8998/redcap/redcap_v5.7.4/ControlCenter/user_api_ajax.php?action=getAPIRights&api_username=site_admin&api_pid=12','ControlCenter/user_api_ajax.php',NULL,NULL,NULL,NULL,NULL,'r1a1r2fb6o1vr50fmuivn7lia6'),(97,'2014-09-16 15:52:29','site_admin','PAGE_VIEW','10.0.2.2','chrome','37.0','http://localhost:8998:8998/redcap/redcap_v5.7.4/ControlCenter/user_api_ajax.php?action=getAPIDateForUserJS&username=','ControlCenter/user_api_ajax.php',NULL,NULL,NULL,NULL,NULL,'r1a1r2fb6o1vr50fmuivn7lia6'),(98,'2014-09-16 15:52:29','site_admin','PAGE_VIEW','10.0.2.2','chrome','37.0','http://localhost:8998:8998/redcap/redcap_v5.7.4/ControlCenter/user_api_ajax.php?action=getAPIDateForProjJS&project_id=','ControlCenter/user_api_ajax.php',NULL,NULL,NULL,NULL,NULL,'r1a1r2fb6o1vr50fmuivn7lia6'),(99,'2014-09-16 15:52:36','site_admin','PAGE_VIEW','10.0.2.2','chrome','37.0','http://localhost:8998:8998/redcap/redcap_v5.7.4/ControlCenter/user_api_ajax.php?action=createToken&api_username=site_admin&api_pid=12&api_export=1&api_import=1&api_send_email=0','ControlCenter/user_api_ajax.php',NULL,NULL,NULL,NULL,NULL,'r1a1r2fb6o1vr50fmuivn7lia6'),(100,'2014-09-16 15:52:36','site_admin','PAGE_VIEW','10.0.2.2','chrome','37.0','http://localhost:8998:8998/redcap/redcap_v5.7.4/ControlCenter/user_api_ajax.php?action=tokensByUser&username=','ControlCenter/user_api_ajax.php',NULL,NULL,NULL,NULL,NULL,'r1a1r2fb6o1vr50fmuivn7lia6'),(101,'2014-09-16 15:52:36','site_admin','PAGE_VIEW','10.0.2.2','chrome','37.0','http://localhost:8998:8998/redcap/redcap_v5.7.4/ControlCenter/user_api_ajax.php?action=tokensByProj&project_id=&controlCenterView=1','ControlCenter/user_api_ajax.php',NULL,NULL,NULL,NULL,NULL,'r1a1r2fb6o1vr50fmuivn7lia6'),(102,'2014-09-16 15:52:36','site_admin','PAGE_VIEW','10.0.2.2','chrome','37.0','http://localhost:8998:8998/redcap/redcap_v5.7.4/ControlCenter/user_api_ajax.php?action=getAPIDateForUserJS&username=','ControlCenter/user_api_ajax.php',NULL,NULL,NULL,NULL,NULL,'r1a1r2fb6o1vr50fmuivn7lia6'),(103,'2014-09-16 15:52:36','site_admin','PAGE_VIEW','10.0.2.2','chrome','37.0','http://localhost:8998:8998/redcap/redcap_v5.7.4/ControlCenter/user_api_ajax.php?action=getAPIDateForProjJS&project_id=','ControlCenter/user_api_ajax.php',NULL,NULL,NULL,NULL,NULL,'r1a1r2fb6o1vr50fmuivn7lia6'),(106,'2014-09-16 15:53:20','site_admin','PAGE_VIEW','10.0.2.2','chrome','37.0','http://localhost:8998:8998/redcap/','redcap/index.php',NULL,NULL,NULL,NULL,NULL,'r1a1r2fb6o1vr50fmuivn7lia6'),(107,'2014-09-16 15:53:20','site_admin','PAGE_VIEW','10.0.2.2','chrome','37.0','http://localhost:8998:8998/redcap/','redcap/index.php',NULL,NULL,NULL,NULL,NULL,'r1a1r2fb6o1vr50fmuivn7lia6'),(108,'2014-09-16 15:53:25','site_admin','PAGE_VIEW','10.0.2.2','chrome','37.0','http://localhost:8998:8998/redcap/index.php?action=myprojects','redcap/index.php',NULL,NULL,NULL,NULL,NULL,'r1a1r2fb6o1vr50fmuivn7lia6'),(110,'2014-09-16 16:01:02','site_admin','PAGE_VIEW','10.0.2.2','chrome','37.0','http://localhost:8998:8998/redcap/index.php?action=myprojects','redcap/index.php',NULL,NULL,NULL,NULL,NULL,'r1a1r2fb6o1vr50fmuivn7lia6'),(111,'2014-09-16 16:01:05','site_admin','PAGE_VIEW','10.0.2.2','chrome','37.0','http://localhost:8998:8998/redcap/redcap_v5.7.4/ProjectSetup/index.php?pid=12','ProjectSetup/index.php',12,NULL,NULL,NULL,NULL,'r1a1r2fb6o1vr50fmuivn7lia6'),(112,'2014-09-17 14:17:42','site_admin','PAGE_VIEW','::1','unknown','unknown','http://localhost/redcap/','redcap/index.php',NULL,NULL,NULL,NULL,NULL,'2p95oelds6kukihcov2ihr1ps7'),(113,'2014-09-17 14:17:58','site_admin','PAGE_VIEW','10.0.2.2','chrome','37.0','http://localhost:8998:8998/redcap/','redcap/index.php',NULL,NULL,NULL,NULL,NULL,'csf61sns3hrvajppvf5pa9hvh5'),(114,'2014-09-17 14:18:01','site_admin','PAGE_VIEW','10.0.2.2','chrome','37.0','http://localhost:8998:8998/redcap/index.php?action=myprojects','redcap/index.php',NULL,NULL,NULL,NULL,NULL,'csf61sns3hrvajppvf5pa9hvh5'),(115,'2014-09-17 14:18:02','site_admin','PAGE_VIEW','10.0.2.2','chrome','37.0','http://localhost:8998:8998/redcap/redcap_v5.7.4/ProjectSetup/index.php?pid=12','ProjectSetup/index.php',12,NULL,NULL,NULL,NULL,'csf61sns3hrvajppvf5pa9hvh5'),(116,'2014-09-17 14:18:06','site_admin','PAGE_VIEW','10.0.2.2','chrome','37.0','http://localhost:8998:8998/redcap/redcap_v5.7.4/Design/online_designer.php?pid=12','Design/online_designer.php',12,NULL,NULL,NULL,NULL,'csf61sns3hrvajppvf5pa9hvh5'),(117,'2014-09-17 14:18:11','site_admin','PAGE_VIEW','10.0.2.2','chrome','37.0','http://localhost:8998:8998/redcap/redcap_v5.7.4/Design/online_designer.php?pid=12&page=cbc','Design/online_designer.php',12,NULL,NULL,NULL,NULL,'csf61sns3hrvajppvf5pa9hvh5'),(118,'2014-09-17 14:49:59','site_admin','PAGE_VIEW','10.0.2.2','chrome','37.0','http://localhost:8998:8998/redcap/redcap_v5.7.4/Design/check_field_name.php?pid=12&field_name=cbc&old_field_name=','Design/check_field_name.php',12,NULL,NULL,NULL,NULL,'csf61sns3hrvajppvf5pa9hvh5'),(119,'2014-09-17 14:51:00','site_admin','PAGE_VIEW','10.0.2.2','chrome','37.0','http://localhost:8998:8998/redcap/redcap_v5.7.4/Design/check_field_name.php?pid=12&field_name=cbc&old_field_name=','Design/check_field_name.php',12,NULL,NULL,NULL,NULL,'csf61sns3hrvajppvf5pa9hvh5'),(120,'2014-09-17 14:51:30','site_admin','PAGE_VIEW','10.0.2.2','chrome','37.0','http://localhost:8998:8998/redcap/redcap_v5.7.4/Design/check_field_name.php?pid=12&field_name=cbc_taken_date&old_field_name=','Design/check_field_name.php',12,NULL,NULL,NULL,NULL,'csf61sns3hrvajppvf5pa9hvh5'),(121,'2014-09-17 14:51:44','site_admin','PAGE_VIEW','10.0.2.2','chrome','37.0','http://localhost:8998:8998/redcap/redcap_v5.7.4/Design/check_field_name.php?pid=12&field_name=cbc_taken_date&old_field_name=','Design/check_field_name.php',12,NULL,NULL,NULL,NULL,'csf61sns3hrvajppvf5pa9hvh5'),(122,'2014-09-17 14:51:44','site_admin','PAGE_VIEW','10.0.2.2','chrome','37.0','http://localhost:8998:8998/redcap/redcap_v5.7.4/Design/edit_field.php?pid=12&page=cbc','Design/edit_field.php',12,NULL,NULL,NULL,NULL,'csf61sns3hrvajppvf5pa9hvh5'),(123,'2014-09-17 14:51:44','site_admin','PAGE_VIEW','10.0.2.2','chrome','37.0','http://localhost:8998:8998/redcap/redcap_v5.7.4/Design/online_designer_render_fields.php?pid=12&page=cbc&field_name=cbc_taken_date&edit_question=0&section_header=0','Design/online_designer_render_fields.php',12,NULL,NULL,NULL,NULL,'csf61sns3hrvajppvf5pa9hvh5'),(124,'2014-09-17 14:51:51','site_admin','PAGE_VIEW','10.0.2.2','chrome','37.0','http://localhost:8998:8998/redcap/redcap_v5.7.4/Design/online_designer.php?pid=12','Design/online_designer.php',12,NULL,NULL,NULL,NULL,'csf61sns3hrvajppvf5pa9hvh5'),(125,'2014-09-17 14:51:53','site_admin','PAGE_VIEW','10.0.2.2','chrome','37.0','http://localhost:8998:8998/redcap/redcap_v5.7.4/Design/online_designer.php?pid=12&page=chemistry','Design/online_designer.php',12,NULL,NULL,NULL,NULL,'csf61sns3hrvajppvf5pa9hvh5'),(126,'2014-09-17 14:51:56','site_admin','PAGE_VIEW','10.0.2.2','chrome','37.0','http://localhost:8998:8998/redcap/redcap_v5.7.4/Design/online_designer.php?pid=12','Design/online_designer.php',12,NULL,NULL,NULL,NULL,'csf61sns3hrvajppvf5pa9hvh5'),(127,'2014-09-17 14:51:57','site_admin','PAGE_VIEW','10.0.2.2','chrome','37.0','http://localhost:8998:8998/redcap/redcap_v5.7.4/Design/online_designer.php?pid=12&page=chemistry','Design/online_designer.php',12,NULL,NULL,NULL,NULL,'csf61sns3hrvajppvf5pa9hvh5'),(128,'2014-09-17 14:52:08','site_admin','PAGE_VIEW','10.0.2.2','chrome','37.0','http://localhost:8998:8998/redcap/redcap_v5.7.4/Design/check_field_name.php?pid=12&field_name=chemistry_taken_date&old_field_name=','Design/check_field_name.php',12,NULL,NULL,NULL,NULL,'csf61sns3hrvajppvf5pa9hvh5'),(129,'2014-09-17 14:52:15','site_admin','PAGE_VIEW','10.0.2.2','chrome','37.0','http://localhost:8998:8998/redcap/redcap_v5.7.4/Design/check_field_name.php?pid=12&field_name=chemistry_taken_date&old_field_name=','Design/check_field_name.php',12,NULL,NULL,NULL,NULL,'csf61sns3hrvajppvf5pa9hvh5'),(130,'2014-09-17 14:52:15','site_admin','PAGE_VIEW','10.0.2.2','chrome','37.0','http://localhost:8998:8998/redcap/redcap_v5.7.4/Design/edit_field.php?pid=12&page=chemistry','Design/edit_field.php',12,NULL,NULL,NULL,NULL,'csf61sns3hrvajppvf5pa9hvh5'),(131,'2014-09-17 14:52:15','site_admin','PAGE_VIEW','10.0.2.2','chrome','37.0','http://localhost:8998:8998/redcap/redcap_v5.7.4/Design/online_designer_render_fields.php?pid=12&page=chemistry&field_name=chemistry_taken_date&edit_question=0&section_header=0','Design/online_designer_render_fields.php',12,NULL,NULL,NULL,NULL,'csf61sns3hrvajppvf5pa9hvh5'),(132,'2014-09-17 14:52:22','site_admin','PAGE_VIEW','10.0.2.2','chrome','37.0','http://localhost:8998:8998/redcap/redcap_v5.7.4/Design/edit_field_prefill.php?pid=12&field_name=chemistry_taken_date','Design/edit_field_prefill.php',12,NULL,NULL,NULL,NULL,'csf61sns3hrvajppvf5pa9hvh5'),(133,'2014-09-17 14:52:36','site_admin','PAGE_VIEW','10.0.2.2','chrome','37.0','http://localhost:8998:8998/redcap/redcap_v5.7.4/Design/online_designer.php?pid=12','Design/online_designer.php',12,NULL,NULL,NULL,NULL,'csf61sns3hrvajppvf5pa9hvh5');
/*!40000 ALTER TABLE `redcap_log_view` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_metadata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_metadata` (
  `project_id` int(10) NOT NULL DEFAULT '0',
  `field_name` varchar(100) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `field_phi` varchar(5) COLLATE utf8_unicode_ci DEFAULT NULL,
  `form_name` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `form_menu_description` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `field_order` float DEFAULT NULL,
  `field_units` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `element_preceding_header` mediumtext COLLATE utf8_unicode_ci,
  `element_type` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `element_label` mediumtext COLLATE utf8_unicode_ci,
  `element_enum` mediumtext COLLATE utf8_unicode_ci,
  `element_note` mediumtext COLLATE utf8_unicode_ci,
  `element_validation_type` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `element_validation_min` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `element_validation_max` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `element_validation_checktype` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `branching_logic` text COLLATE utf8_unicode_ci,
  `field_req` int(1) NOT NULL DEFAULT '0',
  `edoc_id` int(10) DEFAULT NULL COMMENT 'image/file attachment',
  `edoc_display_img` int(1) NOT NULL DEFAULT '0',
  `custom_alignment` enum('LH','LV','RH','RV') COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'RV = NULL = default',
  `stop_actions` text COLLATE utf8_unicode_ci,
  `question_num` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `grid_name` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Unique name of grid group',
  `misc` text COLLATE utf8_unicode_ci COMMENT 'Miscellaneous field attributes',
  PRIMARY KEY (`project_id`,`field_name`),
  KEY `project_id_form` (`project_id`,`form_name`),
  KEY `field_name` (`field_name`),
  KEY `project_id_fieldorder` (`project_id`,`field_order`),
  KEY `edoc_id` (`edoc_id`),
  CONSTRAINT `redcap_metadata_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `redcap_projects` (`project_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `redcap_metadata_ibfk_2` FOREIGN KEY (`edoc_id`) REFERENCES `redcap_edocs_metadata` (`doc_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_metadata` DISABLE KEYS */;
INSERT INTO `redcap_metadata` VALUES (1,'address','1','demographics',NULL,5,NULL,NULL,'textarea','Street, City, State, ZIP',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'admission_date_1',NULL,'month_1_data',NULL,56,NULL,NULL,'text','Date of hospital admission',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'admission_date_2',NULL,'month_2_data',NULL,76,NULL,NULL,'text','Date of hospital admission',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'admission_date_3',NULL,'month_3_data',NULL,104,NULL,NULL,'text','Date of hospital admission',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'aerobics',NULL,'demographics',NULL,15,NULL,NULL,'checkbox','Aerobics','0, Monday \\n 1, Tuesday \\n 2, Wednesday \\n 3, Thursday \\n 4, Friday',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,'weekly_schedule',NULL),(1,'age',NULL,'demographics',NULL,8.2,NULL,NULL,'calc','Age (years)','rounddown(datediff([dob],\'today\',\'y\'))',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'alb_1',NULL,'month_1_data',NULL,44,'g/dL',NULL,'text','Serum Albumin (g/dL)',NULL,NULL,'float','3','5','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'alb_2',NULL,'month_2_data',NULL,64,'g/dL',NULL,'text','Serum Albumin (g/dL)',NULL,NULL,'float','3','5','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'alb_3',NULL,'month_3_data',NULL,85,'g/dL',NULL,'text','Serum Albumin (g/dL)',NULL,NULL,'float','3','5','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'alb_b',NULL,'baseline_data',NULL,26,'g/dL',NULL,'text','Serum Albumin (g/dL)',NULL,NULL,'int','3','5','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'baseline_data_complete',NULL,'baseline_data',NULL,42,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'bmi',NULL,'demographics',NULL,21,'kilograms',NULL,'calc','BMI','round(([weight]*10000)/(([height])^(2)),1)',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'cause_death_1',NULL,'month_1_data',NULL,61,NULL,NULL,'select','What was the cause of death?','1, All-cause \\n 2, Cardiovascular',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'cause_death_2',NULL,'month_2_data',NULL,81,NULL,NULL,'select','What was the cause of death?','1, All-cause \\n 2, Cardiovascular',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'cause_death_3',NULL,'month_3_data',NULL,109,NULL,NULL,'select','What was the cause of death?','1, All-cause \\n 2, Cardiovascular',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'cause_hosp_1',NULL,'month_1_data',NULL,55,NULL,NULL,'select','What was the cause of hospitalization?','1, Vascular access related events \\n 2, CVD events \\n 3, Other',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'cause_hosp_2',NULL,'month_2_data',NULL,75,NULL,NULL,'select','What was the cause of hospitalization?','1, Vascular access related events \\n 2, CVD events \\n 3, Other',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'cause_hosp_3',NULL,'month_3_data',NULL,103,NULL,NULL,'select','What was the cause of hospitalization?','1, Vascular access related events \\n 2, CVD events \\n 3, Other',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'chol_1',NULL,'month_1_data',NULL,48,'mg/dL',NULL,'text','Cholesterol (mg/dL)',NULL,NULL,'float','100','300','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'chol_2',NULL,'month_2_data',NULL,68,'mg/dL',NULL,'text','Cholesterol (mg/dL)',NULL,NULL,'float','100','300','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'chol_3',NULL,'month_3_data',NULL,89,'mg/dL',NULL,'text','Cholesterol (mg/dL)',NULL,NULL,'float','100','300','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'chol_b',NULL,'baseline_data',NULL,30,'mg/dL',NULL,'text','Cholesterol (mg/dL)',NULL,NULL,'float','100','300','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'comments',NULL,'demographics',NULL,22,NULL,'General Comments','textarea','Comments',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'complete_study',NULL,'completion_data','Completion Data',111,NULL,'Study Completion Information','select','Has patient completed study?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'complete_study_date',NULL,'completion_data',NULL,114,NULL,NULL,'text','Date of study completion',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'completion_data_complete',NULL,'completion_data',NULL,116,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'compliance_1',NULL,'month_1_data',NULL,53,NULL,NULL,'select','How compliant was the patient in drinking the supplement?','0, 100 percent \\n 1, 99-75 percent \\n 2, 74-50 percent \\n 3, 49-25 percent \\n 4, 0-24 percent',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'compliance_2',NULL,'month_2_data',NULL,73,NULL,NULL,'select','How compliant was the patient in drinking the supplement?','0, 100 percent \\n 1, 99-75 percent \\n 2, 74-50 percent \\n 3, 49-25 percent \\n 4, 0-24 percent',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'compliance_3',NULL,'month_3_data',NULL,101,NULL,NULL,'select','How compliant was the patient in drinking the supplement?','0, 100 percent \\n 1, 99-75 percent \\n 2, 74-50 percent \\n 3, 49-25 percent \\n 4, 0-24 percent',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'creat_1',NULL,'month_1_data',NULL,46,'mg/dL',NULL,'text','Creatinine (mg/dL)',NULL,NULL,'float','0.5','20','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'creat_2',NULL,'month_2_data',NULL,66,'mg/dL',NULL,'text','Creatinine (mg/dL)',NULL,NULL,'float','0.5','20','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'creat_3',NULL,'month_3_data',NULL,87,'mg/dL',NULL,'text','Creatinine (mg/dL)',NULL,NULL,'float','0.5','20','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'creat_b',NULL,'baseline_data',NULL,28,'mg/dL',NULL,'text','Creatinine (mg/dL)',NULL,NULL,'float','0.5','20','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'date_blood_3',NULL,'month_3_data',NULL,84,NULL,NULL,'text','Date blood was drawn',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'date_blood_b',NULL,'baseline_data',NULL,25,NULL,NULL,'text','Date blood was drawn',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'date_death_1',NULL,'month_1_data',NULL,60,NULL,NULL,'text','Date of death',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'date_death_2',NULL,'month_2_data',NULL,80,NULL,NULL,'text','Date of death',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'date_death_3',NULL,'month_3_data',NULL,108,NULL,NULL,'text','Date of death',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'date_enrolled',NULL,'demographics',NULL,2,NULL,'Consent Information','text','Date subject signed consent',NULL,'YYYY-MM-DD','date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'date_supplement_dispensed',NULL,'baseline_data',NULL,41,NULL,NULL,'text','Date patient begins supplement',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'date_visit_1',NULL,'month_1_data','Month 1 Data',43,NULL,'Month 1','text','Date of Month 1 visit',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'date_visit_2',NULL,'month_2_data','Month 2 Data',63,NULL,'Month 2','text','Date of Month 2 visit',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'date_visit_3',NULL,'month_3_data','Month 3 Data',83,NULL,'Month 3','text','Date of Month 3 visit',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'date_visit_b',NULL,'baseline_data','Baseline Data',24,NULL,'Baseline Measurements','text','Date of baseline visit',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'death_1',NULL,'month_1_data',NULL,59,NULL,'Mortality Data','select','Has patient died since last visit?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'death_2',NULL,'month_2_data',NULL,79,NULL,'Mortality Data','select','Has patient died since last visit?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'death_3',NULL,'month_3_data',NULL,107,NULL,'Mortality Data','select','Has patient died since last visit?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'demographics_complete',NULL,'demographics',NULL,23,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'discharge_date_1',NULL,'month_1_data',NULL,57,NULL,NULL,'text','Date of hospital discharge',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'discharge_date_2',NULL,'month_2_data',NULL,77,NULL,NULL,'text','Date of hospital discharge',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'discharge_date_3',NULL,'month_3_data',NULL,105,NULL,NULL,'text','Date of hospital discharge',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'discharge_summary_1',NULL,'month_1_data',NULL,58,NULL,NULL,'select','Discharge summary in patients binder?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'discharge_summary_2',NULL,'month_2_data',NULL,78,NULL,NULL,'select','Discharge summary in patients binder?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'discharge_summary_3',NULL,'month_3_data',NULL,106,NULL,NULL,'select','Discharge summary in patients binder?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'dob','1','demographics',NULL,8.1,NULL,NULL,'text','Date of birth',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'drink',NULL,'demographics',NULL,17,NULL,NULL,'checkbox','Drink (Alcoholic Beverages)','0, Monday \\n 1, Tuesday \\n 2, Wednesday \\n 3, Thursday \\n 4, Friday',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,'weekly_schedule',NULL),(1,'drywt_1',NULL,'month_1_data',NULL,51,'kilograms',NULL,'text','Dry weight (kilograms)',NULL,NULL,'float','35','200','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'drywt_2',NULL,'month_2_data',NULL,71,'kilograms',NULL,'text','Dry weight (kilograms)',NULL,NULL,'float','35','200','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'drywt_3',NULL,'month_3_data',NULL,92,'kilograms',NULL,'text','Dry weight (kilograms)',NULL,NULL,'float','35','200','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'drywt_b',NULL,'baseline_data',NULL,33,'kilograms',NULL,'text','Dry weight (kilograms)',NULL,NULL,'float','35','200','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'eat',NULL,'demographics',NULL,16,NULL,NULL,'checkbox','Eat Out (Dinner/Lunch)','0, Monday \\n 1, Tuesday \\n 2, Wednesday \\n 3, Thursday \\n 4, Friday',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,'weekly_schedule',NULL),(1,'email','1','demographics',NULL,8,NULL,NULL,'text','E-mail',NULL,NULL,'email',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'ethnicity',NULL,'demographics',NULL,9,NULL,NULL,'radio','Ethnicity','0, Hispanic or Latino \\n 1, NOT Hispanic or Latino \\n 2, Unknown / Not Reported',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,'LH',NULL,NULL,NULL,NULL),(1,'first_name','1','demographics',NULL,3,NULL,'Contact Information','text','First Name',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'given_birth',NULL,'demographics',NULL,12,NULL,NULL,'yesno','Has the patient given birth before?',NULL,NULL,NULL,NULL,NULL,NULL,'[sex] = \"0\"',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'gym',NULL,'demographics',NULL,14,NULL,'Please provide the patient\'s weekly schedule for the activities below.','checkbox','Gym (Weight Training)','0, Monday \\n 1, Tuesday \\n 2, Wednesday \\n 3, Thursday \\n 4, Friday',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,'weekly_schedule',NULL),(1,'height',NULL,'demographics',NULL,19,'cm',NULL,'text','Height (cm)',NULL,NULL,'float','130','215','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'hospit_1',NULL,'month_1_data',NULL,54,NULL,'Hospitalization Data','select','Was patient hospitalized since last visit?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'hospit_2',NULL,'month_2_data',NULL,74,NULL,'Hospitalization Data','select','Was patient hospitalized since last visit?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'hospit_3',NULL,'month_3_data',NULL,102,NULL,'Hospitalization Data','select','Was patient hospitalized since last visit?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'kt_v_1',NULL,'month_1_data',NULL,50,NULL,NULL,'text','Kt/V',NULL,NULL,'float','0.9','3','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'kt_v_2',NULL,'month_2_data',NULL,70,NULL,NULL,'text','Kt/V',NULL,NULL,'float','0.9','3','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'kt_v_3',NULL,'month_3_data',NULL,91,NULL,NULL,'text','Kt/V',NULL,NULL,'float','0.9','3','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'kt_v_b',NULL,'baseline_data',NULL,32,NULL,NULL,'text','Kt/V',NULL,NULL,'float','0.9','3','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'last_name','1','demographics',NULL,4,NULL,NULL,'text','Last Name',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'meds',NULL,'demographics',NULL,17.3,NULL,NULL,'checkbox','Is patient taking any of the following medications? (check all that apply)','1, Lexapro \\n 2, Celexa \\n 3, Prozac \\n 4, Paxil \\n 5, Zoloft',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'month_1_data_complete',NULL,'month_1_data',NULL,62,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'month_2_data_complete',NULL,'month_2_data',NULL,82,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'month_3_data_complete',NULL,'month_3_data',NULL,110,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'no_show_1',NULL,'month_1_data',NULL,52,NULL,NULL,'text','Number of treatments missed',NULL,NULL,'float','0','7','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'no_show_2',NULL,'month_2_data',NULL,72,NULL,NULL,'text','Number of treatments missed',NULL,NULL,'float','0','7','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'no_show_3',NULL,'month_3_data',NULL,100,NULL,NULL,'text','Number of treatments missed',NULL,NULL,'float','0','7','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'npcr_1',NULL,'month_1_data',NULL,47,'g/kg/d',NULL,'text','Normalized Protein Catabolic Rate (g/kg/d)',NULL,NULL,'float','0.5','2','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'npcr_2',NULL,'month_2_data',NULL,67,'g/kg/d',NULL,'text','Normalized Protein Catabolic Rate (g/kg/d)',NULL,NULL,'float','0.5','2','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'npcr_3',NULL,'month_3_data',NULL,88,'g/kg/d',NULL,'text','Normalized Protein Catabolic Rate (g/kg/d)',NULL,NULL,'float','0.5','2','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'npcr_b',NULL,'baseline_data',NULL,29,'g/kg/d',NULL,'text','Normalized Protein Catabolic Rate (g/kg/d)',NULL,NULL,'float','0.5','2','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'num_children',NULL,'demographics',NULL,13,NULL,NULL,'text','How many times has the patient given birth?',NULL,NULL,'int','0',NULL,'soft_typed','[sex] = \"0\" and [given_birth] = \"1\"',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'patient_document',NULL,'demographics',NULL,2.1,NULL,NULL,'file','Upload the patient\'s consent form',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'plasma1_3',NULL,'month_3_data',NULL,93,NULL,NULL,'select','Collected Plasma 1?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'plasma1_b',NULL,'baseline_data',NULL,34,NULL,NULL,'select','Collected Plasma 1?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'plasma2_3',NULL,'month_3_data',NULL,94,NULL,NULL,'select','Collected Plasma 2?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'plasma2_b',NULL,'baseline_data',NULL,35,NULL,NULL,'select','Collected Plasma 2?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'plasma3_3',NULL,'month_3_data',NULL,95,NULL,NULL,'select','Collected Plasma 3?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'plasma3_b',NULL,'baseline_data',NULL,36,NULL,NULL,'select','Collected Plasma 3?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'prealb_1',NULL,'month_1_data',NULL,45,'mg/dL',NULL,'text','Serum Prealbumin (mg/dL)',NULL,NULL,'float','10','40','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'prealb_2',NULL,'month_2_data',NULL,65,'mg/dL',NULL,'text','Serum Prealbumin (mg/dL)',NULL,NULL,'float','10','40','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'prealb_3',NULL,'month_3_data',NULL,86,'mg/dL',NULL,'text','Serum Prealbumin (mg/dL)',NULL,NULL,'float','10','40','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'prealb_b',NULL,'baseline_data',NULL,27,'mg/dL',NULL,'text','Serum Prealbumin (mg/dL)',NULL,NULL,'float','10','40','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'race',NULL,'demographics',NULL,10,NULL,NULL,'select','Race','0, American Indian/Alaska Native \\n 1, Asian \\n 2, Native Hawaiian or Other Pacific Islander \\n 3, Black or African American \\n 4, White \\n 5, More Than One Race \\n 6, Unknown / Not Reported',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'serum1_3',NULL,'month_3_data',NULL,96,NULL,NULL,'select','Collected Serum 1?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'serum1_b',NULL,'baseline_data',NULL,37,NULL,NULL,'select','Collected Serum 1?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'serum2_3',NULL,'month_3_data',NULL,97,NULL,NULL,'select','Collected Serum 2?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'serum2_b',NULL,'baseline_data',NULL,38,NULL,NULL,'select','Collected Serum 2?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'serum3_3',NULL,'month_3_data',NULL,98,NULL,NULL,'select','Collected Serum 3?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'serum3_b',NULL,'baseline_data',NULL,39,NULL,NULL,'select','Collected Serum 3?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'sex',NULL,'demographics',NULL,11,NULL,NULL,'radio','Gender','0, Female \\n 1, Male',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'sga_3',NULL,'month_3_data',NULL,99,NULL,NULL,'text','Subject Global Assessment (score = 1-7)',NULL,NULL,'float','0.9','7.1','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'sga_b',NULL,'baseline_data',NULL,40,NULL,NULL,'text','Subject Global Assessment (score = 1-7)',NULL,NULL,'float','0.9','7.1','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'specify_mood',NULL,'demographics',NULL,17.1,NULL,'Other information','slider','Specify the patient\'s mood','Very sad | Indifferent | Very happy',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'study_comments',NULL,'completion_data',NULL,115,NULL,'General Comments','textarea','Comments',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'study_id',NULL,'demographics','Demographics',1,NULL,NULL,'text','Study ID',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'telephone_1','1','demographics',NULL,6,NULL,NULL,'text','Phone number',NULL,'Include Area Code','phone',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'transferrin_1',NULL,'month_1_data',NULL,49,'mg/dL',NULL,'text','Transferrin (mg/dL)',NULL,NULL,'float','100','300','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'transferrin_2',NULL,'month_2_data',NULL,69,'mg/dL',NULL,'text','Transferrin (mg/dL)',NULL,NULL,'float','100','300','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'transferrin_3',NULL,'month_3_data',NULL,90,'mg/dL',NULL,'text','Transferrin (mg/dL)',NULL,NULL,'float','100','300','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'transferrin_b',NULL,'baseline_data',NULL,31,'mg/dL',NULL,'text','Transferrin (mg/dL)',NULL,NULL,'float','100','300','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'weight',NULL,'demographics',NULL,20,'kilograms',NULL,'text','Weight (kilograms)',NULL,NULL,'int','35','200','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'withdraw_date',NULL,'completion_data',NULL,112,NULL,NULL,'text','Put a date if patient withdrew study',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(1,'withdraw_reason',NULL,'completion_data',NULL,113,NULL,NULL,'select','Reason patient withdrew from study','0, Non-compliance \\n 1, Did not wish to continue in study \\n 2, Could not tolerate the supplement \\n 3, Hospitalization \\n 4, Other',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'address','1','demographics',NULL,5,NULL,NULL,'textarea','Street, City, State, ZIP',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'aerobics',NULL,'demographics',NULL,15,NULL,NULL,'checkbox','Aerobics','0, Monday \\n 1, Tuesday \\n 2, Wednesday \\n 3, Thursday \\n 4, Friday',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,'weekly_schedule',NULL),(2,'age',NULL,'demographics',NULL,8.2,NULL,NULL,'calc','Age (years)','rounddown(datediff([dob],\'today\',\'y\'))',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'alb_4',NULL,'completion_data',NULL,80,NULL,NULL,'text','Serum Albumin (g/dL)',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'baseline_data_complete',NULL,'baseline_data',NULL,39,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'bmi',NULL,'demographics',NULL,21,'kilograms',NULL,'calc','BMI','round(([weight]*10000)/(([height])^(2)),1)',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'bmi2',NULL,'baseline_data',NULL,33,NULL,NULL,'calc','BMI','round(([weight2]*10000)/(([height2])^(2)),1)',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'chol_4',NULL,'completion_data',NULL,86,NULL,NULL,'text','Cholesterol (mg/dL)',NULL,NULL,'int',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'chol_b',NULL,'baseline_data',NULL,37,NULL,NULL,'text','Cholesterol (mg/dL)',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'comments',NULL,'demographics',NULL,22,NULL,'General Comments','textarea','Comments',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'complete_study',NULL,'completion_data',NULL,77,NULL,NULL,'select','Has patient completed study?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'completion_data_complete',NULL,'completion_data',NULL,88,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'completion_project_questionnaire_complete',NULL,'completion_project_questionnaire',NULL,102,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'contact_info_complete',NULL,'contact_info',NULL,30,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'cpq1',NULL,'completion_project_questionnaire','Completion Project Questionnaire',89,NULL,NULL,'text','Date of study completion',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'cpq10',NULL,'completion_project_questionnaire',NULL,98,NULL,NULL,'select','On average, how many pills did you take each day last week?','0, less than 5 \\n 1, 5-10 \\n 2, 6-15 \\n 3, over 15',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'cpq11',NULL,'completion_project_questionnaire',NULL,99,NULL,NULL,'select','Using the handout, which level of dependence do you feel you are currently at?','0, 0 \\n 1, 1 \\n 2, 2 \\n 3, 3 \\n 4, 4 \\n 5, 5',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'cpq12',NULL,'completion_project_questionnaire',NULL,100,NULL,NULL,'radio','Would you be willing to discuss your experiences with a psychiatrist?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'cpq13',NULL,'completion_project_questionnaire',NULL,101,NULL,NULL,'select','How open are you to further testing?','0, not open \\n 1, undecided \\n 2, very open',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'cpq2',NULL,'completion_project_questionnaire',NULL,90,NULL,NULL,'text','Transferrin (mg/dL)',NULL,NULL,'int',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'cpq3',NULL,'completion_project_questionnaire',NULL,91,NULL,NULL,'text','Kt/V',NULL,NULL,'int',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'cpq4',NULL,'completion_project_questionnaire',NULL,92,NULL,NULL,'text','Dry weight (kilograms)',NULL,NULL,'int',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'cpq5',NULL,'completion_project_questionnaire',NULL,93,NULL,NULL,'text','Number of treatments missed',NULL,NULL,'int',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'cpq6',NULL,'completion_project_questionnaire',NULL,94,NULL,NULL,'select','How compliant was the patient in drinking the supplement?','0, 100 percent \\n 1, 99-75 percent \\n 2, 74-50 percent \\n 3, 49-25 percent \\n 4, 0-24 percent',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'cpq7',NULL,'completion_project_questionnaire',NULL,95,NULL,NULL,'select','Was patient hospitalized since last visit?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'cpq8',NULL,'completion_project_questionnaire',NULL,96,NULL,NULL,'select','What was the cause of hospitalization?','1, Vascular access related events \\n 2, CVD events \\n 3, Other',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'cpq9',NULL,'completion_project_questionnaire',NULL,97,NULL,NULL,'text','Date of hospital admission',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'creat_4',NULL,'completion_data',NULL,82,NULL,NULL,'text','Creatinine (mg/dL)',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'creat_b',NULL,'baseline_data',NULL,35,NULL,NULL,'text','Creatinine (mg/dL)',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'date_enrolled',NULL,'demographics',NULL,2,NULL,'Consent Information','text','Date subject signed consent',NULL,'YYYY-MM-DD','date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'date_visit_4',NULL,'completion_data',NULL,79,NULL,NULL,'text','Date of last visit',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'demographics_complete',NULL,'demographics',NULL,23,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'dialysis_schedule_days',NULL,'contact_info',NULL,26,NULL,NULL,'text','Next of Kin Contact Name',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'dialysis_schedule_time',NULL,'contact_info',NULL,27,NULL,NULL,'textarea','Next of Kin Contact Address',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'dialysis_unit_name',NULL,'contact_info','Contact Info',24,NULL,NULL,'text','Emergency Contact Phone Number',NULL,'Include Area Code','phone',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'dialysis_unit_phone',NULL,'contact_info',NULL,25,NULL,NULL,'radio','Confirmed?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'discharge_date_4',NULL,'completion_data',NULL,83,NULL,NULL,'text','Date of hospital discharge',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'discharge_summary_4',NULL,'completion_data',NULL,84,NULL,NULL,'select','Discharge summary in patients binder?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'dob','1','demographics',NULL,8.1,NULL,NULL,'text','Date of birth',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'drink',NULL,'demographics',NULL,17,NULL,NULL,'checkbox','Drink (Alcoholic Beverages)','0, Monday \\n 1, Tuesday \\n 2, Wednesday \\n 3, Thursday \\n 4, Friday',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,'weekly_schedule',NULL),(2,'eat',NULL,'demographics',NULL,16,NULL,NULL,'checkbox','Eat Out (Dinner/Lunch)','0, Monday \\n 1, Tuesday \\n 2, Wednesday \\n 3, Thursday \\n 4, Friday',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,'weekly_schedule',NULL),(2,'email','1','demographics',NULL,8,NULL,NULL,'text','E-mail',NULL,NULL,'email',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'ethnicity',NULL,'demographics',NULL,9,NULL,NULL,'radio','Ethnicity','0, Hispanic or Latino \\n 1, NOT Hispanic or Latino \\n 2, Unknown / Not Reported',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,'LH',NULL,NULL,NULL,NULL),(2,'etiology_esrd',NULL,'contact_info',NULL,28,NULL,NULL,'text','Next of Kin Contact Phone Number',NULL,'Include Area Code','phone',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'first_name','1','demographics',NULL,3,NULL,'Contact Information','text','First Name',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'given_birth',NULL,'demographics',NULL,12,NULL,NULL,'yesno','Has the patient given birth before?',NULL,NULL,NULL,NULL,NULL,NULL,'[sex] = \"0\"',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'gym',NULL,'demographics',NULL,14,NULL,'Please provide the patient\'s weekly schedule for the activities below.','checkbox','Gym (Weight Training)','0, Monday \\n 1, Tuesday \\n 2, Wednesday \\n 3, Thursday \\n 4, Friday',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,'weekly_schedule',NULL),(2,'height',NULL,'demographics',NULL,19,'cm',NULL,'text','Height (cm)',NULL,NULL,'float','130','215','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'height2',NULL,'baseline_data','Baseline Data',31,NULL,NULL,'text','Height (cm)',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'last_name','1','demographics',NULL,4,NULL,NULL,'text','Last Name',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'meds',NULL,'demographics',NULL,17.3,NULL,NULL,'checkbox','Is patient taking any of the following medications? (check all that apply)','1, Lexapro \\n 2, Celexa \\n 3, Prozac \\n 4, Paxil \\n 5, Zoloft',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'npcr_4',NULL,'completion_data',NULL,85,NULL,NULL,'text','Normalized Protein Catabolic Rate (g/kg/d)',NULL,NULL,'int',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'npcr_b',NULL,'baseline_data',NULL,36,NULL,NULL,'text','Normalized Protein Catabolic Rate (g/kg/d)',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'num_children',NULL,'demographics',NULL,13,NULL,NULL,'text','How many times has the patient given birth?',NULL,NULL,'int','0',NULL,'soft_typed','[sex] = \"0\" and [given_birth] = \"1\"',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'patient_document',NULL,'demographics',NULL,2.1,NULL,NULL,'file','Upload the patient\'s consent form',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'patient_morale_questionnaire_complete',NULL,'patient_morale_questionnaire',NULL,50,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'pmq1',NULL,'patient_morale_questionnaire','Patient Morale Questionnaire',46,NULL,NULL,'select','On average, how many pills did you take each day last week?','0, less than 5 \\n 1, 5-10 \\n 2, 6-15 \\n 3, over 15',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'pmq2',NULL,'patient_morale_questionnaire',NULL,47,NULL,NULL,'select','Using the handout, which level of dependence do you feel you are currently at?','0, 0 \\n 1, 1 \\n 2, 2 \\n 3, 3 \\n 4, 4 \\n 5, 5',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'pmq3',NULL,'patient_morale_questionnaire',NULL,48,NULL,NULL,'radio','Would you be willing to discuss your experiences with a psychiatrist?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'pmq4',NULL,'patient_morale_questionnaire',NULL,49,NULL,NULL,'select','How open are you to further testing?','0, not open \\n 1, undecided \\n 2, very open',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'prealb_4',NULL,'completion_data',NULL,81,NULL,NULL,'text','Serum Prealbumin (mg/dL)',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'prealb_b',NULL,'baseline_data',NULL,34,NULL,NULL,'text','Serum Prealbumin (mg/dL)',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'race',NULL,'demographics',NULL,10,NULL,NULL,'select','Race','0, American Indian/Alaska Native \\n 1, Asian \\n 2, Native Hawaiian or Other Pacific Islander \\n 3, Black or African American \\n 4, White \\n 5, More Than One Race \\n 6, Unknown / Not Reported',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'sex',NULL,'demographics',NULL,11,NULL,NULL,'radio','Gender','0, Female \\n 1, Male',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'specify_mood',NULL,'demographics',NULL,17.1,NULL,'Other information','slider','Specify the patient\'s mood','Very sad | Indifferent | Very happy',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'study_comments',NULL,'completion_data','Completion Data',76,NULL,NULL,'textarea','Comments',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'study_id',NULL,'demographics','Demographics',1,NULL,NULL,'text','Study ID',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'subject_comments',NULL,'contact_info',NULL,29,NULL,NULL,'radio','Confirmed?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'telephone_1','1','demographics',NULL,6,NULL,NULL,'text','Phone number',NULL,'Include Area Code','phone',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'transferrin_b',NULL,'baseline_data',NULL,38,NULL,NULL,'text','Transferrin (mg/dL)',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'vbw1',NULL,'visit_blood_workup','Visit Blood Workup',51,NULL,NULL,'text','Serum Prealbumin (mg/dL)',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'vbw2',NULL,'visit_blood_workup',NULL,52,NULL,NULL,'text','Creatinine (mg/dL)',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'vbw3',NULL,'visit_blood_workup',NULL,53,NULL,NULL,'text','Normalized Protein Catabolic Rate (g/kg/d)',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'vbw4',NULL,'visit_blood_workup',NULL,54,NULL,NULL,'text','Cholesterol (mg/dL)',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'vbw5',NULL,'visit_blood_workup',NULL,55,NULL,NULL,'text','Transferrin (mg/dL)',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'vbw6',NULL,'visit_blood_workup',NULL,56,NULL,NULL,'radio','Blood draw shift?','0, AM \\n 1, PM',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'vbw7',NULL,'visit_blood_workup',NULL,57,NULL,NULL,'radio','Blood draw by','0, RN \\n 1, LPN \\n 2, nurse assistant \\n 3, doctor',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'vbw8',NULL,'visit_blood_workup',NULL,58,NULL,NULL,'select','Level of patient anxiety','0, not anxious \\n 1, undecided \\n 2, very anxious',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'vbw9',NULL,'visit_blood_workup',NULL,59,NULL,NULL,'select','Patient scheduled for future draws?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'visit_blood_workup_complete',NULL,'visit_blood_workup',NULL,60,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'visit_lab_data_complete',NULL,'visit_lab_data',NULL,45,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'visit_observed_behavior_complete',NULL,'visit_observed_behavior',NULL,75,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'vld1',NULL,'visit_lab_data','Visit Lab Data',40,NULL,NULL,'text','Serum Prealbumin (mg/dL)',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'vld2',NULL,'visit_lab_data',NULL,41,NULL,NULL,'text','Creatinine (mg/dL)',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'vld3',NULL,'visit_lab_data',NULL,42,NULL,NULL,'text','Normalized Protein Catabolic Rate (g/kg/d)',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'vld4',NULL,'visit_lab_data',NULL,43,NULL,NULL,'text','Cholesterol (mg/dL)',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'vld5',NULL,'visit_lab_data',NULL,44,NULL,NULL,'text','Transferrin (mg/dL)',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'vob1',NULL,'visit_observed_behavior','Visit Observed Behavior',61,NULL,'Was the patient...','radio','nervous?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'vob10',NULL,'visit_observed_behavior',NULL,70,NULL,NULL,'radio','scared?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'vob11',NULL,'visit_observed_behavior',NULL,71,NULL,NULL,'radio','fidgety?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'vob12',NULL,'visit_observed_behavior',NULL,72,NULL,NULL,'radio','crying?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'vob13',NULL,'visit_observed_behavior',NULL,73,NULL,NULL,'radio','screaming?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'vob14',NULL,'visit_observed_behavior',NULL,74,NULL,NULL,'textarea','other',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'vob2',NULL,'visit_observed_behavior',NULL,62,NULL,NULL,'radio','worried?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'vob3',NULL,'visit_observed_behavior',NULL,63,NULL,NULL,'radio','scared?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'vob4',NULL,'visit_observed_behavior',NULL,64,NULL,NULL,'radio','fidgety?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'vob5',NULL,'visit_observed_behavior',NULL,65,NULL,NULL,'radio','crying?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'vob6',NULL,'visit_observed_behavior',NULL,66,NULL,NULL,'radio','screaming?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'vob7',NULL,'visit_observed_behavior',NULL,67,NULL,NULL,'textarea','other',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'vob8',NULL,'visit_observed_behavior',NULL,68,NULL,'Were you...','radio','nervous?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'vob9',NULL,'visit_observed_behavior',NULL,69,NULL,NULL,'radio','worried?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'weight',NULL,'demographics',NULL,20,'kilograms',NULL,'text','Weight (kilograms)',NULL,NULL,'int','35','200','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'weight2',NULL,'baseline_data',NULL,32,NULL,NULL,'text','Weight (kilograms)',NULL,NULL,'int',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'withdraw_date',NULL,'completion_data',NULL,78,NULL,NULL,'text','Put a date if patient withdrew study',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(2,'withdraw_reason',NULL,'completion_data',NULL,87,NULL,NULL,'select','Reason patient withdrew from study','0, Non-compliance \\n 1, Did not wish to continue in study \\n 2, Could not tolerate the supplement \\n 3, Hospitalization \\n 4, Other',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(3,'aerobics',NULL,'survey',NULL,11.2,NULL,NULL,'checkbox','Aerobics','0, Monday \\n 1, Tuesday \\n 2, Wednesday \\n 3, Thursday \\n 4, Friday',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,'weekly_schedule',NULL),(3,'comment_box',NULL,'survey',NULL,15,NULL,NULL,'textarea','If you need the respondent to enter a large amount of text, you may use a NOTES BOX.<br><br>This question has also been set as a REQUIRED QUESTION, so the respondent cannot fully submit the survey until this question has been answered. ANY question type can be set to be required.',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,'LH',NULL,NULL,NULL,NULL),(3,'date_ymd',NULL,'survey',NULL,8,NULL,NULL,'text','DATE questions are also an option. If you click the calendar icon on the right, a pop-up calendar will appear, thus allowing the respondent to easily select a date. Or it can be simply typed in.',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(3,'descriptive',NULL,'survey',NULL,11,NULL,NULL,'descriptive','You may also use DESCRIPTIVE TEXT to provide informational text within a survey section. ',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(3,'drink',NULL,'survey',NULL,11.4,NULL,NULL,'checkbox','Drink (Alcoholic Beverages)','0, Monday \\n 1, Tuesday \\n 2, Wednesday \\n 3, Thursday \\n 4, Friday',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,'weekly_schedule',NULL),(3,'dropdown',NULL,'survey',NULL,3,NULL,NULL,'select','You may also set multiple choice questions as DROP-DOWN MENUs.','1, Choice One \\n 2, Choice Two \\n 3, Choice Three \\n 4, Etc.',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(3,'eat',NULL,'survey',NULL,11.3,NULL,NULL,'checkbox','Eat Out (Dinner/Lunch)','0, Monday \\n 1, Tuesday \\n 2, Wednesday \\n 3, Thursday \\n 4, Friday',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,'weekly_schedule',NULL),(3,'file',NULL,'survey',NULL,9,NULL,NULL,'file','The FILE UPLOAD question type allows respondents to upload any type of document to the survey that you may afterward download and open when viewing your survey results.',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(3,'gym',NULL,'survey',NULL,11.1,NULL,'Below is a matrix of checkbox fields. A matrix can also be displayed as radio button fields.','checkbox','Gym (Weight Training)','0, Monday \\n 1, Tuesday \\n 2, Wednesday \\n 3, Thursday \\n 4, Friday',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,'weekly_schedule',NULL),(3,'hidden_branch',NULL,'survey',NULL,13,NULL,NULL,'text','HIDDEN QUESTION: This question will only appear when you select the second option of the question immediately above.',NULL,NULL,NULL,'undefined','undefined','soft_typed','[radio_branch] = \"2\"',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(3,'ma',NULL,'survey',NULL,5,NULL,NULL,'checkbox','This type of multiple choice question, known as CHECKBOXES, allows for more than one answer choice to be selected, whereas radio buttons and drop-downs only allow for one choice.','1, Choice One \\n 2, Choice Two \\n 3, Choice Three \\n 4, Select as many as you like',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(3,'participant_id',NULL,'survey','Example Survey',1,NULL,NULL,'text','Participant ID',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(3,'radio',NULL,'survey',NULL,2,NULL,'Section 1 (This is a section header with descriptive text. It only provides informational text and is used to divide the survey into sections for organization. If the survey is set to be displayed as \"one section per page\", then these section headers will begin each new page of the survey.)','radio','You may create MULTIPLE CHOICE questions and set the answer choices for them. You can have as many answer choices as you need. This multiple choice question is rendered as RADIO buttons.','1, Choice One \\n 2, Choice Two \\n 3, Choice Three \\n 4, Etc.',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(3,'radio_branch',NULL,'survey',NULL,12,NULL,'ADVANCED FEATURES: The questions below will illustrate how some advanced survey features are used.','radio','BRANCHING LOGIC: The question immediately following this one is using branching logic, which means that the question will stay hidden until defined criteria are specified.\n\nFor example, the following question has been set NOT to appear until the respondent selects the second option to the right.  ','1, This option does nothing. \\n 2, Clicking this option will trigger the branching logic to reveal the next question. \\n 3, This option also does nothing.',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(3,'slider',NULL,'survey',NULL,10,NULL,NULL,'slider','A SLIDER is a question type that allows the respondent to choose an answer along a continuum. The respondent\'s answer is saved as an integer between 0 (far left) and 100 (far right) with a step of 1.','You can provide labels above the slider | Middle label | Right-hand label',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(3,'stop_actions',NULL,'survey',NULL,14,NULL,NULL,'checkbox','STOP ACTIONS may be used with any multiple choice question. Stop actions can be applied to any (or all) answer choices. When that answer choice is selected by a respondent, their survey responses are then saved, and the survey is immediately ended.\n\nThe third option to the right has a stop action.','1, This option does nothing. \\n 2, This option also does nothing. \\n 3, Click here to trigger the stop action and end the survey.',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,'3',NULL,NULL,NULL),(3,'survey_complete',NULL,'survey',NULL,16,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(3,'textbox',NULL,'survey',NULL,4,NULL,NULL,'text','This is a TEXT BOX, which allows respondents to enter a small amount of text. A Text Box can be validated, if needed, as a number, integer, phone number, email, or zipcode. If validated as a number or integer, you may also set the minimum and/or maximum allowable values.\n\nThis question has \"number\" validation set with a minimum of 1 and a maximum of 10. ',NULL,NULL,'float','1','10','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(3,'tf',NULL,'survey',NULL,7,NULL,NULL,'truefalse','And you can also create TRUE-FALSE questions.<br><br>This question has horizontal alignment.',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,'RH',NULL,NULL,NULL,NULL),(3,'yn',NULL,'survey',NULL,6,NULL,NULL,'yesno','You can create YES-NO questions.<br><br>This question has vertical alignment of choices on the right.',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'address','1','demographics',NULL,5,NULL,NULL,'textarea','Street, City, State, ZIP',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'aerobics',NULL,'demographics',NULL,15,NULL,NULL,'checkbox','Aerobics','0, Monday \\n 1, Tuesday \\n 2, Wednesday \\n 3, Thursday \\n 4, Friday',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,'weekly_schedule',NULL),(4,'age',NULL,'demographics',NULL,8.2,NULL,NULL,'calc','Age (years)','rounddown(datediff([dob],\'today\',\'y\'))',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'alb_4',NULL,'completion_data',NULL,80,NULL,NULL,'text','Serum Albumin (g/dL)',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'baseline_data_complete',NULL,'baseline_data',NULL,39,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'bmi',NULL,'demographics',NULL,21,'kilograms',NULL,'calc','BMI','round(([weight]*10000)/(([height])^(2)),1)',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'bmi2',NULL,'baseline_data',NULL,33,NULL,NULL,'calc','BMI','round(([weight2]*10000)/(([height2])^(2)),1)',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'chol_4',NULL,'completion_data',NULL,86,NULL,NULL,'text','Cholesterol (mg/dL)',NULL,NULL,'int',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'chol_b',NULL,'baseline_data',NULL,37,NULL,NULL,'text','Cholesterol (mg/dL)',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'comments',NULL,'demographics',NULL,22,NULL,'General Comments','textarea','Comments',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'complete_study',NULL,'completion_data',NULL,77,NULL,NULL,'select','Has patient completed study?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'completion_data_complete',NULL,'completion_data',NULL,88,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'completion_project_questionnaire_complete',NULL,'completion_project_questionnaire',NULL,102,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'contact_info_complete',NULL,'contact_info',NULL,30,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'cpq1',NULL,'completion_project_questionnaire','Completion Project Questionnaire',89,NULL,NULL,'text','Date of study completion',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'cpq10',NULL,'completion_project_questionnaire',NULL,98,NULL,NULL,'select','On average, how many pills did you take each day last week?','0, less than 5 \\n 1, 5-10 \\n 2, 6-15 \\n 3, over 15',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'cpq11',NULL,'completion_project_questionnaire',NULL,99,NULL,NULL,'select','Using the handout, which level of dependence do you feel you are currently at?','0, 0 \\n 1, 1 \\n 2, 2 \\n 3, 3 \\n 4, 4 \\n 5, 5',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'cpq12',NULL,'completion_project_questionnaire',NULL,100,NULL,NULL,'radio','Would you be willing to discuss your experiences with a psychiatrist?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'cpq13',NULL,'completion_project_questionnaire',NULL,101,NULL,NULL,'select','How open are you to further testing?','0, not open \\n 1, undecided \\n 2, very open',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'cpq2',NULL,'completion_project_questionnaire',NULL,90,NULL,NULL,'text','Transferrin (mg/dL)',NULL,NULL,'int',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'cpq3',NULL,'completion_project_questionnaire',NULL,91,NULL,NULL,'text','Kt/V',NULL,NULL,'int',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'cpq4',NULL,'completion_project_questionnaire',NULL,92,NULL,NULL,'text','Dry weight (kilograms)',NULL,NULL,'int',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'cpq5',NULL,'completion_project_questionnaire',NULL,93,NULL,NULL,'text','Number of treatments missed',NULL,NULL,'int',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'cpq6',NULL,'completion_project_questionnaire',NULL,94,NULL,NULL,'select','How compliant was the patient in drinking the supplement?','0, 100 percent \\n 1, 99-75 percent \\n 2, 74-50 percent \\n 3, 49-25 percent \\n 4, 0-24 percent',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'cpq7',NULL,'completion_project_questionnaire',NULL,95,NULL,NULL,'select','Was patient hospitalized since last visit?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'cpq8',NULL,'completion_project_questionnaire',NULL,96,NULL,NULL,'select','What was the cause of hospitalization?','1, Vascular access related events \\n 2, CVD events \\n 3, Other',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'cpq9',NULL,'completion_project_questionnaire',NULL,97,NULL,NULL,'text','Date of hospital admission',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'creat_4',NULL,'completion_data',NULL,82,NULL,NULL,'text','Creatinine (mg/dL)',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'creat_b',NULL,'baseline_data',NULL,35,NULL,NULL,'text','Creatinine (mg/dL)',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'date_enrolled',NULL,'demographics',NULL,2,NULL,'Consent Information','text','Date subject signed consent',NULL,'YYYY-MM-DD','date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'date_visit_4',NULL,'completion_data',NULL,79,NULL,NULL,'text','Date of last visit',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'demographics_complete',NULL,'demographics',NULL,23,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'dialysis_schedule_days',NULL,'contact_info',NULL,26,NULL,NULL,'text','Next of Kin Contact Name',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'dialysis_schedule_time',NULL,'contact_info',NULL,27,NULL,NULL,'textarea','Next of Kin Contact Address',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'dialysis_unit_name',NULL,'contact_info','Contact Info',24,NULL,NULL,'text','Emergency Contact Phone Number',NULL,'Include Area Code','phone',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'dialysis_unit_phone',NULL,'contact_info',NULL,25,NULL,NULL,'radio','Confirmed?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'discharge_date_4',NULL,'completion_data',NULL,83,NULL,NULL,'text','Date of hospital discharge',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'discharge_summary_4',NULL,'completion_data',NULL,84,NULL,NULL,'select','Discharge summary in patients binder?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'dob','1','demographics',NULL,8.1,NULL,NULL,'text','Date of birth',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'drink',NULL,'demographics',NULL,17,NULL,NULL,'checkbox','Drink (Alcoholic Beverages)','0, Monday \\n 1, Tuesday \\n 2, Wednesday \\n 3, Thursday \\n 4, Friday',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,'weekly_schedule',NULL),(4,'eat',NULL,'demographics',NULL,16,NULL,NULL,'checkbox','Eat Out (Dinner/Lunch)','0, Monday \\n 1, Tuesday \\n 2, Wednesday \\n 3, Thursday \\n 4, Friday',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,'weekly_schedule',NULL),(4,'email','1','demographics',NULL,8,NULL,NULL,'text','E-mail',NULL,NULL,'email',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'ethnicity',NULL,'demographics',NULL,9,NULL,NULL,'radio','Ethnicity','0, Hispanic or Latino \\n 1, NOT Hispanic or Latino \\n 2, Unknown / Not Reported',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,'LH',NULL,NULL,NULL,NULL),(4,'etiology_esrd',NULL,'contact_info',NULL,28,NULL,NULL,'text','Next of Kin Contact Phone Number',NULL,'Include Area Code','phone',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'first_name','1','demographics',NULL,3,NULL,'Contact Information','text','First Name',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'given_birth',NULL,'demographics',NULL,12,NULL,NULL,'yesno','Has the patient given birth before?',NULL,NULL,NULL,NULL,NULL,NULL,'[sex] = \"0\"',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'gym',NULL,'demographics',NULL,14,NULL,'Please provide the patient\'s weekly schedule for the activities below.','checkbox','Gym (Weight Training)','0, Monday \\n 1, Tuesday \\n 2, Wednesday \\n 3, Thursday \\n 4, Friday',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,'weekly_schedule',NULL),(4,'height',NULL,'demographics',NULL,19,'cm',NULL,'text','Height (cm)',NULL,NULL,'float','130','215','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'height2',NULL,'baseline_data','Baseline Data',31,NULL,NULL,'text','Height (cm)',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'last_name','1','demographics',NULL,4,NULL,NULL,'text','Last Name',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'meds',NULL,'demographics',NULL,17.3,NULL,NULL,'checkbox','Is patient taking any of the following medications? (check all that apply)','1, Lexapro \\n 2, Celexa \\n 3, Prozac \\n 4, Paxil \\n 5, Zoloft',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'npcr_4',NULL,'completion_data',NULL,85,NULL,NULL,'text','Normalized Protein Catabolic Rate (g/kg/d)',NULL,NULL,'int',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'npcr_b',NULL,'baseline_data',NULL,36,NULL,NULL,'text','Normalized Protein Catabolic Rate (g/kg/d)',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'num_children',NULL,'demographics',NULL,13,NULL,NULL,'text','How many times has the patient given birth?',NULL,NULL,'int','0',NULL,'soft_typed','[sex] = \"0\" and [given_birth] = \"1\"',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'patient_document',NULL,'demographics',NULL,2.1,NULL,NULL,'file','Upload the patient\'s consent form',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'patient_morale_questionnaire_complete',NULL,'patient_morale_questionnaire',NULL,50,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'pmq1',NULL,'patient_morale_questionnaire','Patient Morale Questionnaire',46,NULL,NULL,'select','On average, how many pills did you take each day last week?','0, less than 5 \\n 1, 5-10 \\n 2, 6-15 \\n 3, over 15',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'pmq2',NULL,'patient_morale_questionnaire',NULL,47,NULL,NULL,'select','Using the handout, which level of dependence do you feel you are currently at?','0, 0 \\n 1, 1 \\n 2, 2 \\n 3, 3 \\n 4, 4 \\n 5, 5',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'pmq3',NULL,'patient_morale_questionnaire',NULL,48,NULL,NULL,'radio','Would you be willing to discuss your experiences with a psychiatrist?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'pmq4',NULL,'patient_morale_questionnaire',NULL,49,NULL,NULL,'select','How open are you to further testing?','0, not open \\n 1, undecided \\n 2, very open',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'prealb_4',NULL,'completion_data',NULL,81,NULL,NULL,'text','Serum Prealbumin (mg/dL)',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'prealb_b',NULL,'baseline_data',NULL,34,NULL,NULL,'text','Serum Prealbumin (mg/dL)',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'race',NULL,'demographics',NULL,10,NULL,NULL,'select','Race','0, American Indian/Alaska Native \\n 1, Asian \\n 2, Native Hawaiian or Other Pacific Islander \\n 3, Black or African American \\n 4, White \\n 5, More Than One Race \\n 6, Unknown / Not Reported',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'sex',NULL,'demographics',NULL,11,NULL,NULL,'radio','Gender','0, Female \\n 1, Male',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'specify_mood',NULL,'demographics',NULL,17.1,NULL,'Other information','slider','Specify the patient\'s mood','Very sad | Indifferent | Very happy',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'study_comments',NULL,'completion_data','Completion Data',76,NULL,NULL,'textarea','Comments',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'study_id',NULL,'demographics','Demographics',1,NULL,NULL,'text','Study ID',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'subject_comments',NULL,'contact_info',NULL,29,NULL,NULL,'radio','Confirmed?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'telephone_1','1','demographics',NULL,6,NULL,NULL,'text','Phone number',NULL,'Include Area Code','phone',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'transferrin_b',NULL,'baseline_data',NULL,38,NULL,NULL,'text','Transferrin (mg/dL)',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'vbw1',NULL,'visit_blood_workup','Visit Blood Workup',51,NULL,NULL,'text','Serum Prealbumin (mg/dL)',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'vbw2',NULL,'visit_blood_workup',NULL,52,NULL,NULL,'text','Creatinine (mg/dL)',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'vbw3',NULL,'visit_blood_workup',NULL,53,NULL,NULL,'text','Normalized Protein Catabolic Rate (g/kg/d)',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'vbw4',NULL,'visit_blood_workup',NULL,54,NULL,NULL,'text','Cholesterol (mg/dL)',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'vbw5',NULL,'visit_blood_workup',NULL,55,NULL,NULL,'text','Transferrin (mg/dL)',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'vbw6',NULL,'visit_blood_workup',NULL,56,NULL,NULL,'radio','Blood draw shift?','0, AM \\n 1, PM',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'vbw7',NULL,'visit_blood_workup',NULL,57,NULL,NULL,'radio','Blood draw by','0, RN \\n 1, LPN \\n 2, nurse assistant \\n 3, doctor',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'vbw8',NULL,'visit_blood_workup',NULL,58,NULL,NULL,'select','Level of patient anxiety','0, not anxious \\n 1, undecided \\n 2, very anxious',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'vbw9',NULL,'visit_blood_workup',NULL,59,NULL,NULL,'select','Patient scheduled for future draws?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'visit_blood_workup_complete',NULL,'visit_blood_workup',NULL,60,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'visit_lab_data_complete',NULL,'visit_lab_data',NULL,45,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'visit_observed_behavior_complete',NULL,'visit_observed_behavior',NULL,75,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'vld1',NULL,'visit_lab_data','Visit Lab Data',40,NULL,NULL,'text','Serum Prealbumin (mg/dL)',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'vld2',NULL,'visit_lab_data',NULL,41,NULL,NULL,'text','Creatinine (mg/dL)',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'vld3',NULL,'visit_lab_data',NULL,42,NULL,NULL,'text','Normalized Protein Catabolic Rate (g/kg/d)',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'vld4',NULL,'visit_lab_data',NULL,43,NULL,NULL,'text','Cholesterol (mg/dL)',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'vld5',NULL,'visit_lab_data',NULL,44,NULL,NULL,'text','Transferrin (mg/dL)',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'vob1',NULL,'visit_observed_behavior','Visit Observed Behavior',61,NULL,'Was the patient...','radio','nervous?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'vob10',NULL,'visit_observed_behavior',NULL,70,NULL,NULL,'radio','scared?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'vob11',NULL,'visit_observed_behavior',NULL,71,NULL,NULL,'radio','fidgety?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'vob12',NULL,'visit_observed_behavior',NULL,72,NULL,NULL,'radio','crying?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'vob13',NULL,'visit_observed_behavior',NULL,73,NULL,NULL,'radio','screaming?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'vob14',NULL,'visit_observed_behavior',NULL,74,NULL,NULL,'textarea','other',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'vob2',NULL,'visit_observed_behavior',NULL,62,NULL,NULL,'radio','worried?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'vob3',NULL,'visit_observed_behavior',NULL,63,NULL,NULL,'radio','scared?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'vob4',NULL,'visit_observed_behavior',NULL,64,NULL,NULL,'radio','fidgety?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'vob5',NULL,'visit_observed_behavior',NULL,65,NULL,NULL,'radio','crying?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'vob6',NULL,'visit_observed_behavior',NULL,66,NULL,NULL,'radio','screaming?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'vob7',NULL,'visit_observed_behavior',NULL,67,NULL,NULL,'textarea','other',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'vob8',NULL,'visit_observed_behavior',NULL,68,NULL,'Were you...','radio','nervous?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'vob9',NULL,'visit_observed_behavior',NULL,69,NULL,NULL,'radio','worried?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'weight',NULL,'demographics',NULL,20,'kilograms',NULL,'text','Weight (kilograms)',NULL,NULL,'int','35','200','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'weight2',NULL,'baseline_data',NULL,32,NULL,NULL,'text','Weight (kilograms)',NULL,NULL,'int',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'withdraw_date',NULL,'completion_data',NULL,78,NULL,NULL,'text','Put a date if patient withdrew study',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'withdraw_reason',NULL,'completion_data',NULL,87,NULL,NULL,'select','Reason patient withdrew from study','0, Non-compliance \\n 1, Did not wish to continue in study \\n 2, Could not tolerate the supplement \\n 3, Hospitalization \\n 4, Other',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(5,'address','1','demographics',NULL,5,NULL,NULL,'textarea','Street, City, State, ZIP',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(5,'age',NULL,'demographics',NULL,8.2,NULL,NULL,'calc','Age (years)','rounddown(datediff([dob],\'today\',\'y\'))',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(5,'bmi',NULL,'demographics',NULL,21,'kilograms',NULL,'calc','BMI','round(([weight]*10000)/(([height])^(2)),1)',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(5,'comments',NULL,'demographics',NULL,22,NULL,'General Comments','textarea','Comments',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(5,'demographics_complete',NULL,'demographics',NULL,23,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(5,'dob','1','demographics',NULL,8.1,NULL,NULL,'text','Date of birth',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(5,'email','1','demographics',NULL,8,NULL,NULL,'text','E-mail',NULL,NULL,'email',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(5,'ethnicity',NULL,'demographics',NULL,9,NULL,NULL,'radio','Ethnicity','0, Hispanic or Latino \\n 1, NOT Hispanic or Latino \\n 2, Unknown / Not Reported',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,'LH',NULL,NULL,NULL,NULL),(5,'first_name','1','demographics',NULL,3,NULL,'Contact Information','text','First Name',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(5,'height',NULL,'demographics',NULL,19,'cm',NULL,'text','Height (cm)',NULL,NULL,'float','130','215','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(5,'last_name','1','demographics',NULL,4,NULL,NULL,'text','Last Name',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(5,'race',NULL,'demographics',NULL,10,NULL,NULL,'select','Race','0, American Indian/Alaska Native \\n 1, Asian \\n 2, Native Hawaiian or Other Pacific Islander \\n 3, Black or African American \\n 4, White \\n 5, More Than One Race \\n 6, Unknown / Not Reported',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(5,'record_id',NULL,'demographics','Basic Demography Form',1,NULL,NULL,'text','Study ID',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(5,'sex',NULL,'demographics',NULL,11,NULL,NULL,'radio','Gender','0, Female \\n 1, Male',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(5,'telephone','1','demographics',NULL,6,NULL,NULL,'text','Phone number',NULL,'Include Area Code','phone',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(5,'weight',NULL,'demographics',NULL,20,'kilograms',NULL,'text','Weight (kilograms)',NULL,NULL,'int','35','200','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'amendment_number',NULL,'project',NULL,9,NULL,NULL,'select','Amendment Number','0 \\n 1 \\n 2 \\n 3 \\n 4 \\n 5 \\n 6 \\n 7 \\n 8 \\n 9 \\n 10 \\n 11 \\n 12 \\n 13 \\n 14 \\n 15 \\n 16 \\n 17 \\n 18 \\n 19 \\n 20','',NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'amendment_status',NULL,'project',NULL,8,NULL,'Amendment Information','radio','Amendment?','0, No \\n 1, Yes','',NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'comments_pi_response',NULL,'workflow',NULL,33,NULL,NULL,'textarea','Comments - PI Process',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'comments_preprereview',NULL,'workflow',NULL,26,NULL,NULL,'textarea','Comments - Pre-Pre-Review',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'comments_prereview',NULL,'workflow',NULL,30,NULL,NULL,'textarea','Comments - Pre-Review',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'comments_src',NULL,'post_award_administration',NULL,126,NULL,NULL,'textarea','Comments - SRC Award',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'crc_cores',NULL,'post_award_administration',NULL,129,NULL,NULL,'text','CRC Cores ($)',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'crc_facilities',NULL,'post_award_administration',NULL,127,NULL,NULL,'text','CRC Facilities ($)',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'crc_original_review',NULL,'project',NULL,12,NULL,NULL,'select','CRC Original Review?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'crc_personnel',NULL,'post_award_administration',NULL,128,NULL,NULL,'text','CRC Nursing ($)',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'crc_type',NULL,'project',NULL,10,NULL,'CRC Legacy System Data','select','CRC Type','A \\n B \\n C \\n D',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'crc_webcamp_import',NULL,'project',NULL,11,NULL,NULL,'select','CRC WebCamp Project Import?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'date_agenda',NULL,'workflow',NULL,35,NULL,'Agenda Information','text','Agenda Date',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'date_pi_notification',NULL,'workflow',NULL,31,NULL,'PI Notification Information','text','PI Notification Date',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'date_pi_response',NULL,'workflow',NULL,32,NULL,NULL,'text','PI Response Date',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'date_receipt',NULL,'workflow','Workflow',23,NULL,'Pre-Pre-Review Information','text','Project Receipt Date',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'date_start_preprereview',NULL,'workflow',NULL,24,NULL,NULL,'text','Pre-Pre-Review - Start Date',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'date_start_prereview',NULL,'workflow',NULL,28,NULL,'Pre-Review Information','text','Pre-Review Notification Date',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'date_stop_preprereview',NULL,'workflow',NULL,25,NULL,NULL,'text','Pre-Pre-Review - Stop Date',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'date_stop_prereview',NULL,'workflow',NULL,29,NULL,NULL,'text','Pre-Review Completion Date',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'equipment',NULL,'post_award_administration',NULL,133,NULL,NULL,'text','Equipment ($)',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'file_biosketch1',NULL,'project',NULL,15,NULL,NULL,'file','Biosketch(1)',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'file_biosketch2',NULL,'project',NULL,16,NULL,NULL,'file','Biosketch(2)',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'file_biosketch3',NULL,'project',NULL,17,NULL,NULL,'file','Biosketch(3)',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'file_budget',NULL,'project',NULL,14,NULL,NULL,'file','Budget',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'file_crc',NULL,'project',NULL,18,NULL,NULL,'file','CRC Resources',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'file_other1',NULL,'project',NULL,19,NULL,NULL,'file','Other(1)',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'file_other2',NULL,'project',NULL,20,NULL,NULL,'file','Other(2)',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'file_other3',NULL,'project',NULL,21,NULL,NULL,'file','Other(3)',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'file_pi_comments',NULL,'workflow',NULL,34,NULL,NULL,'file','PI response',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'file_proposal',NULL,'project',NULL,13,NULL,'Project Files','file','Research Proposal',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'hospital_ancillaries',NULL,'post_award_administration',NULL,135,NULL,NULL,'text','Hospital Ancillaries ($)',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'irb_number',NULL,'project',NULL,7,NULL,NULL,'text','IRB Number',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'misc_services',NULL,'post_award_administration',NULL,134,NULL,NULL,'text','Misc. Services ($)',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'needs_administrative',NULL,'prereview_administrative','Pre-Review Administrative',43,NULL,NULL,'select','Requires Administrative?','0, Yes \\n 1, No',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'needs_biostatistics',NULL,'prereview_biostatistics','Pre-Review Biostatistics',49,NULL,NULL,'select','Requires Biostatistics?','0, Yes \\n 1, No',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'needs_budget',NULL,'prereview_budget','Pre-Review Budget',68,NULL,NULL,'select','Requires Budget?','0, Yes \\n 1, No',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'needs_community',NULL,'prereview_community','Pre-Review Community',98,NULL,NULL,'select','Requires Community?','0, Yes \\n 1, No',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'needs_cores',NULL,'prereview_cores','Pre-Review Cores',80,NULL,NULL,'select','Requires Cores?','0, Yes \\n 1, No',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'needs_nursing',NULL,'prereview_nursing','Pre-Review Nursing',74,NULL,NULL,'select','Requires Nursing?','0, Yes \\n 1, No',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'needs_nutrition',NULL,'prereview_nutrition','Pre-Review Nutrition',92,NULL,NULL,'select','Requires Nutrition?','0, Yes \\n 1, No',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'needs_other',NULL,'prereview_ctc','Pre-Review CTC',104,NULL,NULL,'select','Requires Other?','0, Yes \\n 1, No',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'needs_participant',NULL,'prereview_participant','Pre-Review Participant',62,NULL,NULL,'select','Requires Participant?','0, Yes \\n 1, No',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'needs_pi_response',NULL,'prereview_pi_response','Pre-Review PI Response',110,NULL,NULL,'select','Requires PI Response?','0, Yes \\n 1, No',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'needs_scientific',NULL,'prereview_scientific','Pre-Review Scientific',56,NULL,NULL,'select','Requires Scientific?','0, Yes \\n 1, No',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'needs_sleep',NULL,'prereview_sleep','Pre-Review Sleep',86,NULL,NULL,'select','Requires Sleep?','0, Yes \\n 1, No',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'owner_prepreview',NULL,'workflow',NULL,27,NULL,NULL,'select','Owner (Liaison)','0, Shraddha \\n 1, Jennifer \\n 2, Terri \\n 3, Cheryl \\n 4, Lynda',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'personnel',NULL,'post_award_administration',NULL,132,NULL,NULL,'text','Personnel ($)',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'pi_firstname',NULL,'project',NULL,3,NULL,NULL,'text','PI First Name',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'pi_lastname',NULL,'project',NULL,4,NULL,NULL,'text','PI Last Name',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'pi_vunetid',NULL,'project',NULL,5,NULL,NULL,'text','PI VUnetID',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'post_award_administration_complete',NULL,'post_award_administration',NULL,138,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_administrative',NULL,'prereview_administrative',NULL,44,NULL,'Enter PI Pre-Review Notes Or Attach File','textarea','Notes',NULL,NULL,NULL,NULL,NULL,NULL,'[needs_administrative] = \"0\"',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_administrative_complete',NULL,'prereview_administrative',NULL,48,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_administrative_date_received',NULL,'prereview_administrative',NULL,47,NULL,NULL,'text','Date received',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_administrative_date_sent',NULL,'prereview_administrative',NULL,46,NULL,NULL,'text','Date Sent for pre-review',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_administrative_doc',NULL,'prereview_administrative',NULL,45,NULL,NULL,'file','OR File<br><font size=1>(NOTE: If file will not open, then Save it to your computer and then Open it.)</font>',NULL,NULL,NULL,NULL,NULL,NULL,'[needs_administrative] = \"0\"',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_biostatistics',NULL,'prereview_biostatistics',NULL,50,NULL,'Enter Pre-Review Notes Or Attach File','textarea','PI Suggestions',NULL,NULL,NULL,NULL,NULL,NULL,'[needs_biostatistics] = \"0\"',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_biostatistics_complete',NULL,'prereview_biostatistics',NULL,55,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_biostatistics_date_received',NULL,'prereview_biostatistics',NULL,53,NULL,NULL,'text','Date received',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_biostatistics_date_sent',NULL,'prereview_biostatistics',NULL,52,NULL,NULL,'text','Date Sent for pre-review',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_biostatistics_doc',NULL,'prereview_biostatistics',NULL,51,NULL,NULL,'file','OR File<br><font size=1>(NOTE: If file will not open, then Save it to your computer and then Open it.)</font>',NULL,NULL,NULL,NULL,NULL,NULL,'[needs_biostatistics] = \"0\"',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_biostatistics_hours_awarded',NULL,'prereview_biostatistics',NULL,54,NULL,'Biostatistics Award','text','Consultation Hours Awarded',NULL,NULL,'float','0','5000','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_budget',NULL,'prereview_budget',NULL,69,NULL,'Enter Pre-Review Notes Or Attach File','textarea','PI Suggestions',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_budget_complete',NULL,'prereview_budget',NULL,73,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_budget_date_received',NULL,'prereview_budget',NULL,72,NULL,NULL,'text','Date received',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_budget_date_sent',NULL,'prereview_budget',NULL,71,NULL,NULL,'text','Date Sent for pre-review',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed','[needs_budget] = \"0\"',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_budget_doc',NULL,'prereview_budget',NULL,70,NULL,NULL,'file','OR File<br><font size=1>(NOTE: If file will not open, then Save it to your computer and then Open it.)</font>',NULL,NULL,NULL,NULL,NULL,NULL,'[needs_budget] = \"0\"',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_community',NULL,'prereview_community',NULL,99,NULL,'Enter Pre-Review Notes Or Attach File','textarea','PI Suggestions',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_community_complete',NULL,'prereview_community',NULL,103,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_community_date_received',NULL,'prereview_community',NULL,102,NULL,NULL,'text','Date received',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_community_date_sent',NULL,'prereview_community',NULL,101,NULL,NULL,'text','Date Sent for pre-review',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed','[needs_community] = \"0\"',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_community_doc',NULL,'prereview_community',NULL,100,NULL,NULL,'file','OR File<br><font size=1>(NOTE: If file will not open, then Save it to your computer and then Open it.)</font>',NULL,NULL,NULL,NULL,NULL,NULL,'[needs_community] = \"0\"',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_cores',NULL,'prereview_cores',NULL,81,NULL,'Enter Pre-Review Notes Or Attach File','textarea','PI Suggestions',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_cores_complete',NULL,'prereview_cores',NULL,85,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_cores_date_received',NULL,'prereview_cores',NULL,84,NULL,NULL,'text','Date received',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_cores_date_sent',NULL,'prereview_cores',NULL,83,NULL,NULL,'text','Date Sent for pre-review',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed','[needs_cores] = \"0\"',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_cores_doc',NULL,'prereview_cores',NULL,82,NULL,NULL,'file','OR File<br><font size=1>(NOTE: If file will not open, then Save it to your computer and then Open it.)</font>',NULL,NULL,NULL,NULL,NULL,NULL,'[needs_cores] = \"0\"',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_ctc_complete',NULL,'prereview_ctc',NULL,109,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_nursing',NULL,'prereview_nursing',NULL,75,NULL,'Enter Pre-Review Notes Or Attach File','textarea','PI Suggestions',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_nursing_complete',NULL,'prereview_nursing',NULL,79,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_nursing_date_received',NULL,'prereview_nursing',NULL,78,NULL,NULL,'text','Date received',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_nursing_date_sent',NULL,'prereview_nursing',NULL,77,NULL,NULL,'text','Date Sent for pre-review',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed','[needs_nursing] = \"0\"',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_nursing_doc',NULL,'prereview_nursing',NULL,76,NULL,NULL,'file','OR File<br><font size=1>(NOTE: If file will not open, then Save it to your computer and then Open it.)</font>',NULL,NULL,NULL,NULL,NULL,NULL,'[needs_nursing] = \"0\"',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_nutrition',NULL,'prereview_nutrition',NULL,93,NULL,'Enter Pre-Review Notes Or Attach File','textarea','PI Suggestions',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_nutrition_complete',NULL,'prereview_nutrition',NULL,97,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_nutrition_date_received',NULL,'prereview_nutrition',NULL,96,NULL,NULL,'text','Date received',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_nutrition_date_sent',NULL,'prereview_nutrition',NULL,95,NULL,NULL,'text','Date Sent for pre-review',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed','[needs_nutrition] = \"0\"',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_nutrition_doc',NULL,'prereview_nutrition',NULL,94,NULL,NULL,'file','OR File<br><font size=1>(NOTE: If file will not open, then Save it to your computer and then Open it.)</font>',NULL,NULL,NULL,NULL,NULL,NULL,'[needs_nutrition] = \"0\"',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_other',NULL,'prereview_ctc',NULL,105,NULL,'Enter Pre-Review Notes Or Attach File','textarea','PI Suggestions',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_other_date_received',NULL,'prereview_ctc',NULL,108,NULL,NULL,'text','Date received',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_other_date_sent',NULL,'prereview_ctc',NULL,107,NULL,NULL,'text','Date Sent for pre-review',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_other_doc',NULL,'prereview_ctc',NULL,106,NULL,NULL,'file','OR File<br><font size=1>(NOTE: If file will not open, then Save it to your computer and then Open it.)</font>',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_participant',NULL,'prereview_participant',NULL,63,NULL,'Enter Pre-Review Notes Or Attach File','textarea','PI Suggestions',NULL,NULL,NULL,NULL,NULL,NULL,'[needs_participant] = \"0\"',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_participant_complete',NULL,'prereview_participant',NULL,67,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_participant_date_received',NULL,'prereview_participant',NULL,66,NULL,NULL,'text','Date received',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_participant_date_sent',NULL,'prereview_participant',NULL,65,NULL,NULL,'text','Date Sent for pre-review',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_participant_doc',NULL,'prereview_participant',NULL,64,NULL,NULL,'file','OR File<br><font size=1>(NOTE: If file will not open, then Save it to your computer and then Open it.)</font>',NULL,NULL,NULL,NULL,NULL,NULL,'[needs_participant] = \"0\"',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_pi_response',NULL,'prereview_pi_response',NULL,111,NULL,'Enter Pre-Review Notes Or Attach File','textarea','PI response',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_pi_response_complete',NULL,'prereview_pi_response',NULL,115,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_pi_response_date_received',NULL,'prereview_pi_response',NULL,114,NULL,NULL,'text','Date received',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_pi_response_date_sent',NULL,'prereview_pi_response',NULL,113,NULL,NULL,'text','Date Sent for pre-review',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_pi_response_doc',NULL,'prereview_pi_response',NULL,112,NULL,NULL,'file','OR File<br><font size=1>(NOTE: If file will not open, then Save it to your computer and then Open it.)</font>',NULL,NULL,NULL,NULL,NULL,NULL,'[needs_pi_response] = \"0\"',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_scientific',NULL,'prereview_scientific',NULL,57,NULL,'Enter Pre-Review Notes Or Attach File','textarea','PI Suggestions',NULL,NULL,NULL,NULL,NULL,NULL,'[needs_scientific] = \"0\"',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_scientific_complete',NULL,'prereview_scientific',NULL,61,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_scientific_date_received',NULL,'prereview_scientific',NULL,60,NULL,NULL,'text','Date received',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_scientific_date_sent',NULL,'prereview_scientific',NULL,59,NULL,NULL,'text','Date Sent for pre-review',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_scientific_doc',NULL,'prereview_scientific',NULL,58,NULL,NULL,'file','OR File<br><font size=1>(NOTE: If file will not open, then Save it to your computer and then Open it.)</font>',NULL,NULL,NULL,NULL,NULL,NULL,'[needs_scientific] = \"0\"',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_sleep',NULL,'prereview_sleep',NULL,87,NULL,'Enter Pre-Review Notes Or Attach File','textarea','PI Suggestions',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_sleep_complete',NULL,'prereview_sleep',NULL,91,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_sleep_date_received',NULL,'prereview_sleep',NULL,90,NULL,NULL,'text','Date received',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_sleep_date_sent',NULL,'prereview_sleep',NULL,89,NULL,NULL,'text','Date Sent for pre-review',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed','[needs_sleep] = \"0\"',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'prereview_sleep_doc',NULL,'prereview_sleep',NULL,88,NULL,NULL,'file','OR File<br><font size=1>(NOTE: If file will not open, then Save it to your computer and then Open it.)</font>',NULL,NULL,NULL,NULL,NULL,NULL,'[needs_sleep] = \"0\"',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'proj_id',NULL,'project','Project',1,NULL,NULL,'text','Project ID',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'project_complete',NULL,'project',NULL,22,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'project_type',NULL,'project',NULL,6,NULL,NULL,'select','Project Type','1, Expedited \\n 2, Full Committee \\n 3, Industry only',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'rev_notification_date',NULL,'workflow',NULL,38,NULL,NULL,'text','Date - Sent to Reviewers',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'rev1_name',NULL,'workflow',NULL,36,NULL,NULL,'text','Reviewer 1',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'rev2_name',NULL,'workflow',NULL,37,NULL,NULL,'text','Reviewer 2',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'sleep_cores',NULL,'post_award_administration',NULL,130,NULL,NULL,'text','Sleep Core ($)',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'src_center_number',NULL,'post_award_administration',NULL,122,NULL,NULL,'text','SRC Center Number - Institutional',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'src_center_number_crc',NULL,'post_award_administration',NULL,124,NULL,NULL,'text','SRC Center Number - CRC',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'src_center_number_ctsa',NULL,'post_award_administration',NULL,123,NULL,NULL,'text','SRC Center Number - CTSA',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'src_center_number_dh',NULL,'post_award_administration',NULL,125,NULL,NULL,'text','D & H Number',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'src_full_project_period',NULL,'post_award_administration',NULL,121,NULL,NULL,'text','SRC full project period',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'src_letter_date',NULL,'post_award_administration',NULL,118,NULL,NULL,'text','SRC letter sent',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'src_letter_document',NULL,'post_award_administration',NULL,119,NULL,NULL,'file','SRC letter',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'src_notification_date',NULL,'workflow',NULL,39,NULL,NULL,'text','Date- Sent to SRC',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'src_percent_funded',NULL,'post_award_administration','Post-Award Administration',116,NULL,'Post-Award Administration','text','Percent of request funded (%)',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'src_priority_score',NULL,'workflow',NULL,41,NULL,NULL,'text','SRC Priority Score',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'src_project_completion',NULL,'post_award_administration',NULL,137,NULL,NULL,'text','SRC completion date',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'src_project_ending',NULL,'post_award_administration',NULL,120,NULL,NULL,'text','SRC project ending date',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'src_total_award_amount',NULL,'post_award_administration',NULL,117,NULL,NULL,'text','SRC Total Award Amount ($)',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'status_src_award',NULL,'workflow',NULL,40,NULL,NULL,'select','SRC Award Status','0, Approved \\n 1, Pending \\n 2, Deferred (Studio) \\n 3, Disapproved \\n 4, Tabled \\n 5, Withdrawn',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'title',NULL,'project',NULL,2,NULL,'Demographic Characteristics','textarea','Project Title',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'victr_status',NULL,'post_award_administration',NULL,136,NULL,NULL,'radio','VICTR Status','0, Inactive \\n 1, Active',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'vumc_core_facilities',NULL,'post_award_administration',NULL,131,NULL,NULL,'text','VUMC Core Facilities ($)',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'workflow_complete',NULL,'workflow',NULL,42,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'admission_date_1',NULL,'month_1_data',NULL,56,NULL,NULL,'text','Date of hospital admission',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'admission_date_2',NULL,'month_2_data',NULL,76,NULL,NULL,'text','Date of hospital admission',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'admission_date_3',NULL,'month_3_data',NULL,104,NULL,NULL,'text','Date of hospital admission',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'alb_1',NULL,'month_1_data',NULL,44,'g/dL',NULL,'text','Serum Albumin (g/dL)',NULL,NULL,'float','3','5','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'alb_2',NULL,'month_2_data',NULL,64,'g/dL',NULL,'text','Serum Albumin (g/dL)',NULL,NULL,'float','3','5','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'alb_3',NULL,'month_3_data',NULL,85,'g/dL',NULL,'text','Serum Albumin (g/dL)',NULL,NULL,'float','3','5','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'alb_b',NULL,'baseline_data',NULL,26,'g/dL',NULL,'text','Serum Albumin (g/dL)',NULL,NULL,'int','3','5','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'baseline_data_complete',NULL,'baseline_data',NULL,42,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'cause_death_1',NULL,'month_1_data',NULL,61,NULL,NULL,'select','What was the cause of death?','1, All-cause \\n 2, Cardiovascular',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'cause_death_2',NULL,'month_2_data',NULL,81,NULL,NULL,'select','What was the cause of death?','1, All-cause \\n 2, Cardiovascular',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'cause_death_3',NULL,'month_3_data',NULL,109,NULL,NULL,'select','What was the cause of death?','1, All-cause \\n 2, Cardiovascular',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'cause_hosp_1',NULL,'month_1_data',NULL,55,NULL,NULL,'select','What was the cause of hospitalization?','1, Vascular access related events \\n 2, CVD events \\n 3, Other',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'cause_hosp_2',NULL,'month_2_data',NULL,75,NULL,NULL,'select','What was the cause of hospitalization?','1, Vascular access related events \\n 2, CVD events \\n 3, Other',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'cause_hosp_3',NULL,'month_3_data',NULL,103,NULL,NULL,'select','What was the cause of hospitalization?','1, Vascular access related events \\n 2, CVD events \\n 3, Other',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'chol_1',NULL,'month_1_data',NULL,48,'mg/dL',NULL,'text','Cholesterol (mg/dL)',NULL,NULL,'float','100','300','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'chol_2',NULL,'month_2_data',NULL,68,'mg/dL',NULL,'text','Cholesterol (mg/dL)',NULL,NULL,'float','100','300','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'chol_3',NULL,'month_3_data',NULL,89,'mg/dL',NULL,'text','Cholesterol (mg/dL)',NULL,NULL,'float','100','300','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'chol_b',NULL,'baseline_data',NULL,30,'mg/dL',NULL,'text','Cholesterol (mg/dL)',NULL,NULL,'float','100','300','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'complete_study',NULL,'completion_data','Completion Data',111,NULL,'Study Completion Information','select','Has patient completed study?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'complete_study_date',NULL,'completion_data',NULL,114,NULL,NULL,'text','Date of study completion',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'completion_data_complete',NULL,'completion_data',NULL,116,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'compliance_1',NULL,'month_1_data',NULL,53,NULL,NULL,'select','How compliant was the patient in drinking the supplement?','0, 100 percent \\n 1, 99-75 percent \\n 2, 74-50 percent \\n 3, 49-25 percent \\n 4, 0-24 percent',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'compliance_2',NULL,'month_2_data',NULL,73,NULL,NULL,'select','How compliant was the patient in drinking the supplement?','0, 100 percent \\n 1, 99-75 percent \\n 2, 74-50 percent \\n 3, 49-25 percent \\n 4, 0-24 percent',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'compliance_3',NULL,'month_3_data',NULL,101,NULL,NULL,'select','How compliant was the patient in drinking the supplement?','0, 100 percent \\n 1, 99-75 percent \\n 2, 74-50 percent \\n 3, 49-25 percent \\n 4, 0-24 percent',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'creat_1',NULL,'month_1_data',NULL,46,'mg/dL',NULL,'text','Creatinine (mg/dL)',NULL,NULL,'float','0.5','20','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'creat_2',NULL,'month_2_data',NULL,66,'mg/dL',NULL,'text','Creatinine (mg/dL)',NULL,NULL,'float','0.5','20','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'creat_3',NULL,'month_3_data',NULL,87,'mg/dL',NULL,'text','Creatinine (mg/dL)',NULL,NULL,'float','0.5','20','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'creat_b',NULL,'baseline_data',NULL,28,'mg/dL',NULL,'text','Creatinine (mg/dL)',NULL,NULL,'float','0.5','20','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'date_blood_3',NULL,'month_3_data',NULL,84,NULL,NULL,'text','Date blood was drawn',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'date_blood_b',NULL,'baseline_data',NULL,25,NULL,NULL,'text','Date blood was drawn',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'date_death_1',NULL,'month_1_data',NULL,60,NULL,NULL,'text','Date of death',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'date_death_2',NULL,'month_2_data',NULL,80,NULL,NULL,'text','Date of death',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'date_death_3',NULL,'month_3_data',NULL,108,NULL,NULL,'text','Date of death',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'date_enrolled',NULL,'demographics',NULL,2,NULL,'Consent Information','text','Date subject signed consent',NULL,'YYYY-MM-DD','date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'date_supplement_dispensed',NULL,'baseline_data',NULL,41,NULL,NULL,'text','Date patient begins supplement',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'date_visit_1',NULL,'month_1_data','Month 1 Data',43,NULL,'Month 1','text','Date of Month 1 visit',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'date_visit_2',NULL,'month_2_data','Month 2 Data',63,NULL,'Month 2','text','Date of Month 2 visit',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'date_visit_3',NULL,'month_3_data','Month 3 Data',83,NULL,'Month 3','text','Date of Month 3 visit',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'date_visit_b',NULL,'baseline_data','Baseline Data',24,NULL,'Baseline Measurements','text','Date of baseline visit',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'death_1',NULL,'month_1_data',NULL,59,NULL,'Mortality Data','select','Has patient died since last visit?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'death_2',NULL,'month_2_data',NULL,79,NULL,'Mortality Data','select','Has patient died since last visit?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'death_3',NULL,'month_3_data',NULL,107,NULL,'Mortality Data','select','Has patient died since last visit?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'demographics_complete',NULL,'demographics',NULL,23,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'discharge_date_1',NULL,'month_1_data',NULL,57,NULL,NULL,'text','Date of hospital discharge',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'discharge_date_2',NULL,'month_2_data',NULL,77,NULL,NULL,'text','Date of hospital discharge',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'discharge_date_3',NULL,'month_3_data',NULL,105,NULL,NULL,'text','Date of hospital discharge',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'discharge_summary_1',NULL,'month_1_data',NULL,58,NULL,NULL,'select','Discharge summary in patients binder?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'discharge_summary_2',NULL,'month_2_data',NULL,78,NULL,NULL,'select','Discharge summary in patients binder?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'discharge_summary_3',NULL,'month_3_data',NULL,106,NULL,NULL,'select','Discharge summary in patients binder?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'dob','1','demographics',NULL,8.1,NULL,NULL,'text','Date of birth',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'drywt_1',NULL,'month_1_data',NULL,51,'kilograms',NULL,'text','Dry weight (kilograms)',NULL,NULL,'float','35','200','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'drywt_2',NULL,'month_2_data',NULL,71,'kilograms',NULL,'text','Dry weight (kilograms)',NULL,NULL,'float','35','200','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'drywt_3',NULL,'month_3_data',NULL,92,'kilograms',NULL,'text','Dry weight (kilograms)',NULL,NULL,'float','35','200','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'drywt_b',NULL,'baseline_data',NULL,33,'kilograms',NULL,'text','Dry weight (kilograms)',NULL,NULL,'float','35','200','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'ethnicity',NULL,'demographics',NULL,9,NULL,NULL,'radio','Ethnicity','0, Hispanic or Latino \\n 1, NOT Hispanic or Latino \\n 2, Unknown / Not Reported',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,'LH',NULL,NULL,NULL,NULL),(7,'first_name','1','demographics',NULL,3,NULL,'Contact Information','text','First Name',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'hospit_1',NULL,'month_1_data',NULL,54,NULL,'Hospitalization Data','select','Was patient hospitalized since last visit?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'hospit_2',NULL,'month_2_data',NULL,74,NULL,'Hospitalization Data','select','Was patient hospitalized since last visit?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'hospit_3',NULL,'month_3_data',NULL,102,NULL,'Hospitalization Data','select','Was patient hospitalized since last visit?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'kt_v_1',NULL,'month_1_data',NULL,50,NULL,NULL,'text','Kt/V',NULL,NULL,'float','0.9','3','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'kt_v_2',NULL,'month_2_data',NULL,70,NULL,NULL,'text','Kt/V',NULL,NULL,'float','0.9','3','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'kt_v_3',NULL,'month_3_data',NULL,91,NULL,NULL,'text','Kt/V',NULL,NULL,'float','0.9','3','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'kt_v_b',NULL,'baseline_data',NULL,32,NULL,NULL,'text','Kt/V',NULL,NULL,'float','0.9','3','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'last_name','1','demographics',NULL,4,NULL,NULL,'text','Last Name',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'month_1_data_complete',NULL,'month_1_data',NULL,62,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'month_2_data_complete',NULL,'month_2_data',NULL,82,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'month_3_data_complete',NULL,'month_3_data',NULL,110,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'no_show_1',NULL,'month_1_data',NULL,52,NULL,NULL,'text','Number of treatments missed',NULL,NULL,'float','0','7','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'no_show_2',NULL,'month_2_data',NULL,72,NULL,NULL,'text','Number of treatments missed',NULL,NULL,'float','0','7','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'no_show_3',NULL,'month_3_data',NULL,100,NULL,NULL,'text','Number of treatments missed',NULL,NULL,'float','0','7','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'npcr_1',NULL,'month_1_data',NULL,47,'g/kg/d',NULL,'text','Normalized Protein Catabolic Rate (g/kg/d)',NULL,NULL,'float','0.5','2','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'npcr_2',NULL,'month_2_data',NULL,67,'g/kg/d',NULL,'text','Normalized Protein Catabolic Rate (g/kg/d)',NULL,NULL,'float','0.5','2','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'npcr_3',NULL,'month_3_data',NULL,88,'g/kg/d',NULL,'text','Normalized Protein Catabolic Rate (g/kg/d)',NULL,NULL,'float','0.5','2','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'npcr_b',NULL,'baseline_data',NULL,29,'g/kg/d',NULL,'text','Normalized Protein Catabolic Rate (g/kg/d)',NULL,NULL,'float','0.5','2','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'plasma1_3',NULL,'month_3_data',NULL,93,NULL,NULL,'select','Collected Plasma 1?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'plasma1_b',NULL,'baseline_data',NULL,34,NULL,NULL,'select','Collected Plasma 1?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'plasma2_3',NULL,'month_3_data',NULL,94,NULL,NULL,'select','Collected Plasma 2?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'plasma2_b',NULL,'baseline_data',NULL,35,NULL,NULL,'select','Collected Plasma 2?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'plasma3_3',NULL,'month_3_data',NULL,95,NULL,NULL,'select','Collected Plasma 3?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'plasma3_b',NULL,'baseline_data',NULL,36,NULL,NULL,'select','Collected Plasma 3?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'prealb_1',NULL,'month_1_data',NULL,45,'mg/dL',NULL,'text','Serum Prealbumin (mg/dL)',NULL,NULL,'float','10','40','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'prealb_2',NULL,'month_2_data',NULL,65,'mg/dL',NULL,'text','Serum Prealbumin (mg/dL)',NULL,NULL,'float','10','40','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'prealb_3',NULL,'month_3_data',NULL,86,'mg/dL',NULL,'text','Serum Prealbumin (mg/dL)',NULL,NULL,'float','10','40','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'prealb_b',NULL,'baseline_data',NULL,27,'mg/dL',NULL,'text','Serum Prealbumin (mg/dL)',NULL,NULL,'float','10','40','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'race',NULL,'demographics',NULL,10,NULL,NULL,'select','Race','0, American Indian/Alaska Native \\n 1, Asian \\n 2, Native Hawaiian or Other Pacific Islander \\n 3, Black or African American \\n 4, White \\n 5, More Than One Race \\n 6, Unknown / Not Reported',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'randomization_form_complete',NULL,'randomization_form',NULL,23.2,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'randomization_group',NULL,'randomization_form','Randomization Form',23.1,NULL,'General Comments','select','Randomization Group','0, Drug A \\n 1, Drug B \\n 2, Drug C',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'serum1_3',NULL,'month_3_data',NULL,96,NULL,NULL,'select','Collected Serum 1?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'serum1_b',NULL,'baseline_data',NULL,37,NULL,NULL,'select','Collected Serum 1?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'serum2_3',NULL,'month_3_data',NULL,97,NULL,NULL,'select','Collected Serum 2?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'serum2_b',NULL,'baseline_data',NULL,38,NULL,NULL,'select','Collected Serum 2?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'serum3_3',NULL,'month_3_data',NULL,98,NULL,NULL,'select','Collected Serum 3?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'serum3_b',NULL,'baseline_data',NULL,39,NULL,NULL,'select','Collected Serum 3?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'sex',NULL,'demographics',NULL,11,NULL,NULL,'radio','Gender','0, Female \\n 1, Male',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'sga_3',NULL,'month_3_data',NULL,99,NULL,NULL,'text','Subject Global Assessment (score = 1-7)',NULL,NULL,'float','0.9','7.1','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'sga_b',NULL,'baseline_data',NULL,40,NULL,NULL,'text','Subject Global Assessment (score = 1-7)',NULL,NULL,'float','0.9','7.1','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'study_comments',NULL,'completion_data',NULL,115,NULL,'General Comments','textarea','Comments',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'study_id',NULL,'demographics','Demographics',1,NULL,NULL,'text','Study ID',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'transferrin_1',NULL,'month_1_data',NULL,49,'mg/dL',NULL,'text','Transferrin (mg/dL)',NULL,NULL,'float','100','300','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'transferrin_2',NULL,'month_2_data',NULL,69,'mg/dL',NULL,'text','Transferrin (mg/dL)',NULL,NULL,'float','100','300','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'transferrin_3',NULL,'month_3_data',NULL,90,'mg/dL',NULL,'text','Transferrin (mg/dL)',NULL,NULL,'float','100','300','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'transferrin_b',NULL,'baseline_data',NULL,31,'mg/dL',NULL,'text','Transferrin (mg/dL)',NULL,NULL,'float','100','300','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'withdraw_date',NULL,'completion_data',NULL,112,NULL,NULL,'text','Put a date if patient withdrew study',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(7,'withdraw_reason',NULL,'completion_data',NULL,113,NULL,NULL,'select','Reason patient withdrew from study','0, Non-compliance \\n 1, Did not wish to continue in study \\n 2, Could not tolerate the supplement \\n 3, Hospitalization \\n 4, Other',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'age',NULL,'id_shipping',NULL,8,NULL,NULL,'text','Age',NULL,'Age at surgery, DOB not available','float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'age_at_surgery',NULL,'pathology_review',NULL,70,NULL,NULL,'calc','Age at Surgery','round(datediff([date_of_birth],[date_surgery],\"y\",\"mdy\",true),0)',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'another_accnumber',NULL,'tma_information',NULL,186,NULL,NULL,'yesno','Another_AccNumber?',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'bc_molecularsubtype',NULL,'pathology_review',NULL,94,NULL,NULL,'select','BC_MolecularSubtype','1, Luminal A \\n 2, Luminal B \\n 3, HER2 \\n 4, Triple Negative \\n 5, N/A',NULL,NULL,NULL,NULL,NULL,'[tumor_origin] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'bc_precancerous',NULL,'pathology_review',NULL,98,NULL,NULL,'select','BC_Precancerous','1, Not seen \\n 2, DCIS \\n 3, LCIS \\n 4, DCIS+LCIS',NULL,NULL,NULL,NULL,NULL,'[tumor_origin] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'blk_no_received',NULL,'id_shipping',NULL,17,NULL,NULL,'text','Block_ Received',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'block_metastatic',NULL,'pathology_review',NULL,76,NULL,NULL,'text','BlockNum_Metastatic',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'block_normal',NULL,'pathology_review',NULL,75,NULL,NULL,'text','BlockNum_Normal',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'block_precancerous',NULL,'pathology_review',NULL,77,NULL,NULL,'text','BlockNum_Precancerous',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'block_received2',NULL,'id_shipping',NULL,37,NULL,NULL,'text','Block_ Received2',NULL,NULL,'float',NULL,NULL,'soft_typed','[secondtime_getsample] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'block_received3',NULL,'id_shipping',NULL,55,NULL,NULL,'text','Block_ Received3',NULL,NULL,'float',NULL,NULL,'soft_typed','[thirdtime_getsample] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'block_tumor',NULL,'pathology_review',NULL,74,NULL,NULL,'text','BlockNum_Tumor',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'clin_diagn_breast',NULL,'pathology_review',NULL,84,NULL,'For Breast Cancer Samples','select','Clin_Diagn_Breast','1, Noninvasive carcinoma (NOS) \\n 2, Ductal carcinoma in situ \\n 3, Lobular carcinoma in situ \\n 4, Paget disease without invasive carcinoma \\n 5, Invasive carcinoma (NOS) \\n 6, Invasive ductal carcinoma \\n 7, IDC with an extensive intraductal component \\n 8, IDC with Paget disease \\n 9, Invasive lobular \\n 10, Mucinous \\n 11, Medullary \\n 12, Papillary \\n 13, Tubular \\n 14, Adenoid cystic \\n 15, Secretory (juvenile) \\n 16, Apocrine \\n 17, Cribriform \\n 18, Carcinoma with squamous metaplasia \\n 19, Carcinoma with spindle cell metaplasia \\n 20, Carcinoma with cartilaginous/osseous metaplasia \\n 21, Carcinoma with metaplasia, mixed type \\n 22, Other(s) (specify) \\n 23, Not assessable \\n 24, No cancer tissue \\n 25, IDC+ILC (50 -90% each component)',NULL,NULL,NULL,NULL,NULL,'[tumor_origin] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'clin_diagn_lung',NULL,'pathology_review',NULL,125,NULL,'For Lung Cancer Samples','select','Clin_Diagn_Lung','1, Squamous cell carcinoma 8070/3 \\n 2, Small cell carcinoma 8041/3 \\n 3, Adenocarcinoma 8140/3 \\n 4, Adenocarcinoma, mixed subtype 8255/3 \\n 5, Adenocarcinoma, Acinar 8550/3 \\n 6, Adenocarcinoma, Papillary 8260/3 \\n 7, Adenocarcinoma, Micropapillary \\n 8, Bronchioloalveolar carcinoma 8250/3 \\n 9, Solid adenocarcinoma with mucin 8230/3 \\n 10, Adenosquamous carcinoma 8560/3 \\n 11, Large cell carcinoma 8012/3 \\n 12, Sarcomatoid carcinoma 8033/3 \\n 13, Carcinoid tumour 8240/3 \\n 14, Mucoepidermoid carcinoma 8430/3 \\n 15, Epithelial-myoepithelial carcinoma 8562/3 \\n 16, Adenoid cystic carcinoma 8200/3 \\n 17, Unclassified carcinoma \\n 18, Others \\n 19, Large cell neuroendocrine carcinoma  8013/3',NULL,NULL,NULL,NULL,NULL,'[tumor_origin] = \'4\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'clin_diagn_others',NULL,'pathology_review',NULL,133,NULL,'For Other Cancer Samples','text','Clin_Diagn_Others',NULL,NULL,NULL,NULL,NULL,'soft_typed','[tumor_origin] = \'5\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'clin_diagn_prostate',NULL,'pathology_review',NULL,102,NULL,'For Prostate Cancer Samples','select','Clin_Diagn_Prostate','1, Adenocarcinoma,NOS \\n 2, Prostatic duct adenocarcinoma \\n 3, Mucinous adenocarcinoma \\n 4, Signet-ring cell carcinoma \\n 5, Adenosquemous carcinoma \\n 6, Small cell carcinoma \\n 7, Sarcomatoid carcinoma \\n 8, Other (specifiy) \\n 9, Undifferentiated carcinoma, NOS \\n 10, Cannot be determined',NULL,NULL,NULL,NULL,NULL,'[tumor_origin] = \'2\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'clin_giag_colon',NULL,'pathology_review',NULL,115,NULL,'For Colon Cancer Samples','select','Clin_Diagn_Colon','1, 1 Adenocarcinoma \\n 2, 2 Mucinous adenocarcinoma \\n 3, 3 Medullary carcinoma \\n 4, 4 Signet ring cell carcinoma \\n 5, 5 Small cell carcinoma \\n 6, 6 Squamous cell carcinoma \\n 7, 7 Adenosquamous carcinoma \\n 8, 8 Others \\n 9, 9 Adenoma',NULL,NULL,NULL,NULL,NULL,'[tumor_origin] = \'3\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'clin_gleason_score',NULL,'pathology_review',NULL,105,NULL,NULL,'text','Clin_Gleason_Score',NULL,NULL,NULL,NULL,NULL,'soft_typed','[tumor_origin] = \'2\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'clin_grade_breast',NULL,'pathology_review',NULL,88,NULL,NULL,'select','Clin_Grade_Breast','1, 1 \\n 2, 2 \\n 3, 3 \\n 4, 1~2 \\n 5, 2~3 \\n 6, N/A',NULL,NULL,NULL,NULL,NULL,'[tumor_origin] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'clin_grade_colon',NULL,'pathology_review',NULL,119,NULL,NULL,'select','Clin_Grade_Colon','1, Low \\n 2, Intermediate \\n 3, High \\n 4, N/A \\n 5, Low-Intermediate \\n 6, Intermediate-High',NULL,NULL,NULL,NULL,NULL,'[tumor_origin] = \'3\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'clin_grade_lung',NULL,'pathology_review',NULL,128,NULL,NULL,'select','Clin_Grade_Lung','1, Low \\n 2, Intermediate \\n 3, High \\n 4, N/A \\n 5, Low-Intermediate \\n 6, Intermediate-High',NULL,NULL,NULL,NULL,NULL,'[tumor_origin] = \'4\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'clin_grade_others',NULL,'pathology_review',NULL,135,NULL,NULL,'text','Clin_Grade_Others',NULL,NULL,NULL,NULL,NULL,'soft_typed','[tumor_origin] = \'5\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'clin_grade_pro',NULL,'pathology_review',NULL,106,NULL,NULL,'select','Clin_Grade_Pro','1, Low(1-4) \\n 2, Intermediate(5-7) \\n 3, High(8-10)','Gleason Score System',NULL,NULL,NULL,NULL,'[tumor_origin] = \'2\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'collection_note2',NULL,'id_shipping',NULL,27,NULL,NULL,'textarea','FollowUp_Note2',NULL,NULL,NULL,NULL,NULL,NULL,'[follow_up_needed2] = \'1\' and [secondtime_getsample] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'collection_note3',NULL,'id_shipping',NULL,45,NULL,NULL,'textarea','FollowUp_Note',NULL,NULL,NULL,NULL,NULL,NULL,'[follow_up_needed3] = \'1\' and [thirdtime_getsample] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'date_of_birth','1','id_shipping',NULL,7,NULL,NULL,'text','Date of Birth',NULL,NULL,'date_mdy',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'date_surgery',NULL,'pathology_review',NULL,69,NULL,'Clinical Pathology Information','text','Date_Surgery',NULL,NULL,'date_mdy',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'dna_index',NULL,'pathology_review',NULL,97,NULL,NULL,'text','DNA Index',NULL,'Unfavorable: >1.1',NULL,NULL,NULL,'soft_typed','[tumor_origin] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'estrogen_receptor',NULL,'pathology_review',NULL,90,NULL,NULL,'select','Estrogen Receptor','0, negative \\n 1, week (<1%) \\n 2, positive (>=1%) \\n 3, N/A',NULL,NULL,NULL,NULL,NULL,'[tumor_origin] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'extraprostate_extention',NULL,'pathology_review',NULL,114,NULL,NULL,'select','ExtraProstate Extention','0, No \\n 1, Yes \\n 2, N/A',NULL,NULL,NULL,NULL,NULL,'[tumor_origin] = \'2\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'facility_city',NULL,'id_shipping',NULL,10,NULL,NULL,'text','Facility_City',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'facility_city2',NULL,'id_shipping',NULL,30,NULL,NULL,'text','Facility_City2',NULL,NULL,NULL,NULL,NULL,'soft_typed','[secondtime_getsample] = \'1\' and [samefacasbefore] = \'0\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'facility_city3',NULL,'id_shipping',NULL,48,NULL,NULL,'text','Facility_City3',NULL,NULL,NULL,NULL,NULL,'soft_typed','[samefacilityasbefore2] = \'0\' and [thirdtime_getsample] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'facility_name',NULL,'id_shipping',NULL,9,NULL,'Shipping Information','text','Facility_Name',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'facility_name2',NULL,'id_shipping',NULL,29,NULL,NULL,'text','Facility_Name2',NULL,NULL,NULL,NULL,NULL,'soft_typed','[samefacasbefore] = \'0\' and [secondtime_getsample] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'facility_name3',NULL,'id_shipping',NULL,47,NULL,NULL,'text','Facility_Name3',NULL,NULL,NULL,NULL,NULL,'soft_typed','[samefacilityasbefore2] = \'0\' and [thirdtime_getsample] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'facility_state',NULL,'id_shipping',NULL,11,NULL,NULL,'text','Facility_State',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'facility_state2',NULL,'id_shipping',NULL,31,NULL,NULL,'text','Facility_State2',NULL,NULL,NULL,NULL,NULL,'soft_typed','[secondtime_getsample] = \'1\' and [samefacasbefore] = \'0\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'facility_state3',NULL,'id_shipping',NULL,49,NULL,NULL,'text','Facility_State3',NULL,NULL,NULL,NULL,NULL,'soft_typed','[samefacilityasbefore2] = \'0\' and [thirdtime_getsample] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'first_name','1','id_shipping',NULL,3,NULL,NULL,'text','First Name',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,1,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'five_um_met_currentquant',NULL,'slide_information',NULL,166,NULL,NULL,'text','5um_Met_CurrentQuant',NULL,NULL,NULL,NULL,NULL,'soft_typed','[is_there_metastatic_tumor] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'five_um_met_quant',NULL,'slide_information',NULL,165,NULL,NULL,'text','5um_Met_Quant',NULL,NULL,NULL,NULL,NULL,'soft_typed','[is_there_metastatic_tumor] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'five_um_nor_currquant',NULL,'slide_information',NULL,145,NULL,NULL,'text','5um_Nor_CurrQuant',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'five_um_nor_currquant2',NULL,'slide_information',NULL,157,NULL,NULL,'text','5um_Nor_CurrQuant2',NULL,NULL,'float',NULL,NULL,'soft_typed','[is_there_another_accnumber] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'five_um_nor_quant',NULL,'slide_information',NULL,144,NULL,NULL,'text','5um_Nor_Quant',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'five_um_nor_quant2',NULL,'slide_information',NULL,156,NULL,NULL,'text','5um_Nor_Quant2',NULL,NULL,'float',NULL,NULL,'soft_typed','[is_there_another_accnumber] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'five_um_precancer_curquant',NULL,'slide_information',NULL,174,NULL,NULL,'text','5um_Precancer_CurrentQuant',NULL,NULL,NULL,NULL,NULL,'soft_typed','[is_there_precancer] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'five_um_precancer_quant',NULL,'slide_information',NULL,173,NULL,NULL,'text','5um_Precancer_Quant',NULL,NULL,NULL,NULL,NULL,'soft_typed','[is_there_precancer] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'five_um_tumor_currquant',NULL,'slide_information',NULL,141,NULL,NULL,'text','5um_Tumor_CurrQuant',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'five_um_tumor_currquant2',NULL,'slide_information',NULL,153,NULL,NULL,'text','5um_Tumor_CurrQuant2',NULL,NULL,'float',NULL,NULL,'soft_typed','[is_there_another_accnumber] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'five_um_tumor_quant',NULL,'slide_information','Slide Information',140,NULL,NULL,'text','5um_Tumor_Quant',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'five_um_tumor_quant2',NULL,'slide_information',NULL,152,NULL,NULL,'text','5um_Tumor_Quant2',NULL,NULL,'float',NULL,NULL,'soft_typed','[is_there_another_accnumber] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'follow_up_needed2',NULL,'id_shipping',NULL,26,NULL,NULL,'yesno','Follow up needed?',NULL,NULL,NULL,NULL,NULL,NULL,'[secondtime_getsample] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'follow_up_needed3',NULL,'id_shipping',NULL,44,NULL,NULL,'yesno','Follow up needed?',NULL,NULL,NULL,NULL,NULL,NULL,'[thirdtime_getsample] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'followup_note',NULL,'id_shipping',NULL,24,NULL,NULL,'textarea','FollowUp_Note',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'forwhoseproject',NULL,'slide_tracking',NULL,195,NULL,NULL,'text','ForWhoseProject1',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'gender',NULL,'pathology_review',NULL,71,NULL,NULL,'select','Gender','1, male \\n 2, female \\n 3, N/A',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'her2_fish',NULL,'pathology_review',NULL,93,NULL,NULL,'select','HER2_FISH','0, 0 (Non-Amplified, <1.8) \\n 1, 1 (Amplified, >2.2) \\n 2, 2 (Borderline, 1.8~2.2) \\n 3, N/A',NULL,NULL,NULL,NULL,NULL,'[tumor_origin] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'her2_immunohistochemistry',NULL,'pathology_review',NULL,92,NULL,NULL,'select','HER2_Immunohistochemistry','0, 0 \\n 1, 1 (1~9% cells positivity) \\n 2, 2 (10-30% cells positivity) \\n 3, 3 (>30% cells positivity with strong color) \\n 4, N/A',NULL,NULL,NULL,NULL,NULL,'[tumor_origin] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'id_shipping_complete',NULL,'id_shipping',NULL,61,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'if_ilc_subtype',NULL,'pathology_review',NULL,86,NULL,NULL,'select','ILC_Subtype','901, classical ILC \\n 902, solid ILC \\n 903, pleomorphic ILC \\n 904, alveolar ILC \\n 905, tubulolobular ILC \\n 906, mixed ILC \\n 907, signet ring cell ILC \\n 908, others',NULL,NULL,NULL,NULL,NULL,'[tumor_origin] = \'1\' and [lab_diagn_breast] = \'9\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'if_no_location2',NULL,'slide_information',NULL,161,NULL,NULL,'text','If_No_Location2',NULL,NULL,NULL,NULL,NULL,'soft_typed','[same_slideloc] = \'0\' and [is_there_another_accnumber] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'if_others_specify',NULL,'pathology_review',NULL,127,NULL,NULL,'text','If_Others_Specify',NULL,NULL,NULL,NULL,NULL,'soft_typed','[tumor_origin] = \'4\' and [lab_diagn_lung] = \'10\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'invitrosize1',NULL,'pathology_review',NULL,78,NULL,NULL,'text','InvitroSize1',NULL,'Maximum size in centimeter','float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'invitrosize2',NULL,'pathology_review',NULL,79,NULL,NULL,'text','InvitroSize2',NULL,'In % of total tissue volume for prostate cancer','float',NULL,NULL,'soft_typed','[tumor_origin] = \'2\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'invitrosize3',NULL,'pathology_review',NULL,80,NULL,NULL,'text','InvitroSize3',NULL,'The seceond largest tumor',NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'is_there_another_accnumber',NULL,'slide_information',NULL,150,NULL,NULL,'yesno','Is there another AccNumber?',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'is_there_metastatic_tumor',NULL,'slide_information',NULL,163,NULL,NULL,'yesno','Is there Metastatic Tumor?',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'is_there_precancer',NULL,'slide_information',NULL,171,NULL,NULL,'yesno','Is There Precancer?',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'ki_67',NULL,'pathology_review',NULL,95,NULL,NULL,'text','Ki-67',NULL,'positive cells in percentage','float',NULL,NULL,'soft_typed','[tumor_origin] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'lab_diag_prostate',NULL,'pathology_review',NULL,103,NULL,NULL,'select','Lab_Diag_Prostate','1, Adenocarcinoma,NOS \\n 2, Prostatic duct adenocarcinoma \\n 3, Mucinous adenocarcinoma \\n 4, Signet-ring cell carcinoma \\n 5, Adenosquemous carcinoma \\n 6, Small cell carcinoma \\n 7, Sarcomatoid carcinoma \\n 8, Other (specifiy) \\n 9, Undifferentiated carcinoma, NOS \\n 10, Cannot be determined',NULL,NULL,NULL,NULL,NULL,'[tumor_origin] = \'2\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'lab_diagn_breast',NULL,'pathology_review',NULL,85,NULL,NULL,'select','Lab_Diagn_Breast','1, Noninvasive carcinoma (NOS) \\n 2, Ductal carcinoma in situ \\n 3, Lobular carcinoma in situ \\n 4, Paget disease without invasive carcinoma \\n 5, Invasive carcinoma (NOS) \\n 6, Invasive ductal carcinoma \\n 7, IDC with an extensive intraductal component \\n 8, IDC with Paget disease \\n 9, Invasive lobular \\n 10, Mucinous \\n 11, Medullary \\n 12, Papillary \\n 13, Tubular \\n 14, Adenoid cystic \\n 15, Secretory (juvenile) \\n 16, Apocrine \\n 17, Cribriform \\n 18, Carcinoma with squamous metaplasia \\n 19, Carcinoma with spindle cell metaplasia \\n 20, Carcinoma with cartilaginous/osseous metaplasia \\n 21, Carcinoma with metaplasia, mixed type \\n 22, Other(s) (specify) \\n 23, Not assessable \\n 24, No cancer tissue \\n 25, IDC+ILC (50 -90% each component)',NULL,NULL,NULL,NULL,NULL,'[tumor_origin] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'lab_diagn_colon',NULL,'pathology_review',NULL,117,NULL,NULL,'select','Lab_Diagn_Colon','1, 1 Adenocarcinoma \\n 2, 2 Mucinous adenocarcinoma \\n 3, 3 Medullary carcinoma \\n 4, 4 Signet ring cell carcinoma \\n 5, 5 Small cell carcinoma \\n 6, 6 Squamous cell carcinoma \\n 7, 7 Adenosquamous carcinoma \\n 8, 8 Others \\n 9, 9 Adenoma',NULL,NULL,NULL,NULL,NULL,'[tumor_origin] = \'3\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'lab_diagn_lung',NULL,'pathology_review',NULL,126,NULL,NULL,'select','Lab_Diagn_Lung','1, Squamous cell carcinoma 8070/3 \\n 2, Small cell carcinoma 8041/3 \\n 3, Adenocarcinoma 8140/3 \\n 4, Adenocarcinoma, mixed subtype 8255/3 \\n 5, Adenocarcinoma, Acinar 8550/3 \\n 6, Adenocarcinoma, Papillary 8260/3 \\n 7, Adenocarcinoma, Micropapillary \\n 8, Bronchioloalveolar carcinoma 8250/3 \\n 9, Solid adenocarcinoma with mucin 8230/3 \\n 10, Adenosquamous carcinoma 8560/3 \\n 11, Large cell carcinoma 8012/3 \\n 12, Sarcomatoid carcinoma 8033/3 \\n 13, Carcinoid tumour 8240/3 \\n 14, Mucoepidermoid carcinoma 8430/3 \\n 15, Epithelial-myoepithelial carcinoma 8562/3 \\n 16, Adenoid cystic carcinoma 8200/3 \\n 17, Unclassified carcinoma \\n 18, Others \\n 19, Large cell neuroendocrine carcinoma 8013/3',NULL,NULL,NULL,NULL,NULL,'[tumor_origin] = \'4\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'lab_diagn_others',NULL,'pathology_review',NULL,134,NULL,NULL,'text','Lab_Diagn_Others',NULL,NULL,NULL,NULL,NULL,'soft_typed','[tumor_origin] = \'5\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'lab_gleason_score',NULL,'pathology_review',NULL,107,NULL,NULL,'text','Lab_Gleason_Score',NULL,NULL,NULL,NULL,NULL,'soft_typed','[tumor_origin] = \'2\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'lab_grade_breast',NULL,'pathology_review',NULL,89,NULL,NULL,'select','Lab_Grade_Breast','1, 1 \\n 2, 2 \\n 3, 3 \\n 4, N/A',NULL,NULL,NULL,NULL,NULL,'[tumor_origin] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'lab_grade_colon',NULL,'pathology_review',NULL,120,NULL,NULL,'select','Lab_Grade_Colon','1, Low \\n 2, Intermediate \\n 3, High \\n 4, N/A',NULL,NULL,NULL,NULL,NULL,'[tumor_origin] = \'3\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'lab_grade_lung',NULL,'pathology_review',NULL,129,NULL,NULL,'select','Lab_Grade_Lung','1, Low \\n 2, Intermediate \\n 3, High \\n 4, N/A',NULL,NULL,NULL,NULL,NULL,'[tumor_origin] = \'4\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'lab_grade_others',NULL,'pathology_review',NULL,136,NULL,NULL,'text','Lab_Grade_Others',NULL,NULL,NULL,NULL,NULL,'soft_typed','[tumor_origin] = \'5\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'lab_grade_pro',NULL,'pathology_review',NULL,108,NULL,NULL,'select','Lab_Grade_Pro','1, Low(1-4) \\n 2, Intermediate(5-7) \\n 3, High(8-10)','Gleason Score System (1-10)',NULL,NULL,NULL,NULL,'[tumor_origin] = \'2\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'lab_id','0','id_shipping','ID Shipping',1,NULL,'IDs','text','Lab ID',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'labcirculation_time',NULL,'id_shipping',NULL,23,NULL,NULL,'calc','LabCirculation_time','round(datediff([receivedate],[return_date],\"d\",\"mdy\"))',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'last_name','1','id_shipping',NULL,5,NULL,NULL,'text','Last Name',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,1,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'metastatic_accnum',NULL,'slide_information',NULL,164,NULL,NULL,'text','Metastatic_AccNum',NULL,NULL,NULL,NULL,NULL,'soft_typed','[is_there_metastatic_tumor] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'middle_name',NULL,'id_shipping',NULL,4,NULL,NULL,'text','Middle Name',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'other_acc_no',NULL,'pathology_review',NULL,73,NULL,NULL,'text','Other_Acc_No',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'other_location_lung',NULL,'pathology_review',NULL,67,NULL,NULL,'text','Other location_lung',NULL,NULL,NULL,NULL,NULL,'soft_typed','[tumor_origin] = \'4\' and [tumor_location_lung] = \'11\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'otheraccnumber',NULL,'id_shipping',NULL,36,NULL,NULL,'text','OtherAccNumber',NULL,NULL,NULL,NULL,NULL,'soft_typed','[secondtime_getsample] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'otheraccnumber2',NULL,'id_shipping',NULL,16,NULL,NULL,'text','OtherAccNumber',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'otheraccnumber3',NULL,'id_shipping',NULL,54,NULL,NULL,'text','OtherAccNumber',NULL,NULL,NULL,NULL,NULL,'soft_typed','[thirdtime_getsample] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'p53_ihc',NULL,'pathology_review',NULL,96,NULL,NULL,'text','p53_IHC',NULL,'positive cells in percentage',NULL,NULL,NULL,'soft_typed','[tumor_origin] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'parapieceloc_1',NULL,'slide_information',NULL,149,NULL,NULL,'text','ParaPieceLoc_1',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'parapieceloc_2',NULL,'slide_information',NULL,162,NULL,NULL,'text','ParaPieceLoc_2',NULL,NULL,NULL,NULL,NULL,'soft_typed','[is_there_another_accnumber] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'parapieceloc_metastatic',NULL,'slide_information',NULL,170,NULL,NULL,'text','ParaPieceLoc_Metastatic',NULL,NULL,NULL,NULL,NULL,'soft_typed','[is_there_metastatic_tumor] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'parapieceloc_precancer',NULL,'slide_information',NULL,178,NULL,NULL,'text','ParaPieceLoc_Precancer',NULL,NULL,NULL,NULL,NULL,'soft_typed','[is_there_precancer] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'pathaccnum_2',NULL,'slide_information',NULL,151,NULL,NULL,'text','PathAccNum_2',NULL,NULL,NULL,NULL,NULL,'soft_typed','[is_there_another_accnumber] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'pathaccnumber','1','id_shipping',NULL,15,NULL,NULL,'text','PathAccNumber',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,1,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'pathaccnumber2',NULL,'id_shipping',NULL,35,NULL,NULL,'text','PathAccNumber',NULL,NULL,NULL,NULL,NULL,'soft_typed','[secondtime_getsample] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'pathaccnumber3',NULL,'id_shipping',NULL,53,NULL,NULL,'text','PathAccNumber3',NULL,NULL,NULL,NULL,NULL,'soft_typed','[thirdtime_getsample] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'pathoireview_note',NULL,'pathology_review',NULL,138,NULL,NULL,'textarea','PatholReview_Note',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'pathol_acc_no','1','pathology_review',NULL,72,NULL,NULL,'text','Pathol_Acc_No',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,1,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'pathology_review_complete',NULL,'pathology_review',NULL,139,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'perineuralinvasion',NULL,'pathology_review',NULL,81,NULL,NULL,'select','PerineuralInvasion','0, No \\n 1, Yes \\n 2, N/A',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'pre_cancerous_colon',NULL,'pathology_review',NULL,124,NULL,NULL,'textarea','Pre-cancerous_Colon',NULL,NULL,NULL,NULL,NULL,NULL,'[tumor_origin] = \'3\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'precancer_accnum',NULL,'slide_information',NULL,172,NULL,NULL,'text','PreCancer_AccNum',NULL,NULL,NULL,NULL,NULL,'soft_typed','[is_there_precancer] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'progesterone_receptor',NULL,'pathology_review',NULL,91,NULL,NULL,'select','Progesterone Receptor','0, negative (0~2) \\n 1, week (3~4) \\n 2, intermediate (5~6) \\n 3, strong (7~8) \\n 4, N/A','Allred Score System 0-8',NULL,NULL,NULL,NULL,'[tumor_origin] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'psa_level',NULL,'pathology_review',NULL,112,NULL,NULL,'text','PSA_Level',NULL,'ng/mL',NULL,NULL,NULL,'soft_typed','[tumor_origin] = \'2\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'pulled_quant1',NULL,'slide_tracking',NULL,197,NULL,NULL,'text','Pulled_Quant1',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'pulling_date1',NULL,'slide_tracking','Slide Tracking',194,NULL,NULL,'text','Pulling_Date1',NULL,NULL,'date_mdy',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'receivedate','1','id_shipping',NULL,12,NULL,NULL,'text','ReceiveDate',NULL,NULL,'date_mdy',NULL,NULL,'soft_typed',NULL,1,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'receivedate2',NULL,'id_shipping',NULL,32,NULL,NULL,'text','ReceiveDate2',NULL,NULL,'date_mdy',NULL,NULL,'soft_typed','[secondtime_getsample] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'receivedate3',NULL,'id_shipping',NULL,50,NULL,NULL,'text','ReceiveDate3',NULL,NULL,'date_mdy',NULL,NULL,'soft_typed','[thirdtime_getsample] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'receivetracking2',NULL,'id_shipping',NULL,34,NULL,NULL,'text','ReceiveTracking2',NULL,NULL,NULL,NULL,NULL,'soft_typed','[secondtime_getsample] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'receivetracking3',NULL,'id_shipping',NULL,52,NULL,NULL,'text','ReceiveTracking3',NULL,NULL,NULL,NULL,NULL,'soft_typed','[thirdtime_getsample] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'return_date',NULL,'id_shipping',NULL,21,NULL,NULL,'text','ReturnDate',NULL,NULL,'date_mdy',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'return_needed',NULL,'id_shipping',NULL,20,NULL,NULL,'yesno','Return_Needed?',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'return_needed2',NULL,'id_shipping',NULL,40,NULL,NULL,'yesno','Return_needed?',NULL,NULL,NULL,NULL,NULL,NULL,'[secondtime_getsample] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'return_needed3',NULL,'id_shipping',NULL,58,NULL,NULL,'yesno','Return_needed?',NULL,NULL,NULL,NULL,NULL,NULL,'[thirdtime_getsample] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'return_tracking',NULL,'id_shipping',NULL,22,NULL,NULL,'text','ReturnTracking',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'return_tracking2',NULL,'id_shipping',NULL,42,NULL,NULL,'text','ReturnTracking2',NULL,NULL,NULL,NULL,NULL,'soft_typed','[return_needed2] = \'1\' and [secondtime_getsample] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'returndate2',NULL,'id_shipping',NULL,41,NULL,NULL,'text','ReturnDate2',NULL,NULL,'date_mdy',NULL,NULL,'soft_typed','[return_needed2] = \'1\' and [secondtime_getsample] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'returndate3',NULL,'id_shipping',NULL,59,NULL,NULL,'text','ReturnDate3',NULL,NULL,'date_mdy',NULL,NULL,'soft_typed','[return_needed3] = \'1\' and [thirdtime_getsample] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'returntracking3',NULL,'id_shipping',NULL,60,NULL,NULL,'text','ReturnTracking3',NULL,NULL,NULL,NULL,NULL,'soft_typed','[return_needed3] = \'1\' and [thirdtime_getsample] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'same_slideloc',NULL,'slide_information',NULL,160,NULL,NULL,'yesno','Same_SlideLoc?',NULL,NULL,NULL,NULL,NULL,NULL,'[is_there_another_accnumber] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'samefacasbefore',NULL,'id_shipping',NULL,28,NULL,NULL,'yesno','SameFacilityAsBefore?',NULL,NULL,NULL,NULL,NULL,NULL,'[secondtime_getsample] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'samefacilityasbefore2',NULL,'id_shipping',NULL,46,NULL,NULL,'yesno','SameFacilityAsBefore?',NULL,NULL,NULL,NULL,NULL,NULL,'[thirdtime_getsample] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'secondtime_getsample',NULL,'id_shipping',NULL,25,NULL,'If Receive Sample 2nd Time','yesno','2nd_Time_Receive',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'seminalinvasion',NULL,'pathology_review',NULL,113,NULL,NULL,'select','SeminalInvasion','0, No \\n 1, Yes \\n 2, N/A',NULL,NULL,NULL,NULL,NULL,'[tumor_origin] = \'2\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'shipmethod',NULL,'id_shipping',NULL,13,NULL,NULL,'select','ShipMethod','1, FedEx \\n 2, USPS \\n 3, UPS \\n 4, ByPerson \\n 5, Others',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'shipmethod2',NULL,'id_shipping',NULL,33,NULL,NULL,'select','ShipMethod2','1, FedEx \\n 2, USPS \\n 3, UPS \\n 4, ByPerson \\n 5, Others',NULL,NULL,NULL,NULL,NULL,'[secondtime_getsample] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'shipmethod3',NULL,'id_shipping',NULL,51,NULL,NULL,'select','ShipMethod3','1, FedEx \\n 2, USPS \\n 3, UPS \\n 4, ByPerson \\n 5, Others',NULL,NULL,NULL,NULL,NULL,'[thirdtime_getsample] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'slide_information_complete',NULL,'slide_information',NULL,179,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'slide_tracking_complete',NULL,'slide_tracking',NULL,198,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'slideloc_1',NULL,'slide_information',NULL,148,NULL,NULL,'text','SlideLoc_1',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'slideloc_metmetastatic',NULL,'slide_information',NULL,169,NULL,NULL,'text','SlideLoc_Metmetastatic',NULL,NULL,NULL,NULL,NULL,'soft_typed','[is_there_metastatic_tumor] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'slideloc_precancer',NULL,'slide_information',NULL,177,NULL,NULL,'text','SlideLoc_Precancer',NULL,NULL,NULL,NULL,NULL,'soft_typed','[is_there_precancer] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'specify_colon_clin',NULL,'pathology_review',NULL,116,NULL,NULL,'text','If others_specify',NULL,NULL,NULL,NULL,NULL,'soft_typed','[tumor_origin] = \'3\' and [clin_giag_colon] = \'8\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'specify_colon_lab',NULL,'pathology_review',NULL,118,NULL,NULL,'text','If others_specify',NULL,NULL,NULL,NULL,NULL,'soft_typed','[tumor_origin] = \'3\' and [lab_diagn_colon] = \'8\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'specify_if_other_type_br',NULL,'pathology_review',NULL,87,NULL,NULL,'text','Specify_If_Other_Type_Br',NULL,NULL,NULL,NULL,NULL,'soft_typed','[tumor_origin] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'specify_if_other_type_pro',NULL,'pathology_review',NULL,104,NULL,NULL,'text','Specify_If_Other_type_Pro',NULL,NULL,NULL,NULL,NULL,'soft_typed','[tumor_origin] = \'2\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'specify_other_location',NULL,'pathology_review',NULL,68,NULL,NULL,'text','Specify_Other_Location',NULL,NULL,NULL,NULL,NULL,'soft_typed','[tumor_origin] = \'5\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'specify_other_origin',NULL,'pathology_review',NULL,63,NULL,NULL,'text','Specify_Other_Origin',NULL,NULL,NULL,NULL,NULL,'soft_typed','[tumor_origin] = \'5\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'stainedslide_received',NULL,'id_shipping',NULL,18,NULL,NULL,'text','StainedSlide_Received',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'stainedslide_received2',NULL,'id_shipping',NULL,38,NULL,NULL,'text','StainedSlide_Received2',NULL,NULL,'float',NULL,NULL,'soft_typed','[secondtime_getsample] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'stainedslide_received3',NULL,'id_shipping',NULL,56,NULL,NULL,'text','StainedSlide_Received3',NULL,NULL,'float',NULL,NULL,'soft_typed','[thirdtime_getsample] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'suffix',NULL,'id_shipping',NULL,6,NULL,NULL,'text','Suffix',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'surgical_margin_cancer_pre',NULL,'pathology_review',NULL,83,NULL,NULL,'select','Surgical margin cancer present','0, No \\n 1, Yes \\n 2, N/A',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'ten_um_met_currentquant',NULL,'slide_information',NULL,168,NULL,NULL,'text','10um_Met_CurrentQuant',NULL,NULL,NULL,NULL,NULL,'soft_typed','[is_there_metastatic_tumor] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'ten_um_met_quant',NULL,'slide_information',NULL,167,NULL,NULL,'text','10um_Met_Quant',NULL,NULL,NULL,NULL,NULL,'soft_typed','[is_there_metastatic_tumor] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'ten_um_nor_currquant',NULL,'slide_information',NULL,147,NULL,NULL,'text','10um_Nor_CurrQuant',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'ten_um_nor_currquant2',NULL,'slide_information',NULL,159,NULL,NULL,'text','10um_Nor_CurrQuant2',NULL,NULL,'float',NULL,NULL,'soft_typed','[is_there_another_accnumber] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'ten_um_nor_quant',NULL,'slide_information',NULL,146,NULL,NULL,'text','10um_Nor_Quant',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'ten_um_nor_quant2',NULL,'slide_information',NULL,158,NULL,NULL,'text','10um_Nor_Quant2',NULL,NULL,'float',NULL,NULL,'soft_typed','[is_there_another_accnumber] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'ten_um_precancer_curquant',NULL,'slide_information',NULL,176,NULL,NULL,'text','10um_Precancer_CurQuant',NULL,NULL,NULL,NULL,NULL,'soft_typed','[is_there_precancer] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'ten_um_precancer_quant',NULL,'slide_information',NULL,175,NULL,NULL,'text','10um_Precancer_Quant',NULL,NULL,NULL,NULL,NULL,'soft_typed','[is_there_precancer] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'ten_um_tumor_currquant',NULL,'slide_information',NULL,143,NULL,NULL,'text','10um_Tumor_CurrQuant',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'ten_um_tumor_currquant2',NULL,'slide_information',NULL,155,NULL,NULL,'text','10um_Tumor_CurrQuant2',NULL,NULL,'float',NULL,NULL,'soft_typed','[is_there_another_accnumber] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'ten_um_tumor_quant',NULL,'slide_information',NULL,142,NULL,NULL,'text','10um_Tumor_Quant',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'ten_um_tumor_quant2',NULL,'slide_information',NULL,154,NULL,NULL,'text','10um_Tumor_Quant2',NULL,NULL,'float',NULL,NULL,'soft_typed','[is_there_another_accnumber] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'thirdtime_getsample',NULL,'id_shipping',NULL,43,NULL,'If Receive Sample 3rd Time','yesno','3rd_Time_Receive',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'tma_ca_pos1',NULL,'tma_information','TMA Information',180,NULL,NULL,'text','TMA_Ca_pos1',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'tma_ca_pos2',NULL,'tma_information',NULL,181,NULL,NULL,'text','TMA_Ca_pos2',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'tma_ca_pos3',NULL,'tma_information',NULL,187,NULL,NULL,'text','TMA_Ca_pos3',NULL,NULL,NULL,NULL,NULL,'soft_typed','[another_accnumber] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'tma_ca_pos4',NULL,'tma_information',NULL,188,NULL,NULL,'text','TMA_Ca_pos4',NULL,NULL,NULL,NULL,NULL,'soft_typed','[another_accnumber] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'tma_information_complete',NULL,'tma_information',NULL,193,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'tma_metastatic_pos',NULL,'tma_information',NULL,185,NULL,NULL,'text','TMA Metastatic_pos1',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'tma_metastatic_pos2',NULL,'tma_information',NULL,192,NULL,NULL,'text','TMA Metastatic_pos2',NULL,NULL,NULL,NULL,NULL,'soft_typed','[another_accnumber] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'tma_nor_pos1',NULL,'tma_information',NULL,182,NULL,NULL,'text','TMA_Nor_pos1',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'tma_nor_pos2',NULL,'tma_information',NULL,183,NULL,NULL,'text','TMA_Nor_pos2',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'tma_nor_pos3',NULL,'tma_information',NULL,189,NULL,NULL,'text','TMA_Nor_pos3',NULL,NULL,NULL,NULL,NULL,'soft_typed','[another_accnumber] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'tma_nor_pos4',NULL,'tma_information',NULL,190,NULL,NULL,'text','TMA_Nor_pos4',NULL,NULL,NULL,NULL,NULL,'soft_typed','[another_accnumber] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'tma_preca_pos',NULL,'tma_information',NULL,184,NULL,NULL,'text','TMA_ PreCa_pos1',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'tma_preca_pos2',NULL,'tma_information',NULL,191,NULL,NULL,'text','TMA_ PreCa_pos2',NULL,NULL,NULL,NULL,NULL,'soft_typed','[another_accnumber] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'tnm_breast_tumor',NULL,'pathology_review',NULL,99,NULL,NULL,'select','TNMbreast_PrimTum(T)','1, TX:Primary tumor cannot be assessed \\n 2, T0:No evidence of primary tumor \\n 3, Tis:DCIS/LCIS/Paget\'s dis w/o associated tumor \\n 4, T1mic:Microinvasion <=0.1 cm \\n 5, T1a:>0.1 but <=0.5 cm \\n 6, T1b:>0.5 cm but <=1.0 cm \\n 7, T1c:>1.0 cm but <=2.0 cm \\n 8, T2:Tumor >2.0 cm but <=5.0 cm \\n 9, T3:Tumor >5.0 cm \\n 10, T4a:Any size with direct extension to chest wall \\n 11, T4b:skin Edema/ulceration;satellite skin nodules \\n 12, T4c:Both of T4a and T4b \\n 13, T4d:Inflammatory carcinoma',NULL,NULL,NULL,NULL,NULL,'[tumor_origin] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'tnm_stage',NULL,'pathology_review',NULL,137,NULL,NULL,'text','TNM_Stage',NULL,NULL,NULL,NULL,NULL,'soft_typed','[tumor_origin] = \'5\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'tnmbreast_distantmetast_m',NULL,'pathology_review',NULL,101,NULL,NULL,'select','TNMbreast_DistantMetast (M)','1, MX: cannot be assessed \\n 2, M0: No distant metastasis \\n 3, M1: yes includes ipsilateral supraclavicular LNs',NULL,NULL,NULL,NULL,NULL,'[tumor_origin] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'tnmbreast_ln_n',NULL,'pathology_review',NULL,100,NULL,NULL,'select','TNMbreast_LN (N)','1, NX: Regional LNs cannot be assessed \\n 2, N0: No regional LNs metastasis \\n 3, N1: Movable ipsilateral axillary LN(s) \\n 4, N2: Ipsilateral axillary LN(s) fixed \\n 5, N3: Ipsilateral internal mammary LN(s) \\n 6, pNX: Regional LNs cannot be assessed \\n 7, pN0: No regional LNs metastasis \\n 8, pN1: movable ipsilateral axillary LN(s) \\n 9, pN1a:Only micrometastasis <=0.2 cm \\n 10, pN1b: Metastasis any >0.2 cm \\n 11, pN1bi:1 to 3 LNs, any >0.2 cm and all <2.0 cm \\n 12, pN1bii: >=4 LN3, any >0.2 cm and all <2.0 cm \\n 13, pN1biii: beyond LN capsule,metastasis <2.0 cm \\n 14, pN1biv: Metastasis to a LN >=2.0 cm \\n 15, pN2: to ipsilateral axillaryLN(s) fixed \\n 16, pN3: to ipsilateral internal mammary LN(s) \\n 17, pN0(i+)',NULL,NULL,NULL,NULL,NULL,'[tumor_origin] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'tnmcolon_m',NULL,'pathology_review',NULL,123,NULL,NULL,'select','TNMcolon_M','M0, M0 No distant spread \\n M1a, M1a to 1 distant organ or set of distant LNs \\n M1b, M1b to >1 or distant parts peritoneum \\n MX, MX',NULL,NULL,NULL,NULL,NULL,'[tumor_origin] = \'3\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'tnmcolon_n',NULL,'pathology_review',NULL,122,NULL,NULL,'select','TNMcolon_N','Nx, Nx incomplete information. \\n N0, N0 No cancer in nearby LNs \\n N1a, N1a in 1 nearby LN \\n N1b, N1b in 2 to 3 nearby LNs \\n N1c, N1c cancer cells in areas of fat near LN, but not in LNs \\n N2a, N2a in 4 to 6 nearby LN \\n N2b, N2b in 7 or more nearby LNs',NULL,NULL,NULL,NULL,NULL,'[tumor_origin] = \'3\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'tnmcolon_t',NULL,'pathology_review',NULL,121,NULL,NULL,'select','TNMcolon_T','Tx, Tx \\n Tis, Tis earliest stage (in situ) involves only mucosa \\n T1, T1 through the muscularis mucosa \\n T2, T2 through submucosa into muscularis propria \\n T3, T3 through muscularis propria into outermost layers \\n T4a, T4a through serosa/visceral peritoneum \\n T4b, T4b through the wall attach/invade nearby tissues',NULL,NULL,NULL,NULL,NULL,'[tumor_origin] = \'3\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'tnmlung_m',NULL,'pathology_review',NULL,132,NULL,NULL,'select','TNMlung_M','13, MX \\n 14, M0 \\n 15, M1 Distant metastasis, includes separate tumour nodule(s) in different lobe',NULL,NULL,NULL,NULL,NULL,'[tumor_origin] = \'4\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'tnmlung_n',NULL,'pathology_review',NULL,131,NULL,NULL,'select','TNMlung_N','8, NX \\n 9, N0 \\n 10, N1 Ipsilateral peribronchial/ipsilateral hilar LNs and intrapulmonary LNs \\n 11, N2 ipsilateral mediastinal/subcarinal LNs \\n 12, N3 contralateral mediastinal, contralateral hilar, ipsilateral or contralateral scalene, or supraclavicular LNs',NULL,NULL,NULL,NULL,NULL,'[tumor_origin] = \'4\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'tnmlung_t',NULL,'pathology_review',NULL,130,NULL,NULL,'select','TNMlung_T','1, TX \\n 2, T0 No evidence of primary tumour \\n 3, Tis Carcinoma in situ \\n 4, T1 <= 3 cm, without invasion \\n 5, T2 > 3 cm; or involves main bronchus(>2 cm distal to carina)/visceral pleura; or Associated with atelectasis or obstructive pneumonitis that does not involve entire lung \\n 6, T3 any size that directly invades any of:chest wall, diaphragm, mediastinal pleura, parietal pericardium; or tumour in main bronchus < 2 cm distal to carina but without involvement of carina; or associated atelectasis or obstructive pneumonitis of entire lung \\n 7, T4 any size that invades any of: mediastinum, heart, great vessels, trachea, oesophagus, vertebral body, carina; separate tumour nodule(s) in same lobe; tumour with malignant pleural effusion',NULL,NULL,NULL,NULL,NULL,'[tumor_origin] = \'4\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'tnmprostate_m',NULL,'pathology_review',NULL,111,NULL,NULL,'select','TNMprostate_M','1, M0: spread only regionally in pelvic area \\n 2, M1: spread beyond pelvic area \\n 3, MX',NULL,NULL,NULL,NULL,NULL,'[tumor_origin] = \'2\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'tnmprostate_n',NULL,'pathology_review',NULL,110,NULL,NULL,'select','TNMprostate_N','1, N0: not to pelvic LN \\n 2, N1: a single pelvic LN,<= 2 cm \\n 3, N2: a single pelvic LN,2-5cm \\n 4, N3: >5 cm in size \\n 5, NX',NULL,NULL,NULL,NULL,NULL,'[tumor_origin] = \'2\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'tnmprostate_t',NULL,'pathology_review',NULL,109,NULL,NULL,'select','TNMprostate_T','1, T1: Microscopic, DRE/Ultrasound undetectable \\n 2, T1a: <=5 percent \\n 3, T1b: >5 percent \\n 4, T1c: as F/U of screening w/ high PSA \\n 5, T2: within prost, DRE/ultrasound detectable \\n 6, T2a: >half of one lobe \\n 7, T2b: >half of one lobe,DRE detectable often \\n 8, T2c: involve both lobes \\n 9, T3: surrounding tissues or seminal vesicles \\n 10, T3a: outside prostate on one side \\n 11, T3b: outside prostate on both sides \\n 12, T3c: to one or both seminal tubes \\n 13, T4a: to bladder or rectum \\n 14, T4b: beyond prostate or levator muscles \\n 15, TX',NULL,NULL,NULL,NULL,NULL,'[tumor_origin] = \'2\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'trackingnumber',NULL,'id_shipping',NULL,14,NULL,NULL,'text','ReceiveTracking',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'trc_id',NULL,'id_shipping',NULL,2,NULL,NULL,'text','TRC ID',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'tumor_location',NULL,'pathology_review',NULL,64,NULL,NULL,'select','Location_Breast_Prostate','1, Left \\n 2, Right \\n 3, Bilateral \\n 4, Multiple \\n 5, Unclear','Multiple means 2 or more',NULL,NULL,NULL,NULL,'[tumor_origin] = \'1\' or [tumor_origin] = \'2\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'tumor_location_colorectum',NULL,'pathology_review',NULL,65,NULL,NULL,'select','Location_Colorectum','1, Appendix \\n 2, Cecum \\n 3, Ascending \\n 4, Hepatic Flexure \\n 5, Transverse \\n 6, Splenic Flexure \\n 7, Descending \\n 8, Sigmoid \\n 9, Rectum \\n 10, Anus \\n 11, Left \\n 12, Right \\n 13, Unclear',NULL,NULL,NULL,NULL,NULL,'[tumor_origin] = \'3\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'tumor_location_lung',NULL,'pathology_review',NULL,66,NULL,NULL,'select','Location_Lung','1, Right Upper Lobe \\n 2, Right Middle Lobe \\n 3, Right Lower Lobe \\n 4, Left Upper Lobe \\n 5, Left Lower Lobe \\n 6, Right Bronchus \\n 7, Left Bronchus \\n 8, Right \\n 9, Left \\n 10, Unclear \\n 11, Others (specify it)',NULL,NULL,NULL,NULL,NULL,'[tumor_origin] = \'4\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'tumor_origin',NULL,'pathology_review','Pathology Review',62,NULL,'Tumor Origin and Location','select','Tumor_Origin','1, Breast \\n 2, Prostate \\n 3, Colorectum \\n 4, Lung \\n 5, Others',NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'unstainedslide_received',NULL,'id_shipping',NULL,19,NULL,NULL,'text','UnstainedSlide_Received',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'unstainedslide_received2',NULL,'id_shipping',NULL,39,NULL,NULL,'text','UnstainedSlide_Received2',NULL,NULL,'float',NULL,NULL,'soft_typed','[secondtime_getsample] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'unstainedslide_received3',NULL,'id_shipping',NULL,57,NULL,NULL,'text','UnstainedSlide_Received3',NULL,NULL,'float',NULL,NULL,'soft_typed','[thirdtime_getsample] = \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'vascular_invasion',NULL,'pathology_review',NULL,82,NULL,NULL,'select','Vascular invasion present','0, No \\n 1, Yes \\n 2, N/A',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(8,'whichslidepulled1',NULL,'slide_tracking',NULL,196,NULL,NULL,'text','WhichSlidePulled1',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(9,'address','1','participant_info_survey',NULL,8,NULL,NULL,'textarea','Street, City, State, ZIP',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(9,'complete_study',NULL,'completion_data','Completion Data (to be entered by study personnel only)',22,NULL,'This form is to be filled out by study personnel.','yesno','Has patient completed study?',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(9,'completion_data_complete',NULL,'completion_data',NULL,29,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(9,'consent',NULL,'prescreening_survey',NULL,4,NULL,NULL,'checkbox','By checking this box, I certify that I am at least 18 years old and that I give my consent freely to participant in this study.','1, I consent',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(9,'date_visit_4',NULL,'completion_data',NULL,25,NULL,NULL,'text','Date of last visit',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(9,'discharge_date_4',NULL,'completion_data',NULL,26,NULL,NULL,'text','Date of hospital discharge',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(9,'discharge_summary_4',NULL,'completion_data',NULL,27,NULL,NULL,'select','Discharge summary in patients binder?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(9,'dob',NULL,'prescreening_survey',NULL,2,NULL,'Please fill out the information below.','text','Date of birth',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(9,'email','1','prescreening_survey',NULL,2.1,NULL,NULL,'text','E-mail address',NULL,NULL,'email',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(9,'ethnicity',NULL,'participant_info_survey',NULL,11,NULL,NULL,'radio','Ethnicity','0, Hispanic or Latino \\n 1, NOT Hispanic or Latino \\n 2, Unknown / Not Reported',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,'LH',NULL,NULL,NULL,NULL),(9,'first_name','1','participant_info_survey','Participant Info Survey',6,NULL,'As a participant in this study, please answer the questions below. Thank you!','text','First Name',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(9,'has_diabetes',NULL,'prescreening_survey',NULL,3,NULL,NULL,'truefalse','I currently have Type 2 Diabetes',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(9,'height',NULL,'participant_info_survey',NULL,14,NULL,NULL,'text','Height (cm)',NULL,NULL,'float','130','215','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(9,'last_name','1','participant_info_survey',NULL,7,NULL,NULL,'text','Last Name',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(9,'participant_id',NULL,'prescreening_survey','Pre-Screening Survey',1,NULL,NULL,'text','Participant ID',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(9,'participant_info_survey_complete',NULL,'participant_info_survey',NULL,16,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(9,'participant_morale_questionnaire_complete',NULL,'participant_morale_questionnaire',NULL,21,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(9,'pmq1',NULL,'participant_morale_questionnaire','Participant Morale Questionnaire',17,NULL,'As a participant in this study, please answer the questions below. Thank you!','select','On average, how many pills did you take each day last week?','0, Less than 5 \\n 1, 5-10 \\n 2, 6-15 \\n 3, Over 15',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(9,'pmq2',NULL,'participant_morale_questionnaire',NULL,18,NULL,NULL,'select','Using the handout, which level of dependence do you feel you are currently at?','0, 0 \\n 1, 1 \\n 2, 2 \\n 3, 3 \\n 4, 4 \\n 5, 5',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(9,'pmq3',NULL,'participant_morale_questionnaire',NULL,19,NULL,NULL,'yesno','Would you be willing to discuss your experiences with a psychiatrist?',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(9,'pmq4',NULL,'participant_morale_questionnaire',NULL,20,NULL,NULL,'select','How open are you to further testing?','0, Not open \\n 1, Undecided \\n 2, Very open',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(9,'prescreening_survey_complete',NULL,'prescreening_survey',NULL,5,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(9,'race',NULL,'participant_info_survey',NULL,12,NULL,NULL,'select','Race','0, American Indian/Alaska Native \\n 1, Asian \\n 2, Native Hawaiian or Other Pacific Islander \\n 3, Black or African American \\n 4, White \\n 5, More Than One Race \\n 6, Unknown / Not Reported',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(9,'sex',NULL,'participant_info_survey',NULL,13,NULL,NULL,'radio','Gender','0, Female \\n 1, Male',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(9,'study_comments',NULL,'completion_data',NULL,28,NULL,NULL,'textarea','Comments',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(9,'telephone_1','1','participant_info_survey',NULL,9,NULL,NULL,'text','Phone number',NULL,'Include Area Code','phone',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(9,'weight',NULL,'participant_info_survey',NULL,15,NULL,NULL,'text','Weight (kilograms)',NULL,NULL,'int','35','200','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(9,'withdraw_date',NULL,'completion_data',NULL,23,NULL,NULL,'text','Put a date if patient withdrew study',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(9,'withdraw_reason',NULL,'completion_data',NULL,24,NULL,NULL,'select','Reason patient withdrew from study','0, Non-compliance \\n 1, Did not wish to continue in study \\n 2, Could not tolerate the supplement \\n 3, Hospitalization \\n 4, Other',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(10,'address','1','participant_info_survey',NULL,8,NULL,NULL,'textarea','Street, City, State, ZIP',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(10,'choices',NULL,'participant_morale_questionnaire',NULL,19,NULL,'Concerning the past week, how do you feel about ...','radio','The choices you made','1, Not satisfied at all \\n 2, Somewhat dissatisfied \\n 3, Indifferent \\n 4, Somewhat satisfied \\n 5, Very satisfied',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,'feelings_matrix',NULL),(10,'complete_study',NULL,'completion_data','Completion Data (to be entered by study personnel only)',24,NULL,'This form is to be filled out by study personnel.','yesno','Has patient completed study?',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(10,'completion_data_complete',NULL,'completion_data',NULL,31,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(10,'consent',NULL,'prescreening_survey',NULL,4,NULL,NULL,'checkbox','By checking this box, I certify that I am at least 18 years old and that I give my consent freely to participant in this study.','1, I consent',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(10,'date_visit_4',NULL,'completion_data',NULL,27,NULL,NULL,'text','Date of last visit',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(10,'discharge_date_4',NULL,'completion_data',NULL,28,NULL,NULL,'text','Date of hospital discharge',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(10,'discharge_summary_4',NULL,'completion_data',NULL,29,NULL,NULL,'select','Discharge summary in patients binder?','0, No \\n 1, Yes',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(10,'dob',NULL,'prescreening_survey',NULL,2,NULL,'Please fill out the information below.','text','Date of birth',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(10,'email','1','prescreening_survey',NULL,2.1,NULL,NULL,'text','E-mail address',NULL,NULL,'email',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(10,'ethnicity',NULL,'participant_info_survey',NULL,11,NULL,NULL,'radio','Ethnicity','0, Hispanic or Latino \\n 1, NOT Hispanic or Latino \\n 2, Unknown / Not Reported',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,'LH',NULL,NULL,NULL,NULL),(10,'family',NULL,'participant_morale_questionnaire',NULL,22,NULL,NULL,'radio','Your family life','1, Not satisfied at all \\n 2, Somewhat dissatisfied \\n 3, Indifferent \\n 4, Somewhat satisfied \\n 5, Very satisfied',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,'feelings_matrix',NULL),(10,'first_name','1','participant_info_survey','Participant Info Survey',6,NULL,'As a participant in this study, please answer the questions below. Thank you!','text','First Name',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(10,'has_diabetes',NULL,'prescreening_survey',NULL,3,NULL,NULL,'truefalse','I currently have Type 2 Diabetes',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(10,'height',NULL,'participant_info_survey',NULL,14,NULL,NULL,'text','Height (cm)',NULL,NULL,'float','130','215','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(10,'job',NULL,'participant_morale_questionnaire',NULL,21,NULL,NULL,'radio','Your job','1, Not satisfied at all \\n 2, Somewhat dissatisfied \\n 3, Indifferent \\n 4, Somewhat satisfied \\n 5, Very satisfied',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,'feelings_matrix',NULL),(10,'last_name','1','participant_info_survey',NULL,7,NULL,NULL,'text','Last Name',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(10,'life',NULL,'participant_morale_questionnaire',NULL,20,NULL,NULL,'radio','Your life overall','1, Not satisfied at all \\n 2, Somewhat dissatisfied \\n 3, Indifferent \\n 4, Somewhat satisfied \\n 5, Very satisfied',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,'feelings_matrix',NULL),(10,'participant_id',NULL,'prescreening_survey','Pre-Screening Survey',1,NULL,NULL,'text','Participant ID',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(10,'participant_info_survey_complete',NULL,'participant_info_survey',NULL,16,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(10,'participant_morale_questionnaire_complete',NULL,'participant_morale_questionnaire',NULL,23,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(10,'pmq1',NULL,'participant_morale_questionnaire','Participant Morale Questionnaire',17,NULL,'As a participant in this study, please answer the questions below concerning the PAST WEEK. Thank you!','select','On average, how many pills did you take each day last week?','0, Less than 5 \\n 1, 5-10 \\n 2, 6-15 \\n 3, Over 15',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(10,'pmq2',NULL,'participant_morale_questionnaire',NULL,18,NULL,NULL,'select','Using the handout, which level of dependence do you feel you are currently at?','0, 0 \\n 1, 1 \\n 2, 2 \\n 3, 3 \\n 4, 4 \\n 5, 5',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(10,'prescreening_survey_complete',NULL,'prescreening_survey',NULL,5,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(10,'race',NULL,'participant_info_survey',NULL,12,NULL,NULL,'select','Race','0, American Indian/Alaska Native \\n 1, Asian \\n 2, Native Hawaiian or Other Pacific Islander \\n 3, Black or African American \\n 4, White \\n 5, More Than One Race \\n 6, Unknown / Not Reported',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(10,'sex',NULL,'participant_info_survey',NULL,13,NULL,NULL,'radio','Gender','0, Female \\n 1, Male',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(10,'study_comments',NULL,'completion_data',NULL,30,NULL,NULL,'textarea','Comments',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(10,'telephone_1','1','participant_info_survey',NULL,9,NULL,NULL,'text','Phone number',NULL,'Include Area Code','phone',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(10,'weight',NULL,'participant_info_survey',NULL,15,NULL,NULL,'text','Weight (kilograms)',NULL,NULL,'int','35','200','soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(10,'withdraw_date',NULL,'completion_data',NULL,25,NULL,NULL,'text','Put a date if patient withdrew study',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(10,'withdraw_reason',NULL,'completion_data',NULL,26,NULL,NULL,'select','Reason patient withdrew from study','0, Non-compliance \\n 1, Did not wish to continue in study \\n 2, Could not tolerate the supplement \\n 3, Hospitalization \\n 4, Other',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(11,'calc',NULL,'survey',NULL,8,NULL,NULL,'calc','Your favorite number above multiplied by 4 is:','[number]*4','[number] x 4 = [calc]',NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(11,'confirm_name',NULL,'survey',NULL,9,NULL,NULL,'radio','Please confirm your name','0, [first_name] Harris \\n 1, [first_name] [last_name] \\n 2, [first_name] Taylor \\n 3, [first_name] deGrasse Tyson',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(11,'confirm_name_error',NULL,'survey',NULL,10,NULL,NULL,'descriptive','<div class=\"red\" style=\"padding:30px;\"><b>ERROR:</b> Please try again!</div>',NULL,NULL,NULL,NULL,NULL,NULL,'[confirm_name] != \'\' and [confirm_name] != \'1\'',0,NULL,0,NULL,NULL,NULL,NULL,NULL),(11,'date_today',NULL,'survey',NULL,4,NULL,NULL,'text','[first_name], please enter today\'s date?',NULL,NULL,'date_mdy',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(11,'first_name',NULL,'survey',NULL,2,NULL,'Section 1','text','Your first name',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,1,NULL,0,NULL,NULL,NULL,NULL,NULL),(11,'ice_cream',NULL,'survey',NULL,5,NULL,NULL,'radio','What is your favorite ice cream?','1, Chocolate \\n 2, Vanilla \\n 3, Strawberry',NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,0,NULL,NULL,NULL,NULL,NULL),(11,'last_name',NULL,'survey',NULL,3,NULL,NULL,'text','Your last name',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,1,NULL,0,NULL,NULL,NULL,NULL,NULL),(11,'number',NULL,'survey',NULL,7,NULL,NULL,'text','Enter your favorite number',NULL,NULL,'int',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(11,'participant_id',NULL,'survey','Example Survey',1,NULL,NULL,'text','Participant ID',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(11,'review_answers',NULL,'survey',NULL,11,NULL,'Review answers','descriptive','Review your answers below:\n\n<div style=\"font-size:14px;color:red;\">Date: [date_today]\nName: [first_name] [last_name]\nFavorite ice cream: [ice_cream]\nFavorite number multiplied by 4: [calc]</div>\n\nIf all your responses look correct and you did not leave any blank, then click the Submit button below.',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(11,'slider',NULL,'survey',NULL,6,NULL,'Section 2','slider','How much do you like [ice_cream] ice cream?','Hate it | Indifferent | I love [ice_cream]!',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(11,'survey_complete',NULL,'survey',NULL,12,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(12,'c0362923',NULL,'cbc',NULL,8,NULL,NULL,'text','Hemoglobin:MCnc:Pt:Bld:Qn',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(12,'c0362923_units',NULL,'cbc',NULL,9,NULL,NULL,'text','Hemoglobin:MCnc:Pt:Bld:Qn units',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(12,'c0363876',NULL,'chemistry',NULL,20,NULL,NULL,'text','Alanine aminotransferase:CCnc:Pt:Ser/Plas:Qn',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(12,'c0363876_units',NULL,'chemistry',NULL,21,NULL,NULL,'text','Alanine aminotransferase:CCnc:Pt:Ser/Plas:Qn units',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(12,'c0363885',NULL,'chemistry',NULL,22,NULL,NULL,'text','Albumin:MCnc:Pt:Ser/Plas:Qn',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(12,'c0363885_units',NULL,'chemistry',NULL,23,NULL,NULL,'text','Albumin:MCnc:Pt:Ser/Plas:Qn units',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(12,'c0364055',NULL,'chemistry',NULL,24,NULL,NULL,'text','Aspartate aminotransferase:CCnc:Pt:Ser/Plas:Qn',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(12,'c0364055_units',NULL,'chemistry',NULL,25,NULL,NULL,'text','Aspartate aminotransferase:CCnc:Pt:Ser/Plas:Qn units',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(12,'c0364101',NULL,'chemistry',NULL,28,NULL,NULL,'text','Bilirubin.glucuronidated+Bilirubin.albumin bound:MCnc:Pt:Ser/Plas:Qn',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(12,'c0364101_units',NULL,'chemistry',NULL,29,NULL,NULL,'text','Bilirubin.glucuronidated+Bilirubin.albumin bound:MCnc:Pt:Ser/Plas:Qn units',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(12,'c0364108',NULL,'chemistry',NULL,26,NULL,NULL,'text','Bilirubin:MCnc:Pt:Ser',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(12,'c0364108_units',NULL,'chemistry',NULL,27,NULL,NULL,'text','Bilirubin:MCnc:Pt:Ser units',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(12,'c0364294',NULL,'chemistry',NULL,30,NULL,NULL,'text','Creatinine [Mass/volume] in Serum or Plasma',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(12,'c0364294_units',NULL,'chemistry',NULL,31,NULL,NULL,'text','Creatinine [Mass/volume] in Serum or Plasma units',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(12,'c0364479',NULL,'chemistry',NULL,32,NULL,NULL,'text','Glucose:MCnc:Pt:Bld:Qn',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(12,'c0364479_units',NULL,'chemistry',NULL,33,NULL,NULL,'text','Glucose:MCnc:Pt:Bld:Qn units',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(12,'c0364961',NULL,'chemistry',NULL,34,NULL,NULL,'text','Potassium:SCnc:Pt:Bld:Qn',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(12,'c0364961_units',NULL,'chemistry',NULL,35,NULL,NULL,'text','Potassium:SCnc:Pt:Bld:Qn units',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(12,'c0365091',NULL,'chemistry',NULL,36,NULL,NULL,'text','Sodium:SCnc:Pt:Bld:Qn',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(12,'c0365091_units',NULL,'chemistry',NULL,37,NULL,NULL,'text','Sodium:SCnc:Pt:Bld:Qn units',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(12,'c0806020',NULL,'enrollment',NULL,5,NULL,NULL,'text','End Date',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(12,'c0942437',NULL,'cbc',NULL,12,NULL,NULL,'text','Lymphocytes:NCnc:Pt:Bld:Qn',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(12,'c0942437_units',NULL,'cbc',NULL,13,NULL,NULL,'text','Lymphocytes:NCnc:Pt:Bld:Qn units',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(12,'c0942461',NULL,'cbc',NULL,14,NULL,NULL,'text','Neutrophils:NCnc:Pt:Bld:Qn',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(12,'c0942461_units',NULL,'cbc',NULL,15,NULL,NULL,'text','Neutrophils:NCnc:Pt:Bld:Qn units',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(12,'c0942474',NULL,'cbc',NULL,16,NULL,NULL,'text','Platelets:NCnc:Pt:Bld:Qn',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(12,'c0942474_units',NULL,'cbc',NULL,17,NULL,NULL,'text','Platelets:NCnc:Pt:Bld:Qn units',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(12,'c0945357',NULL,'cbc',NULL,10,NULL,NULL,'text','Leukocytes:NCnc:Pt:Bld:Qn',NULL,NULL,'float',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(12,'c0945357_units',NULL,'cbc',NULL,11,NULL,NULL,'text','Leukocytes:NCnc:Pt:Bld:Qn units',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(12,'c1301894',NULL,'enrollment',NULL,3,NULL,NULL,'text','Medical record number',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(12,'c2826694',NULL,'enrollment',NULL,2,NULL,NULL,'text','Subject Identifier',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(12,'c2985782',NULL,'enrollment',NULL,4,NULL,NULL,'text','Informed Consent Date',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(12,'cbc_complete',NULL,'cbc',NULL,18,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(12,'cbc_taken_date',NULL,'cbc','Cbc',7,NULL,NULL,'text','Date Taken',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,1,NULL,0,NULL,NULL,NULL,NULL,NULL),(12,'chemistry_complete',NULL,'chemistry',NULL,38,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(12,'chemistry_taken_date',NULL,'chemistry','Chemistry',19,NULL,NULL,'text','Date Taken',NULL,NULL,'date_ymd',NULL,NULL,'soft_typed',NULL,1,NULL,0,NULL,NULL,NULL,NULL,NULL),(12,'enrollment_complete',NULL,'enrollment',NULL,6,NULL,'Form Status','select','Complete?','0, Incomplete \\n 1, Unverified \\n 2, Complete',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL),(12,'record_id',NULL,'enrollment','Enrollment',1,NULL,NULL,'text','Record ID',NULL,NULL,NULL,NULL,NULL,'soft_typed',NULL,0,NULL,0,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `redcap_metadata` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_metadata_archive`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_metadata_archive` (
  `project_id` int(10) NOT NULL DEFAULT '0',
  `field_name` varchar(100) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `field_phi` varchar(5) COLLATE utf8_unicode_ci DEFAULT NULL,
  `form_name` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `form_menu_description` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `field_order` float DEFAULT NULL,
  `field_units` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `element_preceding_header` mediumtext COLLATE utf8_unicode_ci,
  `element_type` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `element_label` mediumtext COLLATE utf8_unicode_ci,
  `element_enum` mediumtext COLLATE utf8_unicode_ci,
  `element_note` mediumtext COLLATE utf8_unicode_ci,
  `element_validation_type` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `element_validation_min` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `element_validation_max` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `element_validation_checktype` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `branching_logic` text COLLATE utf8_unicode_ci,
  `field_req` int(1) NOT NULL DEFAULT '0',
  `edoc_id` int(10) DEFAULT NULL COMMENT 'image/file attachment',
  `edoc_display_img` int(1) NOT NULL DEFAULT '0',
  `custom_alignment` enum('LH','LV','RH','RV') COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'RV = NULL = default',
  `stop_actions` text COLLATE utf8_unicode_ci,
  `question_num` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `grid_name` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Unique name of grid group',
  `misc` text COLLATE utf8_unicode_ci COMMENT 'Miscellaneous field attributes',
  `pr_id` int(10) DEFAULT NULL,
  UNIQUE KEY `project_field_prid` (`project_id`,`field_name`,`pr_id`),
  KEY `project_id_form` (`project_id`,`form_name`),
  KEY `field_name` (`field_name`),
  KEY `pr_id` (`pr_id`),
  KEY `edoc_id` (`edoc_id`),
  CONSTRAINT `redcap_metadata_archive_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `redcap_projects` (`project_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `redcap_metadata_archive_ibfk_3` FOREIGN KEY (`pr_id`) REFERENCES `redcap_metadata_prod_revisions` (`pr_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `redcap_metadata_archive_ibfk_4` FOREIGN KEY (`edoc_id`) REFERENCES `redcap_edocs_metadata` (`doc_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_metadata_archive` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_metadata_archive` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_metadata_prod_revisions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_metadata_prod_revisions` (
  `pr_id` int(10) NOT NULL AUTO_INCREMENT,
  `project_id` int(10) NOT NULL DEFAULT '0',
  `ui_id_requester` int(10) DEFAULT NULL,
  `ui_id_approver` int(10) DEFAULT NULL,
  `ts_req_approval` datetime DEFAULT NULL,
  `ts_approved` datetime DEFAULT NULL,
  PRIMARY KEY (`pr_id`),
  KEY `project_user` (`project_id`,`ui_id_requester`),
  KEY `project_approved` (`project_id`,`ts_approved`),
  KEY `ui_id_requester` (`ui_id_requester`),
  KEY `ui_id_approver` (`ui_id_approver`),
  CONSTRAINT `redcap_metadata_prod_revisions_ibfk_3` FOREIGN KEY (`ui_id_approver`) REFERENCES `redcap_user_information` (`ui_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `redcap_metadata_prod_revisions_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `redcap_projects` (`project_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `redcap_metadata_prod_revisions_ibfk_2` FOREIGN KEY (`ui_id_requester`) REFERENCES `redcap_user_information` (`ui_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_metadata_prod_revisions` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_metadata_prod_revisions` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_metadata_temp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_metadata_temp` (
  `project_id` int(10) NOT NULL DEFAULT '0',
  `field_name` varchar(100) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `field_phi` varchar(5) COLLATE utf8_unicode_ci DEFAULT NULL,
  `form_name` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `form_menu_description` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `field_order` float DEFAULT NULL,
  `field_units` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `element_preceding_header` mediumtext COLLATE utf8_unicode_ci,
  `element_type` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `element_label` mediumtext COLLATE utf8_unicode_ci,
  `element_enum` mediumtext COLLATE utf8_unicode_ci,
  `element_note` mediumtext COLLATE utf8_unicode_ci,
  `element_validation_type` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `element_validation_min` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `element_validation_max` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `element_validation_checktype` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `branching_logic` text COLLATE utf8_unicode_ci,
  `field_req` int(1) NOT NULL DEFAULT '0',
  `edoc_id` int(10) DEFAULT NULL COMMENT 'image/file attachment',
  `edoc_display_img` int(1) NOT NULL DEFAULT '0',
  `custom_alignment` enum('LH','LV','RH','RV') COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'RV = NULL = default',
  `stop_actions` text COLLATE utf8_unicode_ci,
  `question_num` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `grid_name` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Unique name of grid group',
  `misc` text COLLATE utf8_unicode_ci COMMENT 'Miscellaneous field attributes',
  PRIMARY KEY (`project_id`,`field_name`),
  KEY `project_id_form` (`project_id`,`form_name`),
  KEY `field_name` (`field_name`),
  KEY `edoc_id` (`edoc_id`),
  CONSTRAINT `redcap_metadata_temp_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `redcap_projects` (`project_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `redcap_metadata_temp_ibfk_2` FOREIGN KEY (`edoc_id`) REFERENCES `redcap_edocs_metadata` (`doc_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_metadata_temp` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_metadata_temp` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_page_hits`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_page_hits` (
  `date` date NOT NULL,
  `page_name` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `page_hits` float NOT NULL DEFAULT '1',
  UNIQUE KEY `date` (`date`,`page_name`),
  KEY `page_name` (`page_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_page_hits` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_page_hits` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_project_checklist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_project_checklist` (
  `list_id` int(11) NOT NULL AUTO_INCREMENT,
  `project_id` int(10) DEFAULT NULL,
  `name` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`list_id`),
  UNIQUE KEY `project_name` (`project_id`,`name`),
  CONSTRAINT `redcap_project_checklist_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `redcap_projects` (`project_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_project_checklist` DISABLE KEYS */;
INSERT INTO `redcap_project_checklist` VALUES (1,7,'design'),(2,7,'modify_project'),(3,7,'modules');
/*!40000 ALTER TABLE `redcap_project_checklist` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_projects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_projects` (
  `project_id` int(10) NOT NULL AUTO_INCREMENT,
  `project_name` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `app_title` text COLLATE utf8_unicode_ci,
  `status` int(1) NOT NULL DEFAULT '0',
  `creation_time` datetime DEFAULT NULL,
  `production_time` datetime DEFAULT NULL,
  `inactive_time` datetime DEFAULT NULL,
  `created_by` int(10) DEFAULT NULL COMMENT 'FK from User Info',
  `draft_mode` int(1) NOT NULL DEFAULT '0',
  `surveys_enabled` int(1) NOT NULL DEFAULT '0' COMMENT '0 = forms only, 1 = survey+forms, 2 = single survey only',
  `repeatforms` int(1) NOT NULL DEFAULT '0',
  `scheduling` int(1) NOT NULL DEFAULT '0',
  `purpose` int(2) DEFAULT NULL,
  `purpose_other` text COLLATE utf8_unicode_ci,
  `show_which_records` int(1) NOT NULL DEFAULT '0',
  `__SALT__` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Alphanumeric hash unique to each project',
  `count_project` int(1) NOT NULL DEFAULT '1',
  `investigators` text COLLATE utf8_unicode_ci,
  `project_note` text COLLATE utf8_unicode_ci,
  `online_offline` int(1) NOT NULL DEFAULT '1',
  `auth_meth` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `double_data_entry` int(1) NOT NULL DEFAULT '0',
  `project_language` varchar(255) COLLATE utf8_unicode_ci NOT NULL DEFAULT 'English',
  `is_child_of` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `date_shift_max` int(10) NOT NULL DEFAULT '364',
  `institution` text COLLATE utf8_unicode_ci,
  `site_org_type` text COLLATE utf8_unicode_ci,
  `grant_cite` text COLLATE utf8_unicode_ci,
  `project_contact_name` text COLLATE utf8_unicode_ci,
  `project_contact_email` text COLLATE utf8_unicode_ci,
  `project_contact_prod_changes_name` text COLLATE utf8_unicode_ci,
  `project_contact_prod_changes_email` text COLLATE utf8_unicode_ci,
  `headerlogo` text COLLATE utf8_unicode_ci,
  `auto_inc_set` int(1) NOT NULL DEFAULT '0',
  `custom_data_entry_note` text COLLATE utf8_unicode_ci,
  `custom_index_page_note` text COLLATE utf8_unicode_ci,
  `order_id_by` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `custom_reports` mediumtext COLLATE utf8_unicode_ci COMMENT 'Legacy report builder',
  `report_builder` mediumtext COLLATE utf8_unicode_ci,
  `mobile_project` int(1) NOT NULL DEFAULT '0',
  `mobile_project_export_flag` int(1) NOT NULL DEFAULT '1',
  `disable_data_entry` int(1) NOT NULL DEFAULT '0',
  `google_translate_default` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `require_change_reason` int(1) NOT NULL DEFAULT '0',
  `dts_enabled` int(1) NOT NULL DEFAULT '0',
  `project_pi_firstname` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `project_pi_mi` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `project_pi_lastname` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `project_pi_email` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `project_pi_alias` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `project_pi_username` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `project_pi_pub_exclude` int(1) DEFAULT NULL,
  `project_pub_matching_institution` text COLLATE utf8_unicode_ci,
  `project_irb_number` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `project_grant_number` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `history_widget_enabled` int(1) NOT NULL DEFAULT '1',
  `secondary_pk` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'field_name of seconary identifier',
  `custom_record_label` text COLLATE utf8_unicode_ci,
  `display_project_logo_institution` int(1) NOT NULL DEFAULT '1',
  `imported_from_rs` int(1) NOT NULL DEFAULT '0' COMMENT 'If imported from REDCap Survey',
  `display_today_now_button` int(1) NOT NULL DEFAULT '1',
  `auto_variable_naming` int(1) NOT NULL DEFAULT '0',
  `randomization` int(1) NOT NULL DEFAULT '0',
  `enable_participant_identifiers` int(1) NOT NULL DEFAULT '0',
  `survey_email_participant_field` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Field name that stores participant email',
  `data_entry_trigger_url` text COLLATE utf8_unicode_ci COMMENT 'URL for sending Post request when a record is created or modified',
  `template_id` int(10) DEFAULT NULL COMMENT 'If created from a project template, the project_id of the template',
  `date_deleted` datetime DEFAULT NULL COMMENT 'Time that project was flagged for deletion',
  `data_resolution_enabled` int(1) NOT NULL DEFAULT '1' COMMENT '0=Disabled, 1=Field comment log, 2=Data Quality resolution workflow',
  `realtime_webservice_enabled` int(1) NOT NULL DEFAULT '0' COMMENT 'Is real-time web service enabled for external data import?',
  `realtime_webservice_offset_days` int(3) NOT NULL DEFAULT '1' COMMENT 'Default value of days offset',
  `realtime_webservice_offset_plusminus` enum('+','-','+-') COLLATE utf8_unicode_ci NOT NULL DEFAULT '+-' COMMENT 'Default value of plus-minus range for days offset',
  `last_logged_event` datetime DEFAULT NULL,
  PRIMARY KEY (`project_id`),
  UNIQUE KEY `project_name` (`project_name`),
  KEY `created_by` (`created_by`),
  KEY `template_id` (`template_id`),
  KEY `last_logged_event` (`last_logged_event`),
  CONSTRAINT `redcap_projects_ibfk_2` FOREIGN KEY (`created_by`) REFERENCES `redcap_user_information` (`ui_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `redcap_projects_ibfk_1` FOREIGN KEY (`template_id`) REFERENCES `redcap_projects` (`project_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='Stores project-level values';
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_projects` DISABLE KEYS */;
INSERT INTO `redcap_projects` VALUES (1,'redcap_demo_789df9','Classic Database',1,'2014-09-16 15:29:47','2014-09-16 15:29:47',NULL,NULL,0,0,0,0,NULL,NULL,0,NULL,0,NULL,NULL,1,'none',0,'English',NULL,364,'','','','','','','','',0,NULL,NULL,NULL,NULL,NULL,0,1,0,NULL,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,0,0,1,0,0,0,NULL,NULL,NULL,NULL,1,0,1,'+-',NULL),(2,'redcap_demo_97600d','Longitudinal Database (2 arms)',1,'2014-09-16 15:29:47','2014-09-16 15:29:47',NULL,NULL,0,0,1,0,NULL,NULL,0,NULL,0,NULL,NULL,1,'none',0,'English',NULL,364,'','','','','','','','',0,NULL,NULL,NULL,NULL,NULL,0,1,0,NULL,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,0,0,1,0,0,0,NULL,NULL,NULL,NULL,1,0,1,'+-',NULL),(3,'redcap_demo_1f66d7','Single Survey',1,'2014-09-16 15:29:48','2014-09-16 15:29:48',NULL,NULL,0,1,0,0,NULL,NULL,0,NULL,0,NULL,NULL,1,'none',0,'English',NULL,364,'','','','','','','','',1,NULL,NULL,NULL,NULL,NULL,0,1,0,NULL,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,0,0,1,0,0,0,NULL,NULL,NULL,NULL,1,0,1,'+-',NULL),(4,'redcap_demo_873daf','Longitudinal Database (1 arm)',1,'2014-09-16 15:29:48','2014-09-16 15:29:48',NULL,NULL,0,0,1,0,NULL,NULL,0,NULL,0,NULL,NULL,1,'none',0,'English',NULL,364,'','','','','','','','',0,NULL,NULL,NULL,NULL,NULL,0,1,0,NULL,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,0,0,1,0,0,0,NULL,NULL,NULL,NULL,1,0,1,'+-',NULL),(5,'redcap_demo_7633af','Basic Demography',1,'2014-09-16 15:29:48','2014-09-16 15:29:48',NULL,NULL,0,0,0,0,NULL,NULL,0,NULL,0,NULL,NULL,1,'none',0,'English',NULL,364,'','','','','','','','',0,NULL,NULL,NULL,NULL,NULL,0,1,0,NULL,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,0,0,1,0,0,0,NULL,NULL,NULL,NULL,1,0,1,'+-',NULL),(6,'redcap_demo_bffd55','Project Tracking Database',1,'2014-09-16 15:29:48','2014-09-16 15:29:48',NULL,NULL,0,0,0,0,NULL,NULL,0,NULL,0,NULL,NULL,1,'none',0,'English',NULL,364,'','','','','','','','',0,NULL,NULL,NULL,NULL,NULL,0,1,0,NULL,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,0,0,1,0,0,0,NULL,NULL,NULL,NULL,1,0,1,'+-',NULL),(7,'redcap_demo_44df3d','Randomized Clinical Trial',0,'2014-09-16 15:29:48','2014-09-16 15:29:48',NULL,NULL,0,0,0,0,NULL,NULL,0,NULL,0,NULL,NULL,1,'none',0,'English',NULL,364,'','','','','','','','',0,NULL,NULL,NULL,NULL,NULL,0,1,0,NULL,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,0,0,1,0,1,0,NULL,NULL,NULL,NULL,1,0,1,'+-',NULL),(8,'redcap_demo_f26eb3','Human Cancer Tissue Biobank',1,'2014-09-16 15:29:48','2014-09-16 15:29:48',NULL,NULL,0,0,0,0,NULL,NULL,0,NULL,0,NULL,NULL,1,'none',0,'English',NULL,364,'','','','','','','','',0,NULL,NULL,NULL,NULL,NULL,0,1,0,NULL,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,0,0,1,0,0,0,NULL,NULL,NULL,NULL,1,0,1,'+-',NULL),(9,'redcap_demo_2700c3','Multiple Surveys (classic)',1,'2014-09-16 15:29:48','2014-09-16 15:29:48',NULL,NULL,0,1,0,0,NULL,NULL,0,NULL,0,NULL,NULL,1,'none',0,'English',NULL,364,'','','','','','','','',1,NULL,NULL,NULL,NULL,NULL,0,1,0,NULL,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,0,0,1,0,0,0,'email',NULL,NULL,NULL,1,0,1,'+-',NULL),(10,'redcap_demo_432731','Multiple Surveys (longitudinal)',1,'2014-09-16 15:29:48','2014-09-16 15:29:48',NULL,NULL,0,1,1,0,NULL,NULL,0,NULL,0,NULL,NULL,1,'none',0,'English',NULL,364,'','','','','','','','',1,NULL,NULL,NULL,NULL,NULL,0,1,0,NULL,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,0,0,1,0,0,0,'email',NULL,NULL,NULL,1,0,1,'+-',NULL),(11,'redcap_demo_910823','Piping Example Project',1,'2014-09-16 15:29:48','2014-09-16 15:29:48',NULL,NULL,0,1,0,0,NULL,NULL,0,NULL,0,NULL,NULL,1,'none',0,'English',NULL,364,'','','','','','','','',1,NULL,NULL,NULL,NULL,NULL,0,1,0,NULL,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,0,0,1,0,0,0,NULL,NULL,NULL,NULL,1,0,1,'+-',NULL),(12,'redi_sample_project','RED-I Sample Project',0,'2014-09-16 15:32:31',NULL,NULL,1,0,0,1,0,0,NULL,0,'e4ed4c0c59',1,NULL,NULL,1,'none',0,'English',NULL,364,'','','','','','','','',0,NULL,NULL,NULL,NULL,NULL,0,1,0,NULL,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,0,0,1,0,0,0,NULL,NULL,NULL,NULL,1,0,1,'+-','2014-09-17 14:52:15');
/*!40000 ALTER TABLE `redcap_projects` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_projects_external`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_projects_external` (
  `project_id` varchar(32) COLLATE utf8_unicode_ci NOT NULL COMMENT 'Brief user-defined project identifier unique within custom_type',
  `custom_type` varchar(32) COLLATE utf8_unicode_ci NOT NULL COMMENT 'Brief user-defined name for the resource/category/bucket under which the project falls',
  `app_title` text COLLATE utf8_unicode_ci,
  `creation_time` datetime DEFAULT NULL,
  `project_pi_firstname` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `project_pi_mi` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `project_pi_lastname` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `project_pi_email` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `project_pi_alias` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `project_pi_pub_exclude` int(1) DEFAULT NULL,
  `project_pub_matching_institution` text COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`project_id`,`custom_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_projects_external` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_projects_external` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_projects_templates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_projects_templates` (
  `project_id` int(10) NOT NULL DEFAULT '0',
  `title` text COLLATE utf8_unicode_ci,
  `description` text COLLATE utf8_unicode_ci,
  `enabled` int(1) NOT NULL DEFAULT '0' COMMENT 'If enabled, template is visible to users in list.',
  PRIMARY KEY (`project_id`),
  CONSTRAINT `redcap_projects_templates_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `redcap_projects` (`project_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='Info about which projects are used as templates';
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_projects_templates` DISABLE KEYS */;
INSERT INTO `redcap_projects_templates` VALUES (1,'Classic Database','Contains six data entry forms, including forms for demography and baseline data, three monthly data forms, and concludes with a completion data form.',1),(2,'Longitudinal Database (2 arms)','Contains nine data entry forms (beginning with a demography form) for collecting data on two different arms (Drug A and Drug B) with each arm containing eight different events.',1),(3,'Single Survey','Contains a single data collection instrument enabled as a survey, which contains questions to demonstrate all the different field types.',1),(4,'Longitudinal Database (1 arm)','Contains nine data entry forms (beginning with a demography form) for collecting data longitudinally over eight different events.',1),(5,'Basic Demography','Contains a single data collection instrument to capture basic demographic information.',1),(6,'Project Tracking Database','Contains fifteen data entry forms dedicated to recording the attributes of and tracking and progress of projects/studies.',1),(7,'Randomized Clinical Trial','Contains seven data entry forms for collecting data for a randomized clinical trial. Incluses a short demographics form followed by a form where randomization is performed. An example randomization model has already been set up, although randomization allocation tables have not yet been created.',1),(8,'Human Cancer Tissue Biobank','Contains five data entry forms for collecting and tracking information for cancer tissue.',1),(9,'Multiple Surveys (classic)','Contains three surveys and a data entry form. Includes a pre-screening survey followed by two follow-up surveys to capture information from the participant, and then a data entry form for final data to be entered by the study personnel. The project data is captured in classic data collection format.',1),(10,'Multiple Surveys (longitudinal)','Contains three surveys and a data entry form. Includes a pre-screening survey followed by two follow-up surveys, one of which is a questionnaire takenly weekly to capture participant information longitudinally over a period of one month. The surveys are followed by a data entry form for final data to be entered by the study personnel. The project data is captured in longitudinal data collection format.',1),(11,'Piping Example Project','Contains a single data collection instrument enabled as a survey, which contains questions to demonstrate the Piping feature.',1);
/*!40000 ALTER TABLE `redcap_projects_templates` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_pub_articles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_pub_articles` (
  `article_id` int(10) NOT NULL AUTO_INCREMENT,
  `pubsrc_id` int(10) NOT NULL,
  `pub_id` varchar(16) COLLATE utf8_unicode_ci NOT NULL COMMENT 'The publication source''s ID for the article (e.g., a PMID in the case of PubMed)',
  `title` text COLLATE utf8_unicode_ci,
  `volume` varchar(16) COLLATE utf8_unicode_ci DEFAULT NULL,
  `issue` varchar(16) COLLATE utf8_unicode_ci DEFAULT NULL,
  `pages` varchar(16) COLLATE utf8_unicode_ci DEFAULT NULL,
  `journal` text COLLATE utf8_unicode_ci,
  `journal_abbrev` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `pub_date` date DEFAULT NULL,
  `epub_date` date DEFAULT NULL,
  PRIMARY KEY (`article_id`),
  UNIQUE KEY `pubsrc_id` (`pubsrc_id`,`pub_id`),
  CONSTRAINT `redcap_pub_articles_ibfk_1` FOREIGN KEY (`pubsrc_id`) REFERENCES `redcap_pub_sources` (`pubsrc_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='Articles pulled from a publication source (e.g., PubMed)';
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_pub_articles` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_pub_articles` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_pub_authors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_pub_authors` (
  `author_id` int(10) NOT NULL AUTO_INCREMENT,
  `article_id` int(10) DEFAULT NULL,
  `author` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`author_id`),
  KEY `article_id` (`article_id`),
  KEY `author` (`author`),
  CONSTRAINT `redcap_pub_authors_ibfk_1` FOREIGN KEY (`article_id`) REFERENCES `redcap_pub_articles` (`article_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_pub_authors` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_pub_authors` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_pub_matches`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_pub_matches` (
  `match_id` int(11) NOT NULL AUTO_INCREMENT,
  `article_id` int(11) NOT NULL,
  `project_id` int(11) DEFAULT NULL,
  `external_project_id` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'FK 1/2 referencing redcap_projects_external (not explicitly defined as FK to allow redcap_projects_external to be blown away)',
  `external_custom_type` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'FK 2/2 referencing redcap_projects_external (not explicitly defined as FK to allow redcap_projects_external to be blown away)',
  `search_term` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `matched` int(1) DEFAULT NULL,
  `matched_time` datetime DEFAULT NULL,
  `email_count` int(11) NOT NULL DEFAULT '0',
  `email_time` datetime DEFAULT NULL,
  `unique_hash` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`match_id`),
  UNIQUE KEY `unique_hash` (`unique_hash`),
  KEY `article_id` (`article_id`),
  KEY `project_id` (`project_id`),
  KEY `external_project_id` (`external_project_id`),
  KEY `external_custom_type` (`external_custom_type`),
  CONSTRAINT `redcap_pub_matches_ibfk_8` FOREIGN KEY (`project_id`) REFERENCES `redcap_projects` (`project_id`) ON UPDATE CASCADE,
  CONSTRAINT `redcap_pub_matches_ibfk_7` FOREIGN KEY (`article_id`) REFERENCES `redcap_pub_articles` (`article_id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_pub_matches` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_pub_matches` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_pub_mesh_terms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_pub_mesh_terms` (
  `mesh_id` int(10) NOT NULL AUTO_INCREMENT,
  `article_id` int(10) DEFAULT NULL,
  `mesh_term` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`mesh_id`),
  KEY `article_id` (`article_id`),
  KEY `mesh_term` (`mesh_term`),
  CONSTRAINT `redcap_pub_mesh_terms_ibfk_1` FOREIGN KEY (`article_id`) REFERENCES `redcap_pub_articles` (`article_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_pub_mesh_terms` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_pub_mesh_terms` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_pub_sources`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_pub_sources` (
  `pubsrc_id` int(11) NOT NULL,
  `pubsrc_name` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `pubsrc_last_crawl_time` datetime DEFAULT NULL,
  PRIMARY KEY (`pubsrc_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='The different places where we grab publications from';
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_pub_sources` DISABLE KEYS */;
INSERT INTO `redcap_pub_sources` VALUES (1,'PubMed',NULL);
/*!40000 ALTER TABLE `redcap_pub_sources` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_randomization`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_randomization` (
  `rid` int(10) NOT NULL AUTO_INCREMENT,
  `project_id` int(10) DEFAULT NULL,
  `stratified` int(1) NOT NULL DEFAULT '1' COMMENT '1=Stratified, 0=Block',
  `group_by` enum('DAG','FIELD') COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Randomize by group?',
  `target_field` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `target_event` int(10) DEFAULT NULL,
  `source_field1` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `source_event1` int(10) DEFAULT NULL,
  `source_field2` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `source_event2` int(10) DEFAULT NULL,
  `source_field3` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `source_event3` int(10) DEFAULT NULL,
  `source_field4` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `source_event4` int(10) DEFAULT NULL,
  `source_field5` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `source_event5` int(10) DEFAULT NULL,
  `source_field6` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `source_event6` int(10) DEFAULT NULL,
  `source_field7` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `source_event7` int(10) DEFAULT NULL,
  `source_field8` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `source_event8` int(10) DEFAULT NULL,
  `source_field9` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `source_event9` int(10) DEFAULT NULL,
  `source_field10` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `source_event10` int(10) DEFAULT NULL,
  `source_field11` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `source_event11` int(10) DEFAULT NULL,
  `source_field12` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `source_event12` int(10) DEFAULT NULL,
  `source_field13` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `source_event13` int(10) DEFAULT NULL,
  `source_field14` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `source_event14` int(10) DEFAULT NULL,
  `source_field15` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `source_event15` int(10) DEFAULT NULL,
  PRIMARY KEY (`rid`),
  UNIQUE KEY `project_id` (`project_id`),
  KEY `target_event` (`target_event`),
  KEY `source_event1` (`source_event1`),
  KEY `source_event2` (`source_event2`),
  KEY `source_event3` (`source_event3`),
  KEY `source_event4` (`source_event4`),
  KEY `source_event5` (`source_event5`),
  KEY `source_event6` (`source_event6`),
  KEY `source_event7` (`source_event7`),
  KEY `source_event8` (`source_event8`),
  KEY `source_event9` (`source_event9`),
  KEY `source_event10` (`source_event10`),
  KEY `source_event11` (`source_event11`),
  KEY `source_event12` (`source_event12`),
  KEY `source_event13` (`source_event13`),
  KEY `source_event14` (`source_event14`),
  KEY `source_event15` (`source_event15`),
  CONSTRAINT `redcap_randomization_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `redcap_projects` (`project_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `redcap_randomization_ibfk_10` FOREIGN KEY (`source_event9`) REFERENCES `redcap_events_metadata` (`event_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `redcap_randomization_ibfk_11` FOREIGN KEY (`source_event10`) REFERENCES `redcap_events_metadata` (`event_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `redcap_randomization_ibfk_12` FOREIGN KEY (`source_event11`) REFERENCES `redcap_events_metadata` (`event_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `redcap_randomization_ibfk_13` FOREIGN KEY (`source_event12`) REFERENCES `redcap_events_metadata` (`event_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `redcap_randomization_ibfk_14` FOREIGN KEY (`source_event13`) REFERENCES `redcap_events_metadata` (`event_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `redcap_randomization_ibfk_15` FOREIGN KEY (`source_event14`) REFERENCES `redcap_events_metadata` (`event_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `redcap_randomization_ibfk_16` FOREIGN KEY (`source_event15`) REFERENCES `redcap_events_metadata` (`event_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `redcap_randomization_ibfk_17` FOREIGN KEY (`target_event`) REFERENCES `redcap_events_metadata` (`event_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `redcap_randomization_ibfk_2` FOREIGN KEY (`source_event1`) REFERENCES `redcap_events_metadata` (`event_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `redcap_randomization_ibfk_3` FOREIGN KEY (`source_event2`) REFERENCES `redcap_events_metadata` (`event_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `redcap_randomization_ibfk_4` FOREIGN KEY (`source_event3`) REFERENCES `redcap_events_metadata` (`event_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `redcap_randomization_ibfk_5` FOREIGN KEY (`source_event4`) REFERENCES `redcap_events_metadata` (`event_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `redcap_randomization_ibfk_6` FOREIGN KEY (`source_event5`) REFERENCES `redcap_events_metadata` (`event_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `redcap_randomization_ibfk_7` FOREIGN KEY (`source_event6`) REFERENCES `redcap_events_metadata` (`event_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `redcap_randomization_ibfk_8` FOREIGN KEY (`source_event7`) REFERENCES `redcap_events_metadata` (`event_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `redcap_randomization_ibfk_9` FOREIGN KEY (`source_event8`) REFERENCES `redcap_events_metadata` (`event_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_randomization` DISABLE KEYS */;
INSERT INTO `redcap_randomization` VALUES (1,7,1,NULL,'randomization_group',NULL,'race',29,'sex',29,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `redcap_randomization` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_randomization_allocation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_randomization_allocation` (
  `aid` int(10) NOT NULL AUTO_INCREMENT,
  `rid` int(10) NOT NULL DEFAULT '0',
  `project_status` int(1) NOT NULL DEFAULT '0' COMMENT 'Used in dev or prod status',
  `is_used_by` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Used by a record?',
  `group_id` int(10) DEFAULT NULL COMMENT 'DAG',
  `target_field` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Data value',
  `source_field1` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Data value',
  `source_field2` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Data value',
  `source_field3` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Data value',
  `source_field4` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Data value',
  `source_field5` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Data value',
  `source_field6` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Data value',
  `source_field7` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Data value',
  `source_field8` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Data value',
  `source_field9` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Data value',
  `source_field10` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Data value',
  `source_field11` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Data value',
  `source_field12` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Data value',
  `source_field13` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Data value',
  `source_field14` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Data value',
  `source_field15` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Data value',
  PRIMARY KEY (`aid`),
  UNIQUE KEY `rid_status_usedby` (`rid`,`project_status`,`is_used_by`),
  KEY `group_id` (`group_id`),
  CONSTRAINT `redcap_randomization_allocation_ibfk_2` FOREIGN KEY (`group_id`) REFERENCES `redcap_data_access_groups` (`group_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `redcap_randomization_allocation_ibfk_1` FOREIGN KEY (`rid`) REFERENCES `redcap_randomization` (`rid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_randomization_allocation` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_randomization_allocation` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_sendit_docs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_sendit_docs` (
  `document_id` int(11) NOT NULL AUTO_INCREMENT,
  `doc_name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `doc_orig_name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `doc_type` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `doc_size` int(11) DEFAULT NULL,
  `send_confirmation` int(1) NOT NULL DEFAULT '0',
  `expire_date` datetime DEFAULT NULL,
  `username` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `location` int(1) NOT NULL DEFAULT '0' COMMENT '1 = Home page; 2 = File Repository; 3 = Form',
  `docs_id` int(11) NOT NULL DEFAULT '0',
  `date_added` datetime DEFAULT NULL,
  `date_deleted` datetime DEFAULT NULL COMMENT 'When really deleted from server (only applicable for location=1)',
  PRIMARY KEY (`document_id`),
  KEY `user_id` (`username`),
  KEY `docs_id_location` (`location`,`docs_id`),
  KEY `expire_location_deleted` (`expire_date`,`location`,`date_deleted`),
  KEY `date_added` (`date_added`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_sendit_docs` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_sendit_docs` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_sendit_recipients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_sendit_recipients` (
  `recipient_id` int(11) NOT NULL AUTO_INCREMENT,
  `email_address` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `sent_confirmation` int(1) NOT NULL DEFAULT '0',
  `download_date` datetime DEFAULT NULL,
  `download_count` int(11) NOT NULL DEFAULT '0',
  `document_id` int(11) NOT NULL DEFAULT '0' COMMENT 'FK from redcap_sendit_docs',
  `guid` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `pwd` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`recipient_id`),
  KEY `document_id` (`document_id`),
  KEY `email_address` (`email_address`),
  KEY `guid` (`guid`),
  CONSTRAINT `redcap_sendit_recipients_ibfk_1` FOREIGN KEY (`document_id`) REFERENCES `redcap_sendit_docs` (`document_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_sendit_recipients` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_sendit_recipients` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_sessions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_sessions` (
  `session_id` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `session_data` text COLLATE utf8_unicode_ci,
  `session_expiration` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`session_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='Stores user authentication session data';
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_sessions` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_sessions` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_standard`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_standard` (
  `standard_id` int(10) NOT NULL AUTO_INCREMENT,
  `standard_name` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  `standard_version` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  `standard_desc` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`standard_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_standard` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_standard` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_standard_code`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_standard_code` (
  `standard_code_id` int(10) NOT NULL AUTO_INCREMENT,
  `standard_code` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  `standard_code_desc` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `standard_id` int(10) NOT NULL DEFAULT '0',
  PRIMARY KEY (`standard_code_id`),
  KEY `standard_id` (`standard_id`),
  CONSTRAINT `redcap_standard_code_ibfk_1` FOREIGN KEY (`standard_id`) REFERENCES `redcap_standard` (`standard_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_standard_code` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_standard_code` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_standard_map`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_standard_map` (
  `standard_map_id` int(10) NOT NULL AUTO_INCREMENT,
  `project_id` int(10) DEFAULT NULL,
  `field_name` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `standard_code_id` int(10) NOT NULL DEFAULT '0',
  `data_conversion` mediumtext COLLATE utf8_unicode_ci,
  `data_conversion2` mediumtext COLLATE utf8_unicode_ci,
  PRIMARY KEY (`standard_map_id`),
  KEY `standard_code_id` (`standard_code_id`),
  KEY `project_id` (`project_id`),
  CONSTRAINT `redcap_standard_map_ibfk_2` FOREIGN KEY (`standard_code_id`) REFERENCES `redcap_standard_code` (`standard_code_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `redcap_standard_map_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `redcap_projects` (`project_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_standard_map` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_standard_map` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_standard_map_audit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_standard_map_audit` (
  `audit_id` int(10) NOT NULL AUTO_INCREMENT,
  `project_id` int(10) DEFAULT NULL,
  `field_name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `standard_code` int(10) DEFAULT NULL,
  `action_id` int(10) DEFAULT NULL,
  `user` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`audit_id`),
  KEY `project_id` (`project_id`),
  KEY `action_id` (`action_id`),
  KEY `standard_code` (`standard_code`),
  CONSTRAINT `redcap_standard_map_audit_ibfk_5` FOREIGN KEY (`standard_code`) REFERENCES `redcap_standard_code` (`standard_code_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `redcap_standard_map_audit_ibfk_2` FOREIGN KEY (`action_id`) REFERENCES `redcap_standard_map_audit_action` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `redcap_standard_map_audit_ibfk_4` FOREIGN KEY (`project_id`) REFERENCES `redcap_projects` (`project_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_standard_map_audit` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_standard_map_audit` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_standard_map_audit_action`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_standard_map_audit_action` (
  `id` int(10) NOT NULL DEFAULT '0',
  `action` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_standard_map_audit_action` DISABLE KEYS */;
INSERT INTO `redcap_standard_map_audit_action` VALUES (1,'add mapped field'),(2,'modify mapped field'),(3,'remove mapped field');
/*!40000 ALTER TABLE `redcap_standard_map_audit_action` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_surveys`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_surveys` (
  `survey_id` int(10) NOT NULL AUTO_INCREMENT,
  `project_id` int(10) DEFAULT NULL,
  `form_name` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'NULL = assume first form',
  `title` text COLLATE utf8_unicode_ci COMMENT 'Survey title',
  `instructions` text COLLATE utf8_unicode_ci COMMENT 'Survey instructions',
  `acknowledgement` text COLLATE utf8_unicode_ci COMMENT 'Survey acknowledgement',
  `question_by_section` int(1) NOT NULL DEFAULT '0' COMMENT '0 = one-page survey',
  `question_auto_numbering` int(1) NOT NULL DEFAULT '1',
  `survey_enabled` int(1) NOT NULL DEFAULT '1',
  `save_and_return` int(1) NOT NULL DEFAULT '0',
  `logo` int(10) DEFAULT NULL COMMENT 'FK for redcap_edocs_metadata',
  `hide_title` int(1) NOT NULL DEFAULT '0',
  `view_results` int(1) NOT NULL DEFAULT '0',
  `min_responses_view_results` int(5) NOT NULL DEFAULT '10',
  `check_diversity_view_results` int(1) NOT NULL DEFAULT '0',
  `end_survey_redirect_url` text COLLATE utf8_unicode_ci COMMENT 'URL to redirect to after completing survey',
  `end_survey_redirect_url_append_id` int(1) NOT NULL DEFAULT '0' COMMENT 'Append participant_id to URL',
  `survey_expiration` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Timestamp when survey expires',
  PRIMARY KEY (`survey_id`),
  UNIQUE KEY `logo` (`logo`),
  UNIQUE KEY `project_form` (`project_id`,`form_name`),
  KEY `survey_expiration_enabled` (`survey_expiration`,`survey_enabled`),
  CONSTRAINT `redcap_surveys_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `redcap_projects` (`project_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `redcap_surveys_ibfk_2` FOREIGN KEY (`logo`) REFERENCES `redcap_edocs_metadata` (`doc_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='Table for survey data';
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_surveys` DISABLE KEYS */;
INSERT INTO `redcap_surveys` VALUES (1,3,'survey','Example Survey','&lt;p style=&quot;margin-top: 10px; margin-right: 0px; margin-bottom: 10px; margin-left: 0px; font-family: Arial, Verdana, Helvetica, sans-serif; font-size: 12px; text-align: left; line-height: 1.5em; max-width: 700px; clear: both; padding: 0px;&quot;&gt;These are your survey instructions that you would enter for your survey participants. You may put whatever text you like here, which may include information about the purpose of the survey, who is taking the survey, or how to take the survey.&lt;/p&gt;<br>&lt;p style=&quot;margin-top: 10px; margin-right: 0px; margin-bottom: 10px; margin-left: 0px; font-family: Arial, Verdana, Helvetica, sans-serif; font-size: 12px; text-align: left; line-height: 1.5em; max-width: 700px; clear: both; padding: 0px;&quot;&gt;Surveys can use a single survey link for all respondents, which can be posted on a webpage or emailed out from your email application of choice.&amp;nbsp;&lt;strong&gt;By default, all survey responses are collected anonymously&lt;/strong&gt;&amp;nbsp;(that is, unless your survey asks for name, email, or other identifying information).&amp;nbsp;If you wish to track individuals who have taken your survey, you may upload a list of email addresses into a Participant List within REDCap, in which you can have REDCap send them an email invitation, which will track if they have taken the survey and when it was taken. This method still collects responses anonymously, but if you wish to identify an individual respondent\'s answers, you may do so by also providing an Identifier in your Participant List. Of course, in that case you may want to inform your respondents in your survey\'s instructions that their responses are not being collected anonymously and can thus be traced back to them.&lt;/p&gt;','&lt;p&gt;&lt;strong&gt;Thank you for taking the survey.&lt;/strong&gt;&lt;/p&gt;<br>&lt;p&gt;Have a nice day!&lt;/p&gt;',0,0,1,1,NULL,0,0,10,0,NULL,0,NULL),(2,9,'participant_info_survey','Follow-Up Survey','&lt;p&gt;&lt;strong&gt;Please complete the survey below.&lt;/strong&gt;&lt;/p&gt;\r\n&lt;p&gt;Thank you!&lt;/p&gt;','&lt;p&gt;&lt;strong&gt;Thank you for taking the survey.&lt;/strong&gt;&lt;/p&gt;\r\n&lt;p&gt;Have a nice day!&lt;/p&gt;',0,1,1,1,NULL,0,0,10,0,NULL,0,NULL),(3,9,'participant_morale_questionnaire','Patient Morale Questionnaire','&lt;p&gt;&lt;strong&gt;Please complete the survey below.&lt;/strong&gt;&lt;/p&gt;\r\n&lt;p&gt;Thank you!&lt;/p&gt;','&lt;p&gt;&lt;strong&gt;Thank you for taking the survey.&lt;/strong&gt;&lt;/p&gt;\r\n&lt;p&gt;Have a nice day!&lt;/p&gt;',0,1,1,1,NULL,0,0,10,0,NULL,0,NULL),(4,9,'prescreening_survey','Pre-Screening Survey','&lt;p&gt;&lt;strong&gt;Please complete the survey below.&lt;/strong&gt;&lt;/p&gt;\r\n&lt;p&gt;Thank you!&lt;/p&gt;','&lt;p&gt;&lt;strong&gt;Thank you for taking the survey.&lt;/strong&gt;&lt;/p&gt;\r\n&lt;p&gt;Have a nice day!&lt;/p&gt;',0,1,1,0,NULL,0,0,10,0,NULL,0,NULL),(5,10,'participant_info_survey','Follow-Up Survey','&lt;p&gt;&lt;strong&gt;Please complete the survey below.&lt;/strong&gt;&lt;/p&gt;\r\n&lt;p&gt;Thank you!&lt;/p&gt;','&lt;p&gt;&lt;strong&gt;Thank you for taking the survey.&lt;/strong&gt;&lt;/p&gt;\r\n&lt;p&gt;Have a nice day!&lt;/p&gt;',0,1,1,1,NULL,0,0,10,0,NULL,0,NULL),(6,10,'participant_morale_questionnaire','Patient Morale Questionnaire','&lt;p&gt;&lt;strong&gt;Please complete the survey below.&lt;/strong&gt;&lt;/p&gt;\r\n&lt;p&gt;Thank you!&lt;/p&gt;','&lt;p&gt;&lt;strong&gt;Thank you for taking the survey.&lt;/strong&gt;&lt;/p&gt;\r\n&lt;p&gt;Have a nice day!&lt;/p&gt;',0,1,1,1,NULL,0,0,10,0,NULL,0,NULL),(7,10,'prescreening_survey','Pre-Screening Survey','&lt;p&gt;&lt;strong&gt;Please complete the survey below.&lt;/strong&gt;&lt;/p&gt;\r\n&lt;p&gt;Thank you!&lt;/p&gt;','&lt;p&gt;&lt;strong&gt;Thank you for taking the survey.&lt;/strong&gt;&lt;/p&gt;\r\n&lt;p&gt;Have a nice day!&lt;/p&gt;',0,1,1,0,NULL,0,0,10,0,NULL,0,NULL),(8,11,'survey','Example Survey to Demonstrate Piping','This survey will demonstrate some basic examples of the Piping feature in REDCap.','&lt;p style=\"font-size:14px;\"&gt;&lt;strong&gt;[first_name], thank you for taking the survey.&lt;/strong&gt;&lt;/p&gt;<br>&lt;p&gt;Have a nice day!&lt;/p&gt;',1,0,1,0,NULL,0,0,10,0,NULL,0,NULL);
/*!40000 ALTER TABLE `redcap_surveys` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_surveys_emails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_surveys_emails` (
  `email_id` int(10) NOT NULL AUTO_INCREMENT,
  `survey_id` int(10) DEFAULT NULL,
  `email_subject` text COLLATE utf8_unicode_ci,
  `email_content` text COLLATE utf8_unicode_ci,
  `email_sender` int(10) DEFAULT NULL COMMENT 'FK ui_id from redcap_user_information',
  `email_account` enum('1','2','3') COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Sender''s account (1=Primary, 2=Secondary, 3=Tertiary)',
  `email_static` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Sender''s static email address (only for scheduled invitations)',
  `email_sent` datetime DEFAULT NULL COMMENT 'Null=Not sent yet (scheduled)',
  PRIMARY KEY (`email_id`),
  KEY `email_sender` (`email_sender`),
  KEY `email_sent` (`email_sent`),
  KEY `survey_id_email_sent` (`survey_id`,`email_sent`),
  CONSTRAINT `redcap_surveys_emails_ibfk_1` FOREIGN KEY (`survey_id`) REFERENCES `redcap_surveys` (`survey_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `redcap_surveys_emails_ibfk_2` FOREIGN KEY (`email_sender`) REFERENCES `redcap_user_information` (`ui_id`) ON DELETE SET NULL ON UPDATE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='Track emails sent out';
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_surveys_emails` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_surveys_emails` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_surveys_emails_recipients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_surveys_emails_recipients` (
  `email_recip_id` int(10) NOT NULL AUTO_INCREMENT,
  `email_id` int(10) DEFAULT NULL COMMENT 'FK redcap_surveys_emails',
  `participant_id` int(10) DEFAULT NULL COMMENT 'FK redcap_surveys_participants',
  `static_email` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Static email address of recipient (used when participant has no email)',
  PRIMARY KEY (`email_recip_id`),
  KEY `emt_id` (`email_id`),
  KEY `participant_id` (`participant_id`),
  CONSTRAINT `redcap_surveys_emails_recipients_ibfk_1` FOREIGN KEY (`email_id`) REFERENCES `redcap_surveys_emails` (`email_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `redcap_surveys_emails_recipients_ibfk_2` FOREIGN KEY (`participant_id`) REFERENCES `redcap_surveys_participants` (`participant_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='Track email recipients';
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_surveys_emails_recipients` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_surveys_emails_recipients` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_surveys_emails_send_rate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_surveys_emails_send_rate` (
  `esr_id` int(10) NOT NULL AUTO_INCREMENT,
  `sent_begin_time` datetime DEFAULT NULL COMMENT 'Time email batch was sent',
  `emails_per_batch` int(10) DEFAULT NULL COMMENT 'Number of emails sent in this batch',
  `emails_per_minute` int(6) DEFAULT NULL COMMENT 'Number of emails sent per minute for this batch',
  PRIMARY KEY (`esr_id`),
  KEY `sent_begin_time` (`sent_begin_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='Capture the rate that emails are sent per minute by REDCap';
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_surveys_emails_send_rate` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_surveys_emails_send_rate` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_surveys_participants`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_surveys_participants` (
  `participant_id` int(10) NOT NULL AUTO_INCREMENT,
  `survey_id` int(10) DEFAULT NULL,
  `event_id` int(10) DEFAULT NULL,
  `hash` varchar(10) CHARACTER SET latin1 COLLATE latin1_general_cs DEFAULT NULL,
  `legacy_hash` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Migrated from RS',
  `participant_email` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'NULL if public survey',
  `participant_identifier` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`participant_id`),
  UNIQUE KEY `hash` (`hash`),
  UNIQUE KEY `legacy_hash` (`legacy_hash`),
  KEY `participant_email` (`participant_email`),
  KEY `survey_event_email` (`survey_id`,`event_id`,`participant_email`),
  KEY `event_id` (`event_id`),
  CONSTRAINT `redcap_surveys_participants_ibfk_2` FOREIGN KEY (`event_id`) REFERENCES `redcap_events_metadata` (`event_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `redcap_surveys_participants_ibfk_1` FOREIGN KEY (`survey_id`) REFERENCES `redcap_surveys` (`survey_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='Table for survey data';
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_surveys_participants` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_surveys_participants` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_surveys_response`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_surveys_response` (
  `response_id` int(11) NOT NULL AUTO_INCREMENT,
  `participant_id` int(10) DEFAULT NULL,
  `record` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `first_submit_time` datetime DEFAULT NULL,
  `completion_time` datetime DEFAULT NULL,
  `return_code` varchar(8) COLLATE utf8_unicode_ci DEFAULT NULL,
  `results_code` varchar(8) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`response_id`),
  UNIQUE KEY `participant_record` (`participant_id`,`record`),
  KEY `return_code` (`return_code`),
  KEY `results_code` (`results_code`),
  KEY `first_submit_time` (`first_submit_time`),
  KEY `completion_time` (`completion_time`),
  CONSTRAINT `redcap_surveys_response_ibfk_1` FOREIGN KEY (`participant_id`) REFERENCES `redcap_surveys_participants` (`participant_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_surveys_response` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_surveys_response` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_surveys_response_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_surveys_response_users` (
  `response_id` int(10) DEFAULT NULL,
  `username` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  UNIQUE KEY `response_user` (`response_id`,`username`),
  KEY `username` (`username`),
  CONSTRAINT `redcap_surveys_response_users_ibfk_1` FOREIGN KEY (`response_id`) REFERENCES `redcap_surveys_response` (`response_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_surveys_response_users` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_surveys_response_users` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_surveys_response_values`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_surveys_response_values` (
  `response_id` int(10) DEFAULT NULL,
  `project_id` int(10) NOT NULL DEFAULT '0',
  `event_id` int(10) DEFAULT NULL,
  `record` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `field_name` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `value` text COLLATE utf8_unicode_ci,
  KEY `event_id` (`event_id`),
  KEY `project_field` (`project_id`,`field_name`),
  KEY `proj_record_field` (`project_id`,`record`,`field_name`),
  KEY `response_id` (`response_id`),
  CONSTRAINT `redcap_surveys_response_values_ibfk_1` FOREIGN KEY (`response_id`) REFERENCES `redcap_surveys_response` (`response_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `redcap_surveys_response_values_ibfk_2` FOREIGN KEY (`project_id`) REFERENCES `redcap_projects` (`project_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `redcap_surveys_response_values_ibfk_3` FOREIGN KEY (`event_id`) REFERENCES `redcap_events_metadata` (`event_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='Storage for completed survey responses (archival purposes)';
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_surveys_response_values` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_surveys_response_values` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_surveys_scheduler`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_surveys_scheduler` (
  `ss_id` int(10) NOT NULL AUTO_INCREMENT,
  `survey_id` int(10) DEFAULT NULL,
  `event_id` int(10) DEFAULT NULL,
  `active` int(1) NOT NULL DEFAULT '1' COMMENT 'Is it currently active?',
  `email_subject` text COLLATE utf8_unicode_ci COMMENT 'Survey invitation subject',
  `email_content` text COLLATE utf8_unicode_ci COMMENT 'Survey invitation text',
  `email_sender` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Static email address of sender',
  `condition_surveycomplete_survey_id` int(10) DEFAULT NULL COMMENT 'survey_id of trigger',
  `condition_surveycomplete_event_id` int(10) DEFAULT NULL COMMENT 'event_id of trigger',
  `condition_andor` enum('AND','OR') COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Include survey complete AND/OR logic',
  `condition_logic` text COLLATE utf8_unicode_ci COMMENT 'Logic using field values',
  `condition_send_time_option` enum('IMMEDIATELY','TIME_LAG','NEXT_OCCURRENCE','EXACT_TIME') COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'When to send invites after condition is met',
  `condition_send_time_lag_days` int(3) DEFAULT NULL COMMENT 'Wait X days to send invites after condition is met',
  `condition_send_time_lag_hours` int(2) DEFAULT NULL COMMENT 'Wait X hours to send invites after condition is met',
  `condition_send_time_lag_minutes` int(2) DEFAULT NULL COMMENT 'Wait X seconds to send invites after condition is met',
  `condition_send_next_day_type` enum('DAY','WEEKDAY','WEEKENDDAY','SUNDAY','MONDAY','TUESDAY','WEDNESDAY','THURSDAY','FRIDAY','SATURDAY') COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Wait till specific day/time to send invites after condition is met',
  `condition_send_next_time` time DEFAULT NULL COMMENT 'Wait till specific day/time to send invites after condition is met',
  `condition_send_time_exact` datetime DEFAULT NULL COMMENT 'Wait till exact date/time to send invites after condition is met',
  PRIMARY KEY (`ss_id`),
  UNIQUE KEY `survey_event` (`survey_id`,`event_id`),
  KEY `event_id` (`event_id`),
  KEY `condition_surveycomplete_event_id` (`condition_surveycomplete_event_id`),
  KEY `condition_surveycomplete_survey_event` (`condition_surveycomplete_survey_id`,`condition_surveycomplete_event_id`),
  CONSTRAINT `redcap_surveys_scheduler_ibfk_1` FOREIGN KEY (`survey_id`) REFERENCES `redcap_surveys` (`survey_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `redcap_surveys_scheduler_ibfk_2` FOREIGN KEY (`event_id`) REFERENCES `redcap_events_metadata` (`event_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `redcap_surveys_scheduler_ibfk_3` FOREIGN KEY (`condition_surveycomplete_survey_id`) REFERENCES `redcap_surveys` (`survey_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `redcap_surveys_scheduler_ibfk_4` FOREIGN KEY (`condition_surveycomplete_event_id`) REFERENCES `redcap_events_metadata` (`event_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_surveys_scheduler` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_surveys_scheduler` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_surveys_scheduler_queue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_surveys_scheduler_queue` (
  `ssq_id` int(10) NOT NULL AUTO_INCREMENT,
  `ss_id` int(10) DEFAULT NULL COMMENT 'FK for surveys_scheduler table',
  `email_recip_id` int(10) DEFAULT NULL COMMENT 'FK for redcap_surveys_emails_recipients table',
  `record` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'NULL if record not created yet',
  `scheduled_time_to_send` datetime DEFAULT NULL COMMENT 'Time invitation will be sent',
  `status` enum('QUEUED','SENDING','SENT','DID NOT SEND') COLLATE utf8_unicode_ci NOT NULL DEFAULT 'QUEUED' COMMENT 'Survey invitation status (default=QUEUED)',
  `time_sent` datetime DEFAULT NULL COMMENT 'Actual time invitation was sent',
  `reason_not_sent` enum('EMAIL ADDRESS NOT FOUND','EMAIL ATTEMPT FAILED','UNKNOWN','SURVEY ALREADY COMPLETED') COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Explanation of why invitation did not send, if applicable',
  PRIMARY KEY (`ssq_id`),
  UNIQUE KEY `ss_id_record` (`ss_id`,`record`),
  UNIQUE KEY `email_recip_id_record` (`email_recip_id`,`record`),
  KEY `time_sent` (`time_sent`),
  KEY `status` (`status`),
  KEY `send_sent_status` (`scheduled_time_to_send`,`time_sent`,`status`),
  CONSTRAINT `redcap_surveys_scheduler_queue_ibfk_2` FOREIGN KEY (`email_recip_id`) REFERENCES `redcap_surveys_emails_recipients` (`email_recip_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `redcap_surveys_scheduler_queue_ibfk_1` FOREIGN KEY (`ss_id`) REFERENCES `redcap_surveys_scheduler` (`ss_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_surveys_scheduler_queue` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_surveys_scheduler_queue` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_user_information`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_user_information` (
  `ui_id` int(10) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `user_email` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Primary email',
  `user_email2` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Secondary email',
  `user_email3` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Tertiary email',
  `user_firstname` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `user_lastname` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `user_inst_id` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `super_user` int(1) NOT NULL DEFAULT '0',
  `user_creation` datetime DEFAULT NULL COMMENT 'Time user account was created',
  `user_firstvisit` datetime DEFAULT NULL,
  `user_firstactivity` datetime DEFAULT NULL,
  `user_lastactivity` datetime DEFAULT NULL,
  `user_lastlogin` datetime DEFAULT NULL,
  `user_suspended_time` datetime DEFAULT NULL,
  `user_expiration` datetime DEFAULT NULL COMMENT 'Time at which the user will be automatically suspended from REDCap',
  `user_access_dashboard_view` datetime DEFAULT NULL,
  `user_access_dashboard_email_queued` enum('QUEUED','SENDING') COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Tracks status of email reminder for User Access Dashboard',
  `user_sponsor` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Username of user''s sponsor or contact person',
  `user_comments` text COLLATE utf8_unicode_ci COMMENT 'Miscellaneous comments about user',
  `allow_create_db` int(1) NOT NULL DEFAULT '1',
  `email_verify_code` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Primary email verification code',
  `email2_verify_code` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Secondary email verification code',
  `email3_verify_code` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Tertiary email verification code',
  PRIMARY KEY (`ui_id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email_verify_code` (`email_verify_code`),
  UNIQUE KEY `email2_verify_code` (`email2_verify_code`),
  UNIQUE KEY `email3_verify_code` (`email3_verify_code`),
  KEY `user_firstname` (`user_firstname`),
  KEY `user_lastname` (`user_lastname`),
  KEY `user_access_dashboard_view` (`user_access_dashboard_view`),
  KEY `user_creation` (`user_creation`),
  KEY `user_firstvisit` (`user_firstvisit`),
  KEY `user_firstactivity` (`user_firstactivity`),
  KEY `user_lastactivity` (`user_lastactivity`),
  KEY `user_lastlogin` (`user_lastlogin`),
  KEY `user_suspended_time` (`user_suspended_time`),
  KEY `user_expiration` (`user_expiration`),
  KEY `user_access_dashboard_email_queued` (`user_access_dashboard_email_queued`),
  KEY `user_email` (`user_email`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_user_information` DISABLE KEYS */;
INSERT INTO `redcap_user_information` VALUES (1,'site_admin','joe.user@project-redcap.org',NULL,NULL,'Joe','User',NULL,1,NULL,'2014-09-16 15:29:47','2014-09-16 15:32:31','2014-09-17 14:52:15','2014-09-16 15:31:53',NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,NULL);
/*!40000 ALTER TABLE `redcap_user_information` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_user_rights`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_user_rights` (
  `project_id` int(10) NOT NULL DEFAULT '0',
  `username` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `expiration` date DEFAULT NULL,
  `role_id` int(10) DEFAULT NULL,
  `group_id` int(10) DEFAULT NULL,
  `lock_record` int(1) NOT NULL DEFAULT '0',
  `lock_record_multiform` int(1) NOT NULL DEFAULT '0',
  `lock_record_customize` int(1) NOT NULL DEFAULT '0',
  `data_export_tool` int(1) NOT NULL DEFAULT '1',
  `data_import_tool` int(1) NOT NULL DEFAULT '1',
  `data_comparison_tool` int(1) NOT NULL DEFAULT '1',
  `data_logging` int(1) NOT NULL DEFAULT '1',
  `file_repository` int(1) NOT NULL DEFAULT '1',
  `double_data` int(1) NOT NULL DEFAULT '0',
  `user_rights` int(1) NOT NULL DEFAULT '1',
  `data_access_groups` int(1) NOT NULL DEFAULT '1',
  `graphical` int(1) NOT NULL DEFAULT '1',
  `reports` int(1) NOT NULL DEFAULT '1',
  `design` int(1) NOT NULL DEFAULT '0',
  `calendar` int(1) NOT NULL DEFAULT '1',
  `data_entry` text COLLATE utf8_unicode_ci,
  `api_token` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `api_export` int(1) NOT NULL DEFAULT '0',
  `api_import` int(1) NOT NULL DEFAULT '0',
  `record_create` int(1) NOT NULL DEFAULT '1',
  `record_rename` int(1) NOT NULL DEFAULT '0',
  `record_delete` int(1) NOT NULL DEFAULT '0',
  `dts` int(1) NOT NULL DEFAULT '0' COMMENT 'DTS adjudication page',
  `participants` int(1) NOT NULL DEFAULT '1',
  `data_quality_design` int(1) NOT NULL DEFAULT '0',
  `data_quality_execute` int(1) NOT NULL DEFAULT '0',
  `data_quality_resolution` int(1) NOT NULL DEFAULT '0' COMMENT '0=No access, 1=View only, 2=Respond, 3=Open, close, respond',
  `random_setup` int(1) NOT NULL DEFAULT '0',
  `random_dashboard` int(1) NOT NULL DEFAULT '0',
  `random_perform` int(1) NOT NULL DEFAULT '0',
  `realtime_webservice_mapping` int(1) NOT NULL DEFAULT '0' COMMENT 'User can map fields for RTWS',
  `realtime_webservice_adjudicate` int(1) NOT NULL DEFAULT '0' COMMENT 'User can adjudicate data for RTWS',
  PRIMARY KEY (`project_id`,`username`),
  UNIQUE KEY `api_token` (`api_token`),
  KEY `username` (`username`),
  KEY `project_id` (`project_id`),
  KEY `group_id` (`group_id`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `redcap_user_rights_ibfk_2` FOREIGN KEY (`project_id`) REFERENCES `redcap_projects` (`project_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `redcap_user_rights_ibfk_3` FOREIGN KEY (`group_id`) REFERENCES `redcap_data_access_groups` (`group_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `redcap_user_rights_ibfk_4` FOREIGN KEY (`role_id`) REFERENCES `redcap_user_roles` (`role_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_user_rights` DISABLE KEYS */;
INSERT INTO `redcap_user_rights` VALUES (1,'site_admin',NULL,NULL,NULL,0,0,0,1,1,1,1,1,0,0,0,1,1,0,1,'',NULL,0,0,1,0,0,0,1,0,1,0,0,0,0,0,0),(2,'site_admin',NULL,NULL,NULL,0,0,0,1,1,1,1,1,0,0,0,1,1,0,1,'',NULL,0,0,1,0,0,0,1,0,1,0,0,0,0,0,0),(3,'site_admin',NULL,NULL,NULL,0,0,0,1,0,1,1,1,0,0,0,1,1,0,1,'',NULL,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0),(4,'site_admin',NULL,NULL,NULL,0,0,0,1,1,1,1,1,0,0,0,1,1,0,1,'',NULL,0,0,1,0,0,0,1,0,1,0,0,0,0,0,0),(5,'site_admin',NULL,NULL,NULL,0,0,0,1,1,1,1,1,0,0,0,1,1,0,1,'',NULL,0,0,1,0,0,0,1,0,1,0,0,0,0,0,0),(6,'site_admin',NULL,NULL,NULL,0,0,0,1,1,1,1,1,0,0,0,1,1,0,1,'',NULL,0,0,1,0,0,0,1,0,1,0,0,0,0,0,0),(7,'site_admin',NULL,NULL,NULL,0,0,0,1,1,1,1,1,0,0,0,1,1,0,1,'',NULL,0,0,1,0,0,0,1,0,1,0,1,1,1,0,0),(8,'site_admin',NULL,NULL,NULL,0,0,0,1,1,1,1,1,0,0,0,1,1,0,1,'',NULL,0,0,1,0,0,0,1,0,1,0,0,0,0,0,0),(9,'site_admin',NULL,NULL,NULL,0,0,0,1,0,1,1,1,0,0,0,1,1,0,1,'',NULL,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0),(10,'site_admin',NULL,NULL,NULL,0,0,0,1,0,1,1,1,0,0,0,1,1,0,1,'',NULL,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0),(11,'site_admin',NULL,NULL,NULL,0,0,0,1,0,1,1,1,0,0,0,1,1,0,1,'',NULL,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0),(12,'site_admin',NULL,NULL,NULL,0,0,0,1,1,1,1,1,0,1,1,1,1,1,1,'[enrollment,1][cbc,1][chemistry,1]','THIS_IS_THE_API_KEY',1,1,1,0,0,0,1,1,1,0,0,0,0,0,0);
/*!40000 ALTER TABLE `redcap_user_rights` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_user_roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_user_roles` (
  `role_id` int(10) NOT NULL AUTO_INCREMENT,
  `project_id` int(10) DEFAULT NULL,
  `role_name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Name of user role',
  `lock_record` int(1) NOT NULL DEFAULT '0',
  `lock_record_multiform` int(1) NOT NULL DEFAULT '0',
  `lock_record_customize` int(1) NOT NULL DEFAULT '0',
  `data_export_tool` int(1) NOT NULL DEFAULT '1',
  `data_import_tool` int(1) NOT NULL DEFAULT '1',
  `data_comparison_tool` int(1) NOT NULL DEFAULT '1',
  `data_logging` int(1) NOT NULL DEFAULT '1',
  `file_repository` int(1) NOT NULL DEFAULT '1',
  `double_data` int(1) NOT NULL DEFAULT '0',
  `user_rights` int(1) NOT NULL DEFAULT '1',
  `data_access_groups` int(1) NOT NULL DEFAULT '1',
  `graphical` int(1) NOT NULL DEFAULT '1',
  `reports` int(1) NOT NULL DEFAULT '1',
  `design` int(1) NOT NULL DEFAULT '0',
  `calendar` int(1) NOT NULL DEFAULT '1',
  `data_entry` text COLLATE utf8_unicode_ci,
  `api_export` int(1) NOT NULL DEFAULT '0',
  `api_import` int(1) NOT NULL DEFAULT '0',
  `record_create` int(1) NOT NULL DEFAULT '1',
  `record_rename` int(1) NOT NULL DEFAULT '0',
  `record_delete` int(1) NOT NULL DEFAULT '0',
  `dts` int(1) NOT NULL DEFAULT '0' COMMENT 'DTS adjudication page',
  `participants` int(1) NOT NULL DEFAULT '1',
  `data_quality_design` int(1) NOT NULL DEFAULT '0',
  `data_quality_execute` int(1) NOT NULL DEFAULT '0',
  `data_quality_resolution` int(1) NOT NULL DEFAULT '0' COMMENT '0=No access, 1=View only, 2=Respond, 3=Open, close, respond',
  `random_setup` int(1) NOT NULL DEFAULT '0',
  `random_dashboard` int(1) NOT NULL DEFAULT '0',
  `random_perform` int(1) NOT NULL DEFAULT '0',
  `realtime_webservice_mapping` int(1) NOT NULL DEFAULT '0' COMMENT 'User can map fields for RTWS',
  `realtime_webservice_adjudicate` int(1) NOT NULL DEFAULT '0' COMMENT 'User can adjudicate data for RTWS',
  PRIMARY KEY (`role_id`),
  KEY `project_id` (`project_id`),
  CONSTRAINT `redcap_user_roles_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `redcap_projects` (`project_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_user_roles` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_user_roles` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_user_whitelist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_user_whitelist` (
  `username` varchar(255) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_user_whitelist` DISABLE KEYS */;
/*!40000 ALTER TABLE `redcap_user_whitelist` ENABLE KEYS */;
DROP TABLE IF EXISTS `redcap_validation_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_validation_types` (
  `validation_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL COMMENT 'Unique name for Data Dictionary',
  `validation_label` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Label in Online Designer',
  `regex_js` text COLLATE utf8_unicode_ci,
  `regex_php` text COLLATE utf8_unicode_ci,
  `data_type` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `legacy_value` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `visible` int(1) NOT NULL DEFAULT '1' COMMENT 'Show in Online Designer?',
  UNIQUE KEY `validation_name` (`validation_name`),
  KEY `data_type` (`data_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `redcap_validation_types` DISABLE KEYS */;
INSERT INTO `redcap_validation_types` VALUES ('alpha_only','Letters only','/^[a-z]+$/i','/^[a-z]+$/i','text',NULL,0),('date_dmy','Date (D-M-Y)','/^((29([-\\/.]?)02\\3(\\d{2}([13579][26]|[2468][048]|04|08)|(1600|2[048]00)))|((((0[1-9]|1\\d|2[0-8])([-\\/.]?)(0[1-9]|1[012]))|((29|30)([-\\/.]?)(0[13-9]|1[012]))|(31([-\\/.]?)(0[13578]|1[02])))(\\11|\\15|\\18)\\d{4}))$/','/^((29([-\\/.]?)02\\3(\\d{2}([13579][26]|[2468][048]|04|08)|(1600|2[048]00)))|((((0[1-9]|1\\d|2[0-8])([-\\/.]?)(0[1-9]|1[012]))|((29|30)([-\\/.]?)(0[13-9]|1[012]))|(31([-\\/.]?)(0[13578]|1[02])))(\\11|\\15|\\18)\\d{4}))$/','date',NULL,1),('date_mdy','Date (M-D-Y)','/^((02([-\\/.]?)29\\3(\\d{2}([13579][26]|[2468][048]|04|08)|(1600|2[048]00)))|((((0[1-9]|1[012])([-\\/.]?)(0[1-9]|1\\d|2[0-8]))|((0[13-9]|1[012])([-\\/.]?)(29|30))|((0[13578]|1[02])([-\\/.]?)31))(\\11|\\15|\\19)\\d{4}))$/','/^((02([-\\/.]?)29\\3(\\d{2}([13579][26]|[2468][048]|04|08)|(1600|2[048]00)))|((((0[1-9]|1[012])([-\\/.]?)(0[1-9]|1\\d|2[0-8]))|((0[13-9]|1[012])([-\\/.]?)(29|30))|((0[13578]|1[02])([-\\/.]?)31))(\\11|\\15|\\19)\\d{4}))$/','date',NULL,1),('date_ymd','Date (Y-M-D)','/^(((\\d{2}([13579][26]|[2468][048]|04|08)|(1600|2[048]00))([-\\/.]?)02(\\6)29)|(\\d{4}([-\\/.]?)((0[1-9]|1[012])(\\9)(0[1-9]|1\\d|2[0-8])|((0[13-9]|1[012])(\\9)(29|30))|((0[13578]|1[02])(\\9)31))))$/','/^(((\\d{2}([13579][26]|[2468][048]|04|08)|(1600|2[048]00))([-\\/.]?)02(\\6)29)|(\\d{4}([-\\/.]?)((0[1-9]|1[012])(\\9)(0[1-9]|1\\d|2[0-8])|((0[13-9]|1[012])(\\9)(29|30))|((0[13578]|1[02])(\\9)31))))$/','date','date',1),('datetime_dmy','Datetime (D-M-Y H:M)','/^((29([-\\/.]?)02\\3(\\d{2}([13579][26]|[2468][048]|04|08)|(1600|2[048]00)))|((((0[1-9]|1\\d|2[0-8])([-\\/.]?)(0[1-9]|1[012]))|((29|30)([-\\/.]?)(0[13-9]|1[012]))|(31([-\\/.]?)(0[13578]|1[02])))(\\11|\\15|\\18)\\d{4})) (\\d|[0-1]\\d|[2][0-3]):[0-5]\\d$/','/^((29([-\\/.]?)02\\3(\\d{2}([13579][26]|[2468][048]|04|08)|(1600|2[048]00)))|((((0[1-9]|1\\d|2[0-8])([-\\/.]?)(0[1-9]|1[012]))|((29|30)([-\\/.]?)(0[13-9]|1[012]))|(31([-\\/.]?)(0[13578]|1[02])))(\\11|\\15|\\18)\\d{4})) (\\d|[0-1]\\d|[2][0-3]):[0-5]\\d$/','datetime',NULL,1),('datetime_mdy','Datetime (M-D-Y H:M)','/^((02([-\\/.]?)29\\3(\\d{2}([13579][26]|[2468][048]|04|08)|(1600|2[048]00)))|((((0[1-9]|1[012])([-\\/.]?)(0[1-9]|1\\d|2[0-8]))|((0[13-9]|1[012])([-\\/.]?)(29|30))|((0[13578]|1[02])([-\\/.]?)31))(\\11|\\15|\\19)\\d{4})) (\\d|[0-1]\\d|[2][0-3]):[0-5]\\d$/','/^((02([-\\/.]?)29\\3(\\d{2}([13579][26]|[2468][048]|04|08)|(1600|2[048]00)))|((((0[1-9]|1[012])([-\\/.]?)(0[1-9]|1\\d|2[0-8]))|((0[13-9]|1[012])([-\\/.]?)(29|30))|((0[13578]|1[02])([-\\/.]?)31))(\\11|\\15|\\19)\\d{4})) (\\d|[0-1]\\d|[2][0-3]):[0-5]\\d$/','datetime',NULL,1),('datetime_seconds_dmy','Datetime w/ seconds (D-M-Y H:M:S)','/^((29([-\\/.]?)02\\3(\\d{2}([13579][26]|[2468][048]|04|08)|(1600|2[048]00)))|((((0[1-9]|1\\d|2[0-8])([-\\/.]?)(0[1-9]|1[012]))|((29|30)([-\\/.]?)(0[13-9]|1[012]))|(31([-\\/.]?)(0[13578]|1[02])))(\\11|\\15|\\18)\\d{4})) (\\d|[0-1]\\d|[2][0-3])(:[0-5]\\d){2}$/','/^((29([-\\/.]?)02\\3(\\d{2}([13579][26]|[2468][048]|04|08)|(1600|2[048]00)))|((((0[1-9]|1\\d|2[0-8])([-\\/.]?)(0[1-9]|1[012]))|((29|30)([-\\/.]?)(0[13-9]|1[012]))|(31([-\\/.]?)(0[13578]|1[02])))(\\11|\\15|\\18)\\d{4})) (\\d|[0-1]\\d|[2][0-3])(:[0-5]\\d){2}$/','datetime_seconds',NULL,1),('datetime_seconds_mdy','Datetime w/ seconds (M-D-Y H:M:S)','/^((02([-\\/.]?)29\\3(\\d{2}([13579][26]|[2468][048]|04|08)|(1600|2[048]00)))|((((0[1-9]|1[012])([-\\/.]?)(0[1-9]|1\\d|2[0-8]))|((0[13-9]|1[012])([-\\/.]?)(29|30))|((0[13578]|1[02])([-\\/.]?)31))(\\11|\\15|\\19)\\d{4})) (\\d|[0-1]\\d|[2][0-3])(:[0-5]\\d){2}$/','/^((02([-\\/.]?)29\\3(\\d{2}([13579][26]|[2468][048]|04|08)|(1600|2[048]00)))|((((0[1-9]|1[012])([-\\/.]?)(0[1-9]|1\\d|2[0-8]))|((0[13-9]|1[012])([-\\/.]?)(29|30))|((0[13578]|1[02])([-\\/.]?)31))(\\11|\\15|\\19)\\d{4})) (\\d|[0-1]\\d|[2][0-3])(:[0-5]\\d){2}$/','datetime_seconds',NULL,1),('datetime_seconds_ymd','Datetime w/ seconds (Y-M-D H:M:S)','/^(((\\d{2}([13579][26]|[2468][048]|04|08)|(1600|2[048]00))([-\\/.]?)02(\\6)29)|(\\d{4}([-\\/.]?)((0[1-9]|1[012])(\\9)(0[1-9]|1\\d|2[0-8])|((0[13-9]|1[012])(\\9)(29|30))|((0[13578]|1[02])(\\9)31)))) (\\d|[0-1]\\d|[2][0-3])(:[0-5]\\d){2}$/','/^(((\\d{2}([13579][26]|[2468][048]|04|08)|(1600|2[048]00))([-\\/.]?)02(\\6)29)|(\\d{4}([-\\/.]?)((0[1-9]|1[012])(\\9)(0[1-9]|1\\d|2[0-8])|((0[13-9]|1[012])(\\9)(29|30))|((0[13578]|1[02])(\\9)31)))) (\\d|[0-1]\\d|[2][0-3])(:[0-5]\\d){2}$/','datetime_seconds','datetime_seconds',1),('datetime_ymd','Datetime (Y-M-D H:M)','/^(((\\d{2}([13579][26]|[2468][048]|04|08)|(1600|2[048]00))([-\\/.]?)02(\\6)29)|(\\d{4}([-\\/.]?)((0[1-9]|1[012])(\\9)(0[1-9]|1\\d|2[0-8])|((0[13-9]|1[012])(\\9)(29|30))|((0[13578]|1[02])(\\9)31)))) (\\d|[0-1]\\d|[2][0-3]):[0-5]\\d$/','/^(((\\d{2}([13579][26]|[2468][048]|04|08)|(1600|2[048]00))([-\\/.]?)02(\\6)29)|(\\d{4}([-\\/.]?)((0[1-9]|1[012])(\\9)(0[1-9]|1\\d|2[0-8])|((0[13-9]|1[012])(\\9)(29|30))|((0[13578]|1[02])(\\9)31)))) (\\d|[0-1]\\d|[2][0-3]):[0-5]\\d$/','datetime','datetime',1),('email','Email','/^([_a-z0-9-\']+)(\\.[_a-z0-9-\']+)*@([a-z0-9-]+)(\\.[a-z0-9-]+)*(\\.[a-z]{2,4})$/i','/^([_a-z0-9-\']+)(\\.[_a-z0-9-\']+)*@([a-z0-9-]+)(\\.[a-z0-9-]+)*(\\.[a-z]{2,4})$/i','email',NULL,1),('integer','Integer','/^[-+]?\\b\\d+\\b$/','/^[-+]?\\b\\d+\\b$/','integer','int',1),('mrn_10d','MRN (10 digits)','/^\\d{10}$/','/^\\d{10}$/','text',NULL,0),('number','Number','/^[-+]?[0-9]*\\.?[0-9]+([eE][-+]?[0-9]+)?$/','/^[-+]?[0-9]*\\.?[0-9]+([eE][-+]?[0-9]+)?$/','number','float',1),('number_1dp','Number (1 decimal place)','/^-?\\d+\\.\\d$/','/^-?\\d+\\.\\d$/','number',NULL,0),('number_2dp','Number (2 decimal places)','/^-?\\d+\\.\\d{2}$/','/^-?\\d+\\.\\d{2}$/','number',NULL,0),('number_3dp','Number (3 decimal places)','/^-?\\d+\\.\\d{3}$/','/^-?\\d+\\.\\d{3}$/','number',NULL,0),('number_4dp','Number (4 decimal places)','/^-?\\d+\\.\\d{4}$/','/^-?\\d+\\.\\d{4}$/','number',NULL,0),('phone','Phone (U.S.)','/^(?:\\(?([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\\)?)\\s*(?:[.-]\\s*)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\\s*(?:[.-]\\s*)?([0-9]{4})(?:\\s*(?:#|x\\.?|ext\\.?|extension)\\s*(\\d+))?$/','/^(?:\\(?([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\\)?)\\s*(?:[.-]\\s*)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\\s*(?:[.-]\\s*)?([0-9]{4})(?:\\s*(?:#|x\\.?|ext\\.?|extension)\\s*(\\d+))?$/','phone',NULL,1),('phone_australia','Phone (Australia)','/^(\\(0[2-8]\\)|0[2-8])\\s*\\d{4}\\s*\\d{4}$/','/^(\\(0[2-8]\\)|0[2-8])\\s*\\d{4}\\s*\\d{4}$/','phone',NULL,0),('postalcode_australia','Postal Code (Australia)','/^\\d{4}$/','/^\\d{4}$/','postal_code',NULL,0),('postalcode_canada','Postal Code (Canada)','/^[ABCEGHJKLMNPRSTVXY]{1}\\d{1}[A-Z]{1}\\s*\\d{1}[A-Z]{1}\\d{1}$/i','/^[ABCEGHJKLMNPRSTVXY]{1}\\d{1}[A-Z]{1}\\s*\\d{1}[A-Z]{1}\\d{1}$/i','postal_code',NULL,0),('ssn','Social Security Number (U.S.)','/^\\d{3}-\\d\\d-\\d{4}$/','/^\\d{3}-\\d\\d-\\d{4}$/','ssn',NULL,0),('time','Time (HH:MM)','/^([0-9]|[0-1][0-9]|[2][0-3]):([0-5][0-9])$/','/^([0-9]|[0-1][0-9]|[2][0-3]):([0-5][0-9])$/','time',NULL,1),('time_mm_ss','Time (MM:SS)','/^[0-5]\\d:[0-5]\\d$/','/^[0-5]\\d:[0-5]\\d$/','time',NULL,0),('vmrn','Vanderbilt MRN','/^[0-9]{4,9}$/','/^[0-9]{4,9}$/','mrn',NULL,0),('zipcode','Zipcode (U.S.)','/^\\d{5}(-\\d{4})?$/','/^\\d{5}(-\\d{4})?$/','postal_code',NULL,1);
/*!40000 ALTER TABLE `redcap_validation_types` ENABLE KEYS */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
DROP TABLE IF EXISTS `redcap_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_data` (
  `project_id` int(10) NOT NULL DEFAULT '0',
  `event_id` int(10) DEFAULT NULL,
  `record` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `field_name` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `value` text COLLATE utf8_unicode_ci,
  KEY `event_id` (`event_id`),
  KEY `project_field` (`project_id`,`field_name`),
  KEY `proj_record_field` (`project_id`,`record`,`field_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `redcap_events_calendar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_events_calendar` (
  `cal_id` int(10) NOT NULL AUTO_INCREMENT,
  `record` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `project_id` int(10) DEFAULT NULL,
  `event_id` int(10) DEFAULT NULL,
  `baseline_date` date DEFAULT NULL,
  `group_id` int(10) DEFAULT NULL,
  `event_date` date DEFAULT NULL,
  `event_time` varchar(5) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'HH:MM',
  `event_status` int(2) DEFAULT NULL COMMENT 'NULL=Ad Hoc, 0=Due Date, 1=Scheduled, 2=Confirmed, 3=Cancelled, 4=No Show',
  `note_type` int(2) DEFAULT NULL,
  `notes` text COLLATE utf8_unicode_ci,
  `extra_notes` text COLLATE utf8_unicode_ci,
  PRIMARY KEY (`cal_id`),
  KEY `project_date` (`project_id`,`event_date`),
  KEY `project_record` (`project_id`,`record`),
  KEY `event_id` (`event_id`),
  KEY `group_id` (`group_id`),
  CONSTRAINT `redcap_events_calendar_ibfk_3` FOREIGN KEY (`group_id`) REFERENCES `redcap_data_access_groups` (`group_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `redcap_events_calendar_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `redcap_projects` (`project_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `redcap_events_calendar_ibfk_2` FOREIGN KEY (`event_id`) REFERENCES `redcap_events_metadata` (`event_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='Calendar Data';
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `redcap_log_event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_log_event` (
  `log_event_id` int(11) NOT NULL AUTO_INCREMENT,
  `project_id` int(10) NOT NULL DEFAULT '0',
  `ts` bigint(14) DEFAULT NULL,
  `user` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ip` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `page` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `event` enum('UPDATE','INSERT','DELETE','SELECT','ERROR','LOGIN','LOGOUT','OTHER','DATA_EXPORT','DOC_UPLOAD','DOC_DELETE','MANAGE','LOCK_RECORD','ESIGNATURE') COLLATE utf8_unicode_ci DEFAULT NULL,
  `object_type` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  `sql_log` mediumtext COLLATE utf8_unicode_ci,
  `pk` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `event_id` int(10) DEFAULT NULL,
  `data_values` text COLLATE utf8_unicode_ci,
  `description` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `legacy` int(1) NOT NULL DEFAULT '0',
  `change_reason` text COLLATE utf8_unicode_ci,
  PRIMARY KEY (`log_event_id`),
  KEY `user` (`user`),
  KEY `user_project` (`project_id`,`user`),
  KEY `object_type` (`object_type`),
  KEY `ts` (`ts`),
  KEY `event_project` (`event`,`project_id`),
  KEY `description` (`description`),
  KEY `pk` (`pk`)
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `redcap_docs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_docs` (
  `docs_id` int(11) NOT NULL AUTO_INCREMENT,
  `project_id` int(10) NOT NULL DEFAULT '0',
  `docs_date` date DEFAULT NULL,
  `docs_name` text COLLATE utf8_unicode_ci,
  `docs_size` double DEFAULT NULL,
  `docs_type` text COLLATE utf8_unicode_ci,
  `docs_file` longblob,
  `docs_comment` text COLLATE utf8_unicode_ci,
  `docs_rights` text COLLATE utf8_unicode_ci,
  `export_file` int(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`docs_id`),
  KEY `docs_name` (`docs_name`(128)),
  KEY `project_id_export_file` (`project_id`,`export_file`),
  KEY `project_id_comment` (`project_id`,`docs_comment`(128)),
  CONSTRAINT `redcap_docs_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `redcap_projects` (`project_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `redcap_locking_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_locking_data` (
  `ld_id` int(11) NOT NULL AUTO_INCREMENT,
  `project_id` int(10) DEFAULT NULL,
  `record` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `event_id` int(10) DEFAULT NULL,
  `form_name` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `username` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`ld_id`),
  UNIQUE KEY `proj_rec_event_form` (`project_id`,`record`,`event_id`,`form_name`),
  KEY `username` (`username`),
  KEY `event_id` (`event_id`),
  CONSTRAINT `redcap_locking_data_ibfk_2` FOREIGN KEY (`event_id`) REFERENCES `redcap_events_metadata` (`event_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `redcap_locking_data_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `redcap_projects` (`project_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `redcap_esignatures`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_esignatures` (
  `esign_id` int(11) NOT NULL AUTO_INCREMENT,
  `project_id` int(10) DEFAULT NULL,
  `record` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `event_id` int(10) DEFAULT NULL,
  `form_name` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `username` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`esign_id`),
  UNIQUE KEY `proj_rec_event_form` (`project_id`,`record`,`event_id`,`form_name`),
  KEY `username` (`username`),
  KEY `event_id` (`event_id`),
  CONSTRAINT `redcap_esignatures_ibfk_2` FOREIGN KEY (`event_id`) REFERENCES `redcap_events_metadata` (`event_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `redcap_esignatures_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `redcap_projects` (`project_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `redcap_surveys_participants`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_surveys_participants` (
  `participant_id` int(10) NOT NULL AUTO_INCREMENT,
  `survey_id` int(10) DEFAULT NULL,
  `event_id` int(10) DEFAULT NULL,
  `hash` varchar(10) CHARACTER SET latin1 COLLATE latin1_general_cs DEFAULT NULL,
  `legacy_hash` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Migrated from RS',
  `participant_email` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'NULL if public survey',
  `participant_identifier` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`participant_id`),
  UNIQUE KEY `hash` (`hash`),
  UNIQUE KEY `legacy_hash` (`legacy_hash`),
  KEY `participant_email` (`participant_email`),
  KEY `survey_event_email` (`survey_id`,`event_id`,`participant_email`),
  KEY `event_id` (`event_id`),
  CONSTRAINT `redcap_surveys_participants_ibfk_2` FOREIGN KEY (`event_id`) REFERENCES `redcap_events_metadata` (`event_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `redcap_surveys_participants_ibfk_1` FOREIGN KEY (`survey_id`) REFERENCES `redcap_surveys` (`survey_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='Table for survey data';
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `redcap_surveys_emails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_surveys_emails` (
  `email_id` int(10) NOT NULL AUTO_INCREMENT,
  `survey_id` int(10) DEFAULT NULL,
  `email_subject` text COLLATE utf8_unicode_ci,
  `email_content` text COLLATE utf8_unicode_ci,
  `email_sender` int(10) DEFAULT NULL COMMENT 'FK ui_id from redcap_user_information',
  `email_account` enum('1','2','3') COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Sender''s account (1=Primary, 2=Secondary, 3=Tertiary)',
  `email_static` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Sender''s static email address (only for scheduled invitations)',
  `email_sent` datetime DEFAULT NULL COMMENT 'Null=Not sent yet (scheduled)',
  PRIMARY KEY (`email_id`),
  KEY `email_sender` (`email_sender`),
  KEY `email_sent` (`email_sent`),
  KEY `survey_id_email_sent` (`survey_id`,`email_sent`),
  CONSTRAINT `redcap_surveys_emails_ibfk_1` FOREIGN KEY (`survey_id`) REFERENCES `redcap_surveys` (`survey_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `redcap_surveys_emails_ibfk_2` FOREIGN KEY (`email_sender`) REFERENCES `redcap_user_information` (`ui_id`) ON DELETE SET NULL ON UPDATE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='Track emails sent out';
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `redcap_surveys_response`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_surveys_response` (
  `response_id` int(11) NOT NULL AUTO_INCREMENT,
  `participant_id` int(10) DEFAULT NULL,
  `record` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `first_submit_time` datetime DEFAULT NULL,
  `completion_time` datetime DEFAULT NULL,
  `return_code` varchar(8) COLLATE utf8_unicode_ci DEFAULT NULL,
  `results_code` varchar(8) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`response_id`),
  UNIQUE KEY `participant_record` (`participant_id`,`record`),
  KEY `return_code` (`return_code`),
  KEY `results_code` (`results_code`),
  KEY `first_submit_time` (`first_submit_time`),
  KEY `completion_time` (`completion_time`),
  CONSTRAINT `redcap_surveys_response_ibfk_1` FOREIGN KEY (`participant_id`) REFERENCES `redcap_surveys_participants` (`participant_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `redcap_data_quality_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_data_quality_status` (
  `status_id` int(10) NOT NULL AUTO_INCREMENT,
  `rule_id` int(10) DEFAULT NULL COMMENT 'FK from data_quality_rules table',
  `pd_rule_id` int(2) DEFAULT NULL COMMENT 'Name of pre-defined rules',
  `non_rule` int(1) DEFAULT NULL COMMENT '1 for non-rule, else NULL',
  `project_id` int(11) DEFAULT NULL,
  `record` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `event_id` int(10) DEFAULT NULL,
  `field_name` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Only used if field-level is required',
  `status` int(2) DEFAULT NULL COMMENT 'Current status of discrepancy',
  `exclude` int(1) NOT NULL DEFAULT '0' COMMENT 'Hide from results',
  `query_status` enum('OPEN','CLOSED','VERIFIED','DEVERIFIED') COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Status of data query',
  `assigned_user_id` int(10) DEFAULT NULL COMMENT 'UI ID of user assigned to query',
  PRIMARY KEY (`status_id`),
  UNIQUE KEY `rule_record_event` (`rule_id`,`record`,`event_id`),
  UNIQUE KEY `pd_rule_proj_record_event_field` (`pd_rule_id`,`record`,`event_id`,`field_name`,`project_id`),
  UNIQUE KEY `nonrule_proj_record_event_field` (`non_rule`,`project_id`,`record`,`event_id`,`field_name`),
  KEY `event_id` (`event_id`),
  KEY `pd_rule_proj_record_event` (`pd_rule_id`,`record`,`event_id`,`project_id`),
  KEY `project_query_status` (`project_id`,`query_status`),
  KEY `assigned_user_id` (`assigned_user_id`),
  CONSTRAINT `redcap_data_quality_status_ibfk_4` FOREIGN KEY (`assigned_user_id`) REFERENCES `redcap_user_information` (`ui_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `redcap_data_quality_status_ibfk_1` FOREIGN KEY (`rule_id`) REFERENCES `redcap_data_quality_rules` (`rule_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `redcap_data_quality_status_ibfk_2` FOREIGN KEY (`event_id`) REFERENCES `redcap_events_metadata` (`event_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `redcap_data_quality_status_ibfk_3` FOREIGN KEY (`project_id`) REFERENCES `redcap_projects` (`project_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `redcap_ddp_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_ddp_records` (
  `mr_id` int(10) NOT NULL AUTO_INCREMENT,
  `project_id` int(10) DEFAULT NULL,
  `record` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL COMMENT 'Time of last data fetch',
  `item_count` int(10) DEFAULT NULL COMMENT 'New item count (as of last viewing)',
  `fetch_status` enum('QUEUED','FETCHING') COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Current status of data fetch for this record',
  PRIMARY KEY (`mr_id`),
  UNIQUE KEY `project_record` (`project_id`,`record`),
  KEY `project_updated_at` (`updated_at`,`project_id`),
  KEY `project_id_fetch_status` (`fetch_status`,`project_id`),
  CONSTRAINT `redcap_ddp_records_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `redcap_projects` (`project_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `redcap_ip_cache`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_ip_cache` (
  `ip_hash` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `timestamp` timestamp NULL DEFAULT NULL,
  KEY `timestamp` (`timestamp`),
  KEY `ip_hash` (`ip_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `redcap_page_hits`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_page_hits` (
  `date` date NOT NULL,
  `page_name` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `page_hits` float NOT NULL DEFAULT '1',
  UNIQUE KEY `date` (`date`,`page_name`),
  KEY `page_name` (`page_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `redcap_sessions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redcap_sessions` (
  `session_id` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `session_data` text COLLATE utf8_unicode_ci,
  `session_expiration` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`session_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='Stores user authentication session data';
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

