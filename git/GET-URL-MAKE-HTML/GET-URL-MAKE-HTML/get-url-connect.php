<?php
//connection to the database
$hostname = "localhost";
$username = "root";
$password = "";
$dbhandle = mysql_connect($hostname, $username, $password)
or die("Unable to connect to MySQL");

//select a database to work with
$selected = mysql_select_db("geturl",$dbhandle)
or die("Could not select geturl");
?>
