<?php
/**
*  Implements the declared function in API_DB_Statement.php
*
*  @author Andrei Sura
*/
class API_DB_Statement_Maria implements API_DB_Statement {
   private $pdo;
   private $ps;
  
   public function __construct(PDO $pdo, PDOStatement $ps) {
      $this->pdo = $pdo;
      $this->ps = $ps;
   }

   public function execute() {
      $argZero = func_get_arg(0);

      try {
         if (! func_num_args()) {
            $this->ps->execute();
         }
         else if (is_array($argZero)) {
            $this->ps->execute($argZero);
         }
         else {
            $this->ps->execute(func_get_args());      
         }
      }
      catch(Exception $pdoe) {
         API_DB_Exception::handle($pdoe);
      }      
      return new API_DB_Result_Maria($this->ps);
   }

   public function executeWithParams($params) {
      return $this->execute($params);
   }

   public function __sleep() {
      return array();
   }
}
