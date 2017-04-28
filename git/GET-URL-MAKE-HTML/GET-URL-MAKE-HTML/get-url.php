
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en"><head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta  name="author" content="Jack Northrup" />
<title>GET URL</title>
<link rel="stylesheet" href="URL.css" />
</head>
<body>
<div id="wrapper">

<div id="center-column">
<div id="post">

<form action="get-url-insert.php" method="post">

Keywords:&nbsp;&nbsp;
<textarea cols="70" rows="3" name="origkeywords" value="text"></textarea><br /><br />
URL:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<textarea cols="70" rows="10" name="origpage" value=""></textarea><br /><br />
<input type= "submit" name= "submit" value="Enter"/>
</form> <br />
<?php
header('Content-Type: text/html; charset=UTF-8');
?>
<?php include('get-url-connect.php'); ?>
<?php
//execute the SQL query and return records
$result = mysql_query("SELECT * FROM `urls`" . "ORDER BY `ID` DESC LIMIT 15");
//fetch the data from the database
?>
<div class="boxit">
<?php 
while ($row = mysql_fetch_array($result)) {
echo "ID -"
.$row['id']."&nbsp;&nbsp;&nbsp;Date:"
.$row['date']."<br />"; 
$page = base64_decode($row['page'])."<br />";
$keywords = $row['keywords'];
echo $keywords."<br />";
echo $page."<br /><br /><hr>";


}
?>


?>
</div>
</div>

</body>
</html>

