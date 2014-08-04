<?php

interface API_DB_Statement {
   function execute();
   // function executeWithParams($params);
   function __sleep();
}
