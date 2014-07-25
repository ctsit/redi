<?php
/**
*  Stores the fragments of an URL used to create database connections.
*
*  @author Andrei Sura
*/
class API_DB_Url {
   private $url;

   private $user;
   private $pass;

   private $host;
   private $port;
   private $dbname;

   // split the URL: 
   public function __construct($url) {

// echo "\n<br /> construct: $url";
      $this->url = $url;

      $parts = parse_url($url);

      if (isset($parts['user'])) {
         $this->user = urldecode($parts['user']);
      }
      if (isset($parts['pass'])) {
         $this->pass = urldecode($parts['pass']);
      }
      // host is required
      $this->host = $parts['host'];

      // port is optional
      if (isset($parts['port'])) {
         $this->port = $parts['port'];
      }

      // dbname is optional
      if (isset($parts['path']) && strlen($parts['path'])) {
         $this->dbname = substr($parts['path'], 1);
      }
   }

   public function getUrl() {
      return $this->url;
   }

   public function getUser() {
      return $this->user;
   }
   public function getPass() {
      return $this->pass;
   }

   /**
   *  @return string - host=xyz;port=abc;dbname=someDB
   * 
   *  @see http://www.php.net/manual/en/pdo.connections.php
   *  @see maria/API_DB_Maria.php#__construct()
   */
   public function getParams() {
      $params = '';

      if (isset($this->host)) {
         $params .= "host={$this->host};";
      }
      if (isset($this->port)) {
         $params .= "port={$this->port};";
      }
      if (isset($this->dbname)) {
         $params .= "dbname={$this->dbname};";
      }
      $params .= 'charset=utf8';
      return $params;
   }
}
