if (chrome) {
	fnd = chrome;
} else if (browser) {
	fnd = browser;
}

function changeCheck(){
	var now = document.getElementById('agree').checked;
	if(now){
		fnd.storage.sync.set({agree:'ok'});
		alert("동의하셨습니다.")
		page_replace();
	} else {
		fnd.storage.sync.set({agree:'no'});
	}
}

function page_replace(){
	fnd.storage.sync.get('agree', function(data){
		var agree = data.agree;
		if(agree == 'ok'){
			document.location.href="popup.html"
		}
	});
}

document.addEventListener('DOMContentLoaded', function(){
	document.getElementById("agree").addEventListener('change', changeCheck);
	//document.querySelector("#off").addEventListener('change', changeCheck);
	page_replace();
});