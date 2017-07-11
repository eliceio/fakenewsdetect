<?php
session_start();
if(isset($_SESSION["annotator_id"]) && isset($_POST["articleid"]) && isset($_POST["answer"]))
{
	$accountid = $_SESSION["annotator_id"];
	$articleid = $_POST["articleid"];
	$answer = $_POST["answer"];

	// DB
    // Hide these values for sharing
	$mysql_url = "localhost";
	$mysql_user = "root";
	$mysql_password = "root";
	$mysql_db = "fakenews";

	$mysqli = new mysqli($mysql_url,$mysql_user,$mysql_password,$mysql_db);
	if (mysqli_connect_errno())
	{
	    echo "Failed to connect to MySQL: " . mysqli_connect_error();
	    exit;
	}
	$mysqli->query('set names utf8');

	# Insert the result
	if ($stmt = $mysqli->prepare("INSERT INTO annotations (annotator, article_id, atime, answer) VALUES (?, ?, now(), ?)")) 
	{
		$stmt->bind_param("iii", $accountid, $articleid, $answer);
	    $stmt->execute();
	    $stmt->close();
	}
	else
	{
		echo "Error!";
		exit;
	}

	# Update the result
	if ($stmt = $mysqli->prepare("UPDATE articles tt set tt.annotated = tt.annotated + 1 where tt.id = ?")) 
	{
		$stmt->bind_param("i", $articleid);
	    $stmt->execute();
	    $stmt->close();
	}
	else
	{
		echo "Error!!";
		exit;
	}
	$mysqli->close();

	// output the response
	echo "Good!";
}
else
{
	echo "Error!!!";
}
?>
