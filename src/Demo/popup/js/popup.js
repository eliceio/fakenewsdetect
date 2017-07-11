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

document.addEventListener('DOMContentLoaded', function(){
	$("#OnOffSwitch").on('change.bootstrapSwitch', function(){
		changeCheck();
	});
	restore_options();
});
