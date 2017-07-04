<?php
session_start();
if(isset($_SESSION["annotator_id"]) && isset($_POST["tweetid"]) && isset($_POST["answer"]))
{
	$accountid = $_SESSION["annotator_id"];
	$tweetid = $_POST["tweetid"];
	$answer = $_POST["answer"];

	// DB
    // Hide these values for sharing
	$mysql_url = "";
	$mysql_user = "";
	$mysql_password = "";
	$mysql_db = "";

	$mysqli = new mysqli($mysql_url,$mysql_user,$mysql_password,$mysql_db);
	if (mysqli_connect_errno())
	{
	    echo "Failed to connect to MySQL: " . mysqli_connect_error();
	    exit;
	}
	$mysqli->query('set names utf8');

	# Insert the result
	if ($stmt = $mysqli->prepare("INSERT INTO annotations (annotator, tweet_id, atime, answer) VALUES (?, ?, now(), ?)")) 
	{
		$stmt->bind_param("iii", $accountid, $tweetid, $answer);
	    $stmt->execute();
	    $stmt->close();
	}
	else
	{
		echo "Error!";
		exit;
	}

	# Update the result
	if ($stmt = $mysqli->prepare("UPDATE tweets tt set tt.annotated = tt.annotated + 1 where tt.id = ?")) 
	{
		$stmt->bind_param("i", $tweetid);
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