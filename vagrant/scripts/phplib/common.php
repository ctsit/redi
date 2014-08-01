<?php
/**
*  Stores common include statements.
*
*  @author Andrei Sura
*/
$new = get_include_path().':./phplib/';
set_include_path($new);

require_once 'db/API_DB.php';
require_once 'db/API_DB_Result.php';                                                                                                                                                                                                          
require_once 'db/API_DB_Statement.php';
require_once 'db/API_DB_Url.php';
require_once 'db/API_DB_Exception.php';
