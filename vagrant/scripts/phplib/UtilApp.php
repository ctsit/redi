<?php
/**
*  This class is an utility application used to
*  run custom queries on the redcap database.
*
*  @author  : Andrei Sura 
*/

class UtilApp {
   private $conn;
   static $instance;

   // The following properties can be stored
   // in a config file or the $_SERVER environment variable
   static $UTIL_DB_HOST = 'localhost';
   static $UTIL_DB_USER = 'root';
   static $UTIL_DB_PASS = 'password';
   static $UTIL_DB_NAME = 'redcap';

   static $BACKUP_FILE_PREFIX = 'backup-redcap-';

   static $TABLES_IGNORE_DATA = array(
      'redcap_data',
      'redcap_events_calendar',
      'redcap_log_event',
      'redcap_docs',
      'redcap_locking_data',
      'redcap_esignatures',
      'redcap_surveys_participants',
      'redcap_surveys_emails',
      'redcap_surveys_response',
      'redcap_data_quality_status',
      'redcap_ddp_records',
      'redcap_ip_cache',
      'redcap_page_hits',
      'redcap_sessions',
   );

   public static function getInstance() {
      if (! self::$instance) {
         self::$instance = new UtilApp();
      }
      return self::$instance;
   }

   private function __construct() {
      $this->setupConnection();
   }

   private function setupConnection() {
      $urlObj = API_DB::createDbUrl(
         self::$UTIL_DB_HOST,
         self::$UTIL_DB_USER,
         self::$UTIL_DB_PASS
      );

      // var_dump($urlObj);
      $url = $urlObj->getUrl();
      $this->conn = API_DB::connect($url);
      $this->conn->useDB('redcap');
   }

   /** 
   *  Accessor for database connection attribute
   */ 
   public function getConn() {
      return $this->conn;
   }   

   /**
   *  Deletes rows in a similar way to how is done in redcap web interface.
   *
   *  TODO: If necessary also run an extra update query:
   *   update redcap_edocs_metadata set delete_date = now() where project_id = $project_id and doc_id in ($fileFieldEdocIds)");
   *
   *  @see #cleanMainTables()
   *  @see #cleanDerivedTables()
   */
   public function cleanProjectData($projID) {
      $count = 0;
      $count += $this->cleanDerivedTables($projID);
      $count += $this->cleanMainTables($projID);
      $count += $this->cleanExtraTables($projID);
      $this->showHelpQuery();

      return $count;
   }

   public function cleanExtraTables($projID) {
      $deleteAll = array(
         'redcap_ip_cache',
         'redcap_page_hits',
         'redcap_sessions',
      );

      $c = 0;
      foreach ($deleteAll as $table) {
         $query = "DELETE FROM $table";
         // echo "\nQuery: $query\n";
         $result = $this->conn->query($query);
         if (! $result) {
            return self::getErrors("\n<br /> Unable to delete data for table: $table");
         }
         $c += $result->rowCount();
         echo "\n Rows deleted in cleanExtraTables(): $c";
      }
      return $c;
   }

   /**
   *  Remove data from tables which have 
   *  `redcap_project.project_id` as a column
   */
   public function cleanMainTables($projID) {
      $c = 0;
      $queries = array(
'DELETE FROM    redcap_data                 WHERE project_id = ?',
'DELETE FROM    redcap_events_calendar      WHERE project_id = ?',
"DELETE FROM    redcap_log_event            WHERE project_id = ?
               AND event IN ('UPDATE', 'INSERT', 'DELETE', 'DATA_EXPORT', 'DOC_UPLOAD', 'DOC_DELETE', 'OTHER')",
'DELETE FROM    redcap_docs                 WHERE project_id = ?',
'DELETE FROM    redcap_locking_data         WHERE project_id = ?',
'DELETE FROM    redcap_esignatures          WHERE project_id = ?',
'DELETE FROM    redcap_data_quality_status  WHERE project_id = ?',
'DELETE FROM    redcap_ddp_records          WHERE project_id = ?',
'DELETE FROM    redcap_log_view             WHERE project_id = ?',
);
      foreach ($queries as $query) {
         // echo "\nQuery: $query\n";
         $result = $this->conn->prepare($query)->execute($projID);
         if (! $result) {
            return self::getErrors("\n<br /> Unable to delete data for projID: $projID");
         }
         $c += $result->rowCount();
         echo "\n Rows deleted in cleanMainTables(): $c";
      }
      return $c;
   }


   /**
   *  Deletes data from tables which store data about surveys.
   */
   public function cleanDerivedTables($projID) {
      $surveys = $this->getProjectSurveys($projID);
      foreach ($surveys as $survey_id => $data) {
         echo "\nDeleting data for survey_id: `" . $survey_id 
            . "`, form_name: `" . $data['form_name'] . "`, title: " . $data['title'] . "\n";
      }

      // surveys responses
      $query = <<<SQL
DELETE
   res
FROM
   redcap_surveys_response AS res
   JOIN redcap_surveys_participants AS part ON (res.participant_id = part.participant_id)
   JOIN redcap_surveys AS surv ON(part.survey_id = surv.survey_id)
   JOIN redcap_projects AS proj ON(surv.project_id = proj.project_id)
WHERE
   proj.project_id = ?
SQL;

      $result = $this->conn->prepare($query)->execute($projID);
      if (! $result) {
         return self::getErrors("\n<br /> Unable to delete data for projID: $projID");
      }
      $c = $result->rowCount();
      echo "\n Rows deleted from `redcap_surveys_response`:" . $c;

      // delete from surveys_participants and surveys_emails
      $query = <<<SQL
DELETE
   redcap_surveys_participants
FROM
   redcap_surveys_participants
   NATURAL JOIN redcap_surveys
   NATURAL JOIN redcap_projects
WHERE
   project_id = ?
SQL;
      $result = $this->conn->prepare($query)->execute($projID);
      if (! $result) {
         return self::getErrors("\n<br /> Unable to delete data for projID: $projID");
      }
      $c2 = $result->rowCount();
      $c += $c2;
      echo "\n Rows deleted from `redcap_surveys_participants`:" . $c2;

      $query = <<<SQL
DELETE
   redcap_surveys_emails
FROM
   redcap_surveys_emails
   NATURAL JOIN redcap_surveys
   NATURAL JOIN redcap_projects
WHERE
   project_id = ?
SQL;
      $result = $this->conn->prepare($query)->execute($projID);
      if (! $result) {
         return self::getErrors("\n<br /> Unable to delete data for projID: $projID");
      }
      $c3 = $result->rowCount();
      $c += $c3;
      echo "\n Rows deleted from `redcap_surveys_emails`:" . $c;
  
      return $c;
   }


   /**
   *  Helper function for building a list of errors
   */
   public static function getErrors($err, $list = array()) {
      if ( isset ($list['errors'])) {
         $list['errors'][] = $err;
      }
      else {
         $list['errors'] = array($err);
      }

      return $list;
   }

   /** 
   *  @see #getProjectsList()
   */
   public function printProjectsList() {
      $list = $this->getProjectsList();
      echo "\n The following projects are currently available in the redcap database: \n";
      foreach($list as $id => $proj) {
         echo "\nproject_id: $id, project_name: " . $proj['project_name'];
      }
      echo "\n";
   }

   /**
   *  Retrives details about a specific redcap project.
   *  @see #getProjectsList()
   */
   public function getProjectDetails($project_id) {
      $proj = null;
      $list = $this->getProjectsList();
      if (isset($list[$project_id])) {
         $proj = $list[$project_id];
      }
      return $proj;
   }

   /**
   *  @return basic information about a project
   */
   public function getProjectsList() {
      $query = <<<SQL
SELECT
   project_id, project_name, app_title
FROM
   redcap_projects
SQL;

      // echo "\nExec: $query\n";
      $list = array();
      try {
         $result = $this->conn->query($query);
         while ($row = $result->fetch()) {
            $project_id = $row['project_id'];
            $list[$project_id] = $row;
         }
      }
      catch (Exception $e) {
         echo "\nFailed due: $e\n";
      }

      return $list;
   }

   /**
   *  @return an array of survey data entries
   */
   public function getProjectSurveys($project_id) {
      $query = <<<SQL
SELECT
   project_id, survey_id, form_name, title 
FROM
   redcap_surveys
WHERE
   project_id = ?
SQL;

      // echo "\nExec: $query\n";
      $list = array();
      try {
         $ps = $this->conn->prepare($query);
         $result = $ps->execute($project_id);
         while ($row = $result->fetch()) {
            $survey_id = $row['survey_id'];
            $list[$survey_id] = $row;
         }
      }
      catch (Exception $e) {
         echo "\nFailed due: $e\n";
      }

      return $list;
   }

   /**
   *  Displays a help query which can be used to verify that row counts
   *  have changed after adding/removing project data.
   *
   *  @see #cleanProjectData()
   */
   // public function showHelpQuery($project_id) {
   public function showHelpQuery() {
      echo "\n
--------------------------------------------------------------------------------
You can run the following query to verify the row counts:\n";
      $query = <<<SQL

SELECT 'redcap_projects' AS tableName,                   COUNT(*) FROM redcap_projects
UNION SELECT 'redcap_data' AS tableName,                 COUNT(*) FROM redcap_data
UNION SELECT 'redcap_events_calendar' AS tableName,      COUNT(*) FROM redcap_events_calendar
UNION SELECT 'redcap_log_event' AS tableName,            COUNT(*) FROM redcap_log_event
UNION SELECT 'redcap_docs' AS tableName,                 COUNT(*) FROM redcap_docs
UNION SELECT 'redcap_locking_data' AS tableName,         COUNT(*) FROM redcap_locking_data
UNION SELECT 'redcap_esignatures' AS tableName,          COUNT(*) FROM redcap_esignatures
UNION SELECT 'redcap_surveys' AS tableName,              COUNT(*) FROM redcap_surveys
UNION SELECT 'redcap_surveys_participants' AS tableName, COUNT(*) FROM redcap_surveys_participants
UNION SELECT 'redcap_surveys_emails' AS tableName,       COUNT(*) FROM redcap_surveys_emails
UNION SELECT 'redcap_surveys_response' AS tableName,     COUNT(*) FROM redcap_surveys_response
UNION SELECT 'redcap_ip_cache',                          COUNT(*) FROM redcap_ip_cache
UNION SELECT 'redcap_log_view',                          COUNT(*) FROM redcap_log_view
UNION SELECT 'redcap_page_hits',                         COUNT(*) FROM redcap_page_hits
UNION SELECT 'redcap_sessions',                          COUNT(*) FROM redcap_sessions
SQL;
      echo $query;
   }

   /**
   *  Retrives the list of tables in the `redcap` database
   */
   public function getTablesForDB($schemaName) {
      $query = <<<SQL
SELECT
   TABLE_SCHEMA, TABLE_NAME
FROM
   information_schema.TABLES
WHERE
   TABLE_SCHEMA = ?
   AND TABLE_TYPE = 'BASE TABLE'
SQL;

      // echo "\nExec: $query\n";
      $list = array();
      try {
         $ps = $this->conn->prepare($query);
         $result = $ps->execute($schemaName);

         while ($row = $result->fetch()) {
            $list[] = $row['TABLE_NAME'];
         }
      }
      catch (Exception $e) {
         echo "\nFailed due: $e\n";
      }
      return $list;
   }


   /**
   *  Executes two mysqldump commands 
   */
   public function backupRedcapDB() {
      /*
      $tables = $this->getTablesForDB(self::$UTIL_DB_NAME);
      $tablesString = implode(',', $tables);
      $out = system("echo $tablesString", $retVal);
      echo $out;
      */

      // create timestamped file name
      $fileName = self::$BACKUP_FILE_PREFIX . date('Ymd-hi', time()) . '.sql';

      // building the string 'db.table_a, db.table_b...''
      $ignoreList = self::$UTIL_DB_NAME . '.' 
         . implode(',' . self::$UTIL_DB_NAME . '.', self::$TABLES_IGNORE_DATA);
      $schemaList = implode(' ', self::$TABLES_IGNORE_DATA);
      $options = ' --skip-add-locks --skip-comments --skip-set-charset --single-transaction';

      $cmdBackupAll =
'mysqldump -u ' . self::$UTIL_DB_USER
. ' -p' . self::$UTIL_DB_PASS  
. ' -h ' . self::$UTIL_DB_HOST . ' ' . self::$UTIL_DB_NAME 
. $options
. " --ignore-table=$ignoreList > $fileName";

      $retVal = 0;
      $out = system($cmdBackupAll, $retVal);
      // echo "\n$cmdBackupAll\n";
      // echo "\n Output: $out";

      if ($retVal) {
         echo "\nThe command $cmdBackupAll returned $retVal";
      }

      $cmdBackupSchema = 
'mysqldump -u ' . self::$UTIL_DB_USER
. ' -p' . self::$UTIL_DB_PASS  
. ' -h ' . self::$UTIL_DB_HOST . ' ' . self::$UTIL_DB_NAME
. $options
. " --no-data $schemaList >> $fileName";

      $out = system($cmdBackupSchema, $retVal);
      if ($retVal) {
         echo "\nThe command $cmdBackupSchema returned $retVal";
      }

      // output the created file size
      system("echo 'Backup file created: ' && du -h $fileName");
   }

}
