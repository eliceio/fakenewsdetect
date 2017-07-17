<?php
session_start();
error_reporting(E_ALL);
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
    $query_template = "SELECT bb.id, bb.article_id from (SELECT * from (SELECT * from articles tt where tt.id not in (SELECT aa.article_id from annotations aa where aa.annotator = ?) and tt.annotated < 20) aa order by aa.annotated limit 20) bb order by rand() limit 1;";

    if ($stmt = $mysqli->prepare($query_template))
    {
        $stmt->bind_param("i", $accountid);
        $stmt->execute();

        $stmt->bind_result($article_id, $file_name);
        $is_exist_row = $stmt->fetch();

        $stmt->close();
    }
    
    if($is_exist_row)
    {
          $file_name = "articles/" . $file_name . ".txt";
          $file = fopen($file_name, "r");
          $fr = fread($file, filesize($file_name));
          $article_total = explode("\n", $fr);
          $article_title = $article_total[0];
          $article_url = $article_total[1];
          $article_content = join("<br>\n", array_slice($article_total, 2, count($article_total)));
          fclose($file);
        echo json_encode(array('id'=>$article_id, 'title'=>$article_title,'url'=>$article_url, 'content'=>$article_content));
    }
    else
    {
        $query_template = "SELECT bb.id, bb.article_id from (SELECT * from (SELECT * from articles tt where tt.id not in (SELECT aa.article_id from annotations aa where aa.annotator = ?)) aa order by aa.annotated limit 20) bb order by rand() limit 1;";
        
        if ($stmt = $mysqli->prepare($query_template))
        {
            $stmt->bind_param("i", $accountid);
            $stmt->execute();

            $stmt->bind_result($article_id, $article_content);
            $is_exist_row = $stmt->fetch();

            $stmt->close();
        }
        
        // output the response
        if($is_exist_row)
        {
          $file = fopen("articles/".$file_name+".txt", "r");
          $fr = fread($file, filesize("articles/".$file_name));
          $article_title = split("\n", $fr);
          $article_title = $article_title[0];
          fclose($file);
          echo json_encode(array('id'=>$article_id, 'title'=>$article_title, 'content'=>$fr));
        }
        else
        {
            echo json_encode(array('id'=>0, 'title'=>"Nothing Left!", 'content'=>"Done! Thank you very much!"));    
        }
    }
    
    $mysqli->close();
}
else
{
    echo "<p>Error!!</p>";
}
?>
