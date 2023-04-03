console.log("hi")


chrome.runtime.onMessage.addListener((message, sender) => {
	if (message.method === 'openLocalFile') {
        console.log("called a listener");
		chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
  // The active tab is the first tab in the array
  var activeTab = tabs[0];
  console.log(activeTab);
		const localFileUrl = message.localFileUrl;
		openLocalFile(localFileUrl, activeTab);
});
	}
});


const openLocalFile = (localFileUrl, baseTab) => {
    console.log("called openLocalFile");
	chrome.tabs.create({
		url: localFileUrl,
		index: baseTab.index + 1,
	});
};