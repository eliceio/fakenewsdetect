function processing_tag(post_str, url, cfunc)
{  
  if (window.XMLHttpRequest)
  {// code for IE7+, Firefox, Chrome, Opera, Safari
    xmlhttp=new XMLHttpRequest();
  }
  else
  {// code for IE6, IE5
    xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
  }

  xmlhttp.onreadystatechange=function()
  {
    if (xmlhttp.readyState == 4 && xmlhttp.status == 200)
    {
      cfunc(xmlhttp.responseText);
    }
  }
  xmlhttp.open("POST", url, true);
  xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xmlhttp.send(post_str);
}

function GetTweet()
{
  processing_tag("", "processing_get_tweet.php", GetTweetFunc);
}

function GetTweetFunc(responseText)
{     
  if(responseText.indexOf("Error!!") > -1)
  {
    alert("Error!!");
  }
  else
  {
    var obj = JSON.parse(responseText);
    document.getElementById("tweet_content").innerHTML = obj.content;
    document.getElementById("tweetid").value = obj.id;
  }
}

function answering(answer)
{
  var tweetid = document.getElementById("tweetid").value;
  var post_str = "tweetid=" + tweetid + "&answer=" + answer;
  
  processing_tag(post_str, "processing_answering.php", answeringFunc);
}

function answeringFunc(responseText)
{
  if(responseText.indexOf("Error") > -1)
  {
    alert(responseText);
  }
  else
  {
    GetTweet();
  }
}

