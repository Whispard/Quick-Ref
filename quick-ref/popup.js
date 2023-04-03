let cb = async (e, error) => {
    e.preventDefault();

    console.log("event", e);
    let q = document.querySelector('#search-box').value;
    console.log(q)
    let updateList = (titleAndUrls) => {
        let searchList = document.querySelector('#main')
        while (searchList.children.length > 0) {
            searchList.removeChild(searchList.children[0])
        }
        if (titleAndUrls.length === 0) {
            let e = document.createElement('div')
            e.textContent = "No results found"
            e.align = "center"
            searchList.appendChild(e)
        }

        const makeUrlFromPDFPage = (url,index) => {
            if (url.includes("#page="))
                return url
            return `http://localhost:7860/open-reader/${index}`
        }

        titleAndUrls.forEach(cur => {
            bracketLinks = '('
            if (cur.pageNo.length >= 1) {
                console.log("hi")
                for (let i=0;i<cur.pageNo.length;i++) {
                    bracketLinks += `<a  href="${makeUrlFromPDFPage(cur.url,i)}"
>${cur.pageNo[i]}</a>, `
                }
                bracketLinks = bracketLinks.slice(0, -2)
                bracketLinks+=')'
            }
            inject = `<div class="card result">
            <div class="card-header result-title">
                <a href="${makeUrlFromPDFPage(cur.url,0)}">
                    ${cur.pdf.split('.pdf')[0]}</a>
                ${bracketLinks}
               
                </a>
            </div>
            <div class="card-body" style="padding: 0;padding-left: 15px">
                <p class="card-text">${cur.content}</p>
          </div>
        </div>`
            let ne = document.createElement('div')
            ne.innerHTML = inject
            searchList.appendChild(ne)
        })
    }


    console.log("waiting");
    let prgbar = document.getElementById("my-progress-bar")
    prgbar.style.display = "";
    const response = await fetch("http://127.0.0.1:7860/", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            data:q,
            num: 5,
            summarised: summarise
        })
    });
    prgbar.style.display='none'
    const datas = await response.json();
    console.log(datas)

    // const betterTitle = (prevTitle) => {
    //     return prevTitle
    //     let title = prevTitle.split(' : ')[1].split('.pdf')[0]
    //     // return prevTitle
    //     return title
    // }


    // console.log(`Title:${data.title},Url:${data.uri},Content:${data.content}`);
    if (q != document.querySelector('#search-box').value) {
        return;
    }

    updateList(datas.map(data =>
        ({url: data.uri, pdf:data.pdf,pageNo:data.pageNo,content:data.content}))
    )

}
let summarise = false;




document.querySelector('#search-form')
    .addEventListener("submit", cb)

document.querySelector("#search-form")
    .addEventListener("search", cb, false)


document.querySelector('#full-screen')
    .addEventListener("click", (e) => {
        e.target.href = "https://google.com/search?q=" + document.querySelector('#search-box').value;

    })

// chrome.runtime.sendMessage({selection:window.getSelection().toString()}, function(response) {
//     console.log(response.farewell);
// }

async function getCurrentTab() {
    let queryOptions = {active: true, currentWindow: true};
    let [tab] = await chrome.tabs.query(queryOptions);
    return tab;
}


chrome.runtime.onMessage.addListener(
    function (request, sender, sendResponse) {
        document.getElementById("search-box").value = request.selection;
        const searchEvent = new Event("search",)
        document.querySelector('#search-form').dispatchEvent(searchEvent); //This would trigger the event listene
    }
);


getCurrentTab().then(t => {
    chrome.scripting.executeScript({
        target: {tabId: t.id},
        func: () => {
            chrome.runtime.sendMessage({selection: window.getSelection().toString()}, function (response) {
            });
        }
    })
})


document.querySelector('#search-form')
    .addEventListener("keyup",cb)

document.querySelector('#library')
    .addEventListener("click",(event)=>{
        event.preventDefault();
        summarise = true;
        cb(event);



    })




window.addEventListener('click', evt => {

    // ユーザーの操作によるイベントならisTrusted == true
    // If event is fired by user's operation then isTrusted == true.
    // Chrome 46.0～
    // https://developer.mozilla.org/ja/docs/Web/API/Event/isTrusted
    if (!evt.isTrusted) return;
    let target = evt.target;
    while (target && target.tagName.toLowerCase() !== 'a' && target.tagName.toLowerCase() !== 'area') {
        target = target.parentElement;
    }
    if (target) {
        // check for baseVal of svg a tag's href-SVGAnimatedString
        const url = target instanceof SVGAElement ? target.href.baseVal : target.href;
        if (url.startsWith('file://')) {
            evt.preventDefault();
            // 拡張が再読み込みされた場合エラーになるので捕捉
            // Catch the error for the extension is reloaded.
            console.log("file found")
            try {
                //chrome.runtime.getBackgroundPage().backgroundFunction();
                chrome.runtime.sendMessage({
                    method: 'openLocalFile',
                    localFileUrl: url,
                });
            } catch (e) {
                console.log(e)
            }
        }
    }
}, {
    capture: true,
});