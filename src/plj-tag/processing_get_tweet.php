<?php
session_start();
if(isset($_SESSION["annotator_id"]))
{
    $accountid = $_SESSION["annotator_id"];
    
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
    $how_times_tag = 4;
    
    // Original
    $query_template = "SELECT bb.id, bb.tweet from (SELECT * from (SELECT * from tweets tt where tt.id not in (SELECT aa.tweet_id from annotations aa where aa.annotator = ?) and tt.annotated < ?) aa order by aa.annotated limit 20) bb order by rand() limit 1;";
    // Type 5
    $query_template = "SELECT bb.id, bb.tweet from (SELECT * from (SELECT * from tweets tt where tt.id not in (SELECT aa.tweet_id from annotations aa where aa.annotator = ?) and tt.source_type = 5) aa order by aa.annotated limit 20) bb order by rand() limit 1;";
    // Type over 100 means for evaluating
    $query_template = "SELECT bb.id, bb.tweet from (SELECT * from (SELECT * from tweets tt where tt.id not in (SELECT aa.tweet_id from annotations aa where aa.annotator = ?) and tt.source_type > 100) aa order by aa.annotated limit 20) bb order by rand() limit 1;";
    // Type over 205 means for doing EMNLP 2017 short paper
    // First, do 205
    $query_template = "SELECT bb.id, bb.tweet from (SELECT * from (SELECT * from tweets tt where tt.id not in (SELECT aa.tweet_id from annotations aa where aa.annotator = ?) and tt.source_type = 205) aa order by aa.annotated limit 20) bb order by rand() limit 1;";
    // First, do 300
    $query_template = "SELECT bb.id, bb.tweet from (SELECT * from (SELECT * from tweets tt where tt.id not in (SELECT aa.tweet_id from annotations aa where aa.annotator = ?) and tt.source_type = 300) aa order by aa.annotated limit 20) bb order by rand() limit 1;";

    if ($stmt = $mysqli->prepare($query_template))
    {
        $stmt->bind_param("i", $accountid);
        $stmt->execute();

        $stmt->bind_result($tweet_id, $tweet_content);
        $is_exist_row = $stmt->fetch();

        $stmt->close();
    }
    
    if($is_exist_row)
    {
        echo json_encode(array('id'=>$tweet_id, 'content'=>$tweet_content));
    }
    else
    {
        $query_template = "SELECT bb.id, bb.tweet from (SELECT * from (SELECT * from tweets tt where tt.id not in (SELECT aa.tweet_id from annotations aa where aa.annotator = ?) and tt.source_type >= 300) aa order by aa.annotated limit 20) bb order by rand() limit 1;";
        
        if ($stmt = $mysqli->prepare($query_template))
        {
            $stmt->bind_param("i", $accountid);
            $stmt->execute();

            $stmt->bind_result($tweet_id, $tweet_content);
            $is_exist_row = $stmt->fetch();

            $stmt->close();
        }
        
        // output the response
        if($is_exist_row)
        {
            echo json_encode(array('id'=>$tweet_id, 'content'=>$tweet_content));    
        }
        else
        {
            echo json_encode(array('id'=>0, 'content'=>"Done! Thank you very much!"));    
        }
    }
    
    $mysqli->close();
}
else
{
    echo "<p>Error!!</p>";
}
?>