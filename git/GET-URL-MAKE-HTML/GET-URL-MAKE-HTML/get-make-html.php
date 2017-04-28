<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en"><head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta  name="author" content="Jack Northrup" />
<title>Make-HTML-from-SQL-Data</title>
<link rel="stylesheet" href="URL.css" />
</head>
<body>
<div id="wrapper">
<div id="center-column">
<div id="post">
<form action="" method="post">
Enter ID -:<input type="text" name="data" /><br /><br />
Save as PageName:&nbsp;&nbsp;
<textarea cols="50" rows="2" name="pagename" value="text"></textarea><br /><br />
<input type= "submit" name= "makeit" value="Enter"/>
</form> <br />
<?php
header('Content-Type: text/html; charset=UTF-8');
?>
<?php include('get-url-connect.php'); ?>
<?php
//execute the SQL query and return records


if (isset($_POST["makeit"]) && !empty($_POST["pagename"])) {
$data = $_POST['data'];
$pagename = $_POST['pagename'];
$min_length = 10;
if(strlen($pagename) >= $min_length){ 
$result = mysql_query("SELECT * FROM urls WHERE id= '$data'");
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
$file = $pagename.'.html';
file_put_contents($file, $page);
}
}?>
<?php Echo "<h2>CLICK RED FILENAME TO VIEW HTML:<a style='color:red;' href=$file>$pagename</a></h2>" ?>
<?php
}
?><hr><br /><br /><br /><br />
</div>
</div>
</div>
</div>
</body>
</html>

