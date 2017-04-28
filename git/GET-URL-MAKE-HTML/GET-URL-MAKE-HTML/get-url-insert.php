<?php
header('Content-Type: text/html; charset=UTF-8');

$con=mysqli_connect("localhost","root","","geturl");
// Check connection
if (mysqli_connect_error())
  {
  echo "Failed to connect to MySQL SERVER: " . mysqli_connect_error();
  }

$keywords = $_POST[origkeywords];
$page1 = file_get_contents($_POST[origpage]);
$page = base64_encode($page1);
  $sql="INSERT INTO urls (keywords, page)
VALUES
('$keywords','$page')";
if (!mysqli_query($con,$sql))
  {
  die('Error - Failed to post: ' . mysqli_error($con));
  }
mysqli_close($con);
header("Location: get_url.php");
  
  ?>

<?php
header('Content-Type: text/html; charset=UTF-8');
?>
<?php include('get-connect.php'); ?>
<?php
//execute the SQL query and return records
$result = mysql_query("SELECT * FROM `urls`" . " ORDER BY `ID` DESC LIMIT 5 ");
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




