if (chrome) {
  fnd = chrome;
} else if (browser) {
  fnd = browser;
}

// 실행 시에 서버에서 언론사 목록 로드
$.getJSON("http://eliceteam.nosyu.pe.kr/press.json", function(data){
  fnd.storage.local.set({
    press:  data.press
  });
});

// content-scripts.js 메시지 처리
fnd.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    $.getJSON("http://eliceteam.nosyu.pe.kr/checkURL", { title: request.title, url: request.url }, function(data){
      sendResponse({title: request.title, url: request.url, percent: data.percent, num: request.num});
    });
    return true;
});
