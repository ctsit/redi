<?php
/**
*  Implementations of this abstract class are used for database interaction.
*
*  @author Andrei Sura
*/

abstract class API_DB {

   /**
   *  Select a database
   *
   *  @throw API_DB_Exception
   */
   abstract function useDB($dbName);

   /**
   *  Sanitize the query to prevent SQL-injections
   *  @return API_DB_Statement object
   */
   abstract function prepare($queryString);

   /**
   *  Execute a prepared statement
   */
   //abstract function query(API_DB_Statement $ps);
   abstract function query($ps);

   /**
   *  @return the id of the row inserted 
   */
   abstract function lastInsertId();

   /**
   *  Sanitize a string
   */
   abstract function quoteString($str);

   abstract function beginTransaction();
   abstract function commit();
   abstract function rollBack();

   abstract function close();
   abstract function __sleep();


   // Can be used to add support for other database types 
   public static function connect($url) {
      $schema = parse_url($url, PHP_URL_SCHEME);
      if ('mysql' == $schema) {
         require_once 'phplib/db/maria/API_DB_Maria.php';
         require_once 'phplib/db/maria/API_DB_Statement_Maria.php';
         require_once 'phplib/db/maria/API_DB_Result_Maria.php';
         return new API_DB_Maria($url);
      }
      // else if ('other' == $schema) { return new API_DB_Other($url)}
      return NULL;
   }

   /**
   *  @return an instance of `API_DB_Url` class
   */
   public static function createDbUrl(
      $host,
      $user = NULL,
      $pass = NULL,
      $schema = NULL,
      $port = NULL,
      $dbname = NULL,
      $params = NULL) {
      
      if (! isset($schema)) {
         $schema = 'mysql';
      }
      
      $url = $schema . '://';
      if (isset($user)) {
         $url .= urlencode($user);

         if (isset($pass)) {
            $url .= ':' . urlencode($pass);
         }
      }

      if (isset($user) || isset($pass)) {
         $url .= '@';
      }
      
      $url .= $host;

      if (isset($port)) {
         $url .= $port;
      }

      if (isset($dbname)) {
         $url .= '/' . $dbname;
      }

      if (isset($params)) {
         $url .= '?' .http_build_query($params);
      }
         
      return new API_DB_Url($url); 
   }
}
