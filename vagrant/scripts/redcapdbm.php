<?php
/**
*  RedCap Data Base Manager (redcapdbm) script allows to perform
*  a list of tasks against the RedCapP database:
*
*     - List the names of the projects in the RedCap database
*     - Delete the data for a specific `project_id`
*     - Backup the database schema and partial data
*
*  The scripts is invoked in the command line and expects a parameter corresponding
*  to the `redcap.redcap_pojects.project_id` primary key.
*
*  To get help pass the `-h` option to the script.
*
*  @author Andrei Sura
*/
require_once 'phplib/common.php';
require_once 'phplib/UtilApp.php';

$app = UtilApp::getInstance();

$options = getopt('hld:b');
//var_dump($options);

$showHelp      = isset($options['h']);
$listProjects  = isset($options['l']);
$projID        = isset($options['d']) ? $options['d'] : null;
$doBackup      = isset($options['b']);

$usage = '
RedCap DataBase Manager

Usage: php redcapdbm.php [<options>]
where <options> are:
   -h    Show help
   -l    List the names of the projects in the RedCap database
   -d    Delete the data for a specific `project_id`
   -b    Backup the database schema and partial data
';

if ($listProjects) {
   $app->printProjectsList();
   exit;
}
if ($doBackup) {
   $app->backupRedcapDB();
   exit;
}

if ($showHelp || ! $projID) {
   echo $usage;
   exit;
}

$proj = $app->getProjectDetails($projID);
if (! $proj) {
   echo "\nThe project with id: $projID was not found in the database\n";
}
else {
   echo "\n<br />Deleting data for project: " . $proj['project_id'] . ', name: ' . $proj['project_name'];
   echo "\nTotal rows deleted: " . $app->cleanProjectData($projID) . "\n";
}

