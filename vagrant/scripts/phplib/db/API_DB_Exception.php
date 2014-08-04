<?php
/**
*  Implement custom database exception handling
*
*  @author Andrei Sura
*/
class API_DB_Exception extends PDOException {
   public $errorCode;

   public function __construct($error, $errorCode) {
      parent::__construct($error); 
      $this->errorCode = $errorCode;
   }
   
   public static function handle(PDOException $pdoExc) {
      throw new API_DB_Exception($pdoExc->getMessage(), $pdoExc->getCode());
   }

}
