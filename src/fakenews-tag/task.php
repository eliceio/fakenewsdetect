<?php

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

// Start the session
session_start();

if(empty($_POST["InputEmail1"]))
{
    print("<h2>Please enter <a href='index.php'>your email address</a>.</h2>");
    header( "refresh:5;url=https://eliceteam.nosyu.pe.kr");
    exit;
}

//if(!isset($_SESSION["email_address"]))
$_SESSION["email_address"] = $_POST["InputEmail1"];
$email_address = $_SESSION["email_address"];

// Insert the email address if it is not in the table
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
$email_insert_query_template = "INSERT INTO annotators (email) VALUES (?)";
if ($stmt = $mysqli->prepare($email_insert_query_template)) 
{
    $stmt->bind_param("s", $email_address);
    $stmt->execute();
    $stmt->close();
}

if ($stmt = $mysqli->prepare("SELECT * FROM annotators where email=?")) 
{
    $stmt->bind_param("s", $email_address);
    $stmt->execute();

    $stmt->bind_result($annotator_id, $annotator_email);
    $stmt->fetch();

    $stmt->close();

    $_SESSION["annotator_id"] = $annotator_id;
}

if ($stmt = $mysqli->prepare("SELECT count(*) from annotations ann where ann.annotator = ?")) 
{
    $stmt->bind_param("s", $annotator_id);
    $stmt->execute();

    $stmt->bind_result($done_tweets);
    $stmt->fetch();

    $stmt->close();
}

?>
<html><head>
        <title>FakeNews - Annotating fake or not</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jquery/2.0.3/jquery.min.js"></script>
        <script type="text/javascript" src="https://netdna.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js"></script>
        <script type="text/javascript" src="articletag.js"></script>
        <script type="text/javascript">
            GetArticle();
        </script>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.3.0/css/font-awesome.min.css" rel="stylesheet" type="text/css">
        <link href="https://pingendo.github.io/pingendo-bootstrap/themes/default/bootstrap.css" rel="stylesheet" type="text/css">
    </head><body>
        <div class="navbar navbar-default navbar-static-top">
            <div class="container">
                <div class="navbar-header">
                    <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#navbar-ex-collapse">
                        <span class="sr-only">Toggle navigation</span>
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                    </button>
                </div>
                <div class="collapse navbar-collapse" id="navbar-ex-collapse">
                    <ul class="nav navbar-nav navbar-right">
                        <li>
                            <a href="index.php">Home</a>
                        </li>
                        <li class="active">
                            <a href="#">Task</a>
                        </li>
                    </ul>
                    <p class="navbar-text navbar-right">Signed in as <a href="#" class="navbar-link"><?php echo $annotator_email;?></a></p></div>
                </div>
            </div>
        </div>
        <div class="section">
            <div class="container">
                <div class="row">
                    <div class="col-md-12">
                        <h1>Tagging fake news - fake or not?</h1>
                    </div>
                </div>
                
                <div class="row">
                    <div class="col-md-12">
                        <hr>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-14">
                        <ul class="lead">
                            <div>This task is annotating fake news whether these are 
                                fake or not.&nbsp;</div>For each task, you can see a news that
                            is written in Korean, for 2016.06 ~ 2017.06.&nbsp;
                            <br>Then, please answer the question:
                            <b>Is this fake news or not?&nbsp;</b>
                            <br>To answer the question,
                            <b>please click the green/red button</b>.&nbsp;
                            <br />
                            <br />Thanks for your work: <b><?php echo $done_tweets;?></b> tweets tagged
                            <br /><br />Team in charge: fakenewsdetect (https://github.com/eliceio/fakenewsdetect)
                        </ul>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-12">
                        <hr>
                        <h2 class="text-center" id="article_title">##ARTICLE_TITLE##</h2>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-12">
                        <h1 class="text-center" id="article_content">##ARTICLE_CONTENT##</h1>
                    </div>
                </div>
            </div>
        </div>
        <div class="section">
            <div class="container">
                <div class="row">
                <form role="form">
                    <input type="hidden" id="articleid" value="0">
                    <div class="col-md-4">
                        <button type="button" class="btn btn-block btn-lg btn-success" onclick="javascript:answering(1);return false;">Yes - fake news</button>
                    </div>
                    <div class="col-md-4">
                        <button type="button" class="btn btn-block btn-lg btn-warning" onclick="javascript:answering(3);return false;">Don't know - Fake? Not?</a>
                    </div>
                    <div class="col-md-4">
                        <button type="button" class="btn btn-block btn-danger btn-lg" onclick="javascript:answering(2);return false;">No - it's real one!</button>
                    </div>
                </form>
                </div>
            </div>
        </div>
    

</body></html>

<?php
$mysqli->close();
?>
