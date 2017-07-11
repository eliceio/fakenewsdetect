if (chrome) {
  yns = chrome;
} else if (browser) {
  yns = browser;
}

// 검색엔진 뉴스 기사 URL 전송
if (document.URL.indexOf("search.naver.com") != -1) {
  newsURL = $(".news").find(".type01").find("dl").find("a");
  for(var i in newsURL) {
    if (newsURL[i].href.indexOf("naver.com") == -1 && newsURL[i].title) {
      console.log("[sendMessage] " + newsURL[i].title + newsURL[i].href);

      yns.runtime.sendMessage({title: newsURL[i].title, url: newsURL[i].href, num: i}, function(response) {
        // 응답 처리
        console.log("[response: " + response.percent + (response.percent > 60.0) + "] " + response.title + response.url);
        showResult(response.percent, response.num);
        return;
      });
    }
  }
} else if (document.URL.indexOf("search.daum.net") != -1) {
  // view.daum.net 링크...
  newsURL = $("#clusterResultUL").find(".wrap_cont").find("a");
  for(var i in newsURL) {
    if (newsURL[i].href.indexOf("?f=o") != -1
     || newsURL[i].href.indexOf("daum.net") == -1) {
      console.log("[sendMessage] " + newsURL[i].text + newsURL[i].href);

      yns.runtime.sendMessage({title: newsURL[i].text, url: newsURL[i].href, num: i}, function(response) {
        // 응답 처리
        console.log("[response: " + response.percent + (response.percent > 60.0) + "] " + response.title + response.url);
        showResult(response.percent, response.num);
        return;
      });
    }
  }
}

function showResult(percent, num) {
  // 개발 단계니까 잘 보이게 하기 위해서
  if (percent > 60.0) { // 확실
    newsURL[num].style = "color: darkred; font-weight: bold;";
  } else if (percent > 50.0) {  // 애매
    newsURL[num].style = "color: IndianRed; font-weight: bold;";
  }
  return;
}

// 뉴스 기사 페이지 추천, 비추천, 신고 표시
yns.storage.local.get('press', function(result){
  for (var i in result.press) {
    if (document.URL.indexOf(result.press[i]) != -1) {
      console.log("press match");
      $.get(yns.extension.getURL('article.html'), function(data) {
        $(data).appendTo('body');
        // Or if you're using jQuery 1.8+:
        // $($.parseHTML(data)).appendTo('body');
      });
      break;
    }
  }

	return;
});
