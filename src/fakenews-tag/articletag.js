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

function GetArticle()
{
  processing_tag("", "processing_get_article.php", GetArticleFunc);
}

function GetArticleFunc(responseText)
{     
  if(responseText.indexOf("Error!!") > -1)
  {
    alert("Error!!");
  }
  else
  {
    var obj = JSON.parse(responseText);
    document.getElementById("article_content").innerHTML = obj.content;
    document.getElementById("article_title").innerHTML = "Title: " + obj.title;
    document.getElementById("articleid").value = obj.id;
  }
}

function answering(answer)
{
  var articleid = document.getElementById("articleid").value;
  var post_str = "articleid=" + articleid + "&answer=" + answer;
  
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
    GetArticle();
  }
}

