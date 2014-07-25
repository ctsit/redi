<?php
/**
*  Declare the list of methods for parsing query results
*
*  @see API_DB.php#execute()
*  @see API_DB.php#executeWithParams()
*
*  @see API_DB_Result_Maria
*
*  @author Andrei Sura
*/ 
interface API_DB_Result {
   function rowCount();
   function fetch(); 
}
