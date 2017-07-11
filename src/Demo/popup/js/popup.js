if (chrome) {
	fnd = chrome;
} else if (browser) {
	fnd = browser;
}

function restore_options() {
	fnd.storage.sync.get('OnOffSwitch', function(data){
		var OnOffSwitch = data.OnOffSwitch;
		if(OnOffSwitch == 'on'){
			$("#OnOffSwitch").bootstrapSwitch('state',true);
		} else {
			$("#OnOffSwitch").bootstrapSwitch('state',false);
		}
	});
}

function changeCheck(){
	var now = document.getElementById('OnOffSwitch').checked;
	if(now){
		fnd.storage.sync.set({OnOffSwitch:'on'});
	} else {
		fnd.storage.sync.set({OnOffSwitch:'off'});
	}
}

function getURL(){
	fnd.storage.sync.get('OnOffSwitch', function(data){
		var OnOffSwitch = data.OnOffSwitch;
		if(OnOffSwitch == 'on'){
			fnd.tabs.query({'active': true, 'lastFocusedWindow': true}, function (tabs) {
				var url = tabs[0].url;
				var title = tabs[0].title;
				document.getElementById('articleTitle').innerHTML = title;
				document.getElementById('articleURL').innerHTML = url;
			});
		} else {
			
		}
	});
}
document.addEventListener('DOMContentLoaded', function(){
	$("#OnOffSwitch").on('change.bootstrapSwitch', function(){
		changeCheck();
	});
	getURL();
	restore_options();
});
