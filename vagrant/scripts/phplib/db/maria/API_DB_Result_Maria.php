<?php
/**
*  Implements the declared function in API_DB_Result.php
*
*  @author Andrei Sura
*/
class API_DB_Result_Maria implements API_DB_Result {
   private $rs;

   // Construct a `result` object instance from the PDOStatement
   public function __construct(PDOStatement $rs) {
      $this->rs = $rs;
   }

   public function rowCount() {
      try {
         return $this->rs->rowCount();
      }
      catch (Exception $pdoe) {
         API_DB_Exception::handle($pdoe);
      }
   }

   public function fetch() {
      try {
         return $this->rs->fetch();
      }
      catch (Exception $pdoe) {
         API_DB_Exception::handle($pdoe);
      }
   }
}
