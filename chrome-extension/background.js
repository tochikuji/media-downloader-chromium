chrome.contextMenus.create({
    id: "downloadVideo",
    title: "Download Video",
    contexts: ["link", "page"]
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
    if (info.menuItemId === "downloadMedia") {
        let videoUrl;

        if (info.linkUrl) {
            videoUrl = info.linkUrl;
        } else if (info.pageUrl) {
            videoUrl = info.pageUrl;
        }

        console.log(`Sending ${videoUrl} to the server for downloading`);

        fetch("http://localhost:19988", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url: videoUrl })
        })
            .then(response => response.json())
            .then(data => console.log(data))
            .catch(error => console.error('Error:', error));
    }
});
