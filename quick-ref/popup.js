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

        titleAndUrls.forEach(cur => {
            bracketLinks = '('
            if (cur.pageNo.length >= 1) {
                console.log("hi")
                for (const page of cur.pageNo) {
                    bracketLinks += `<a target="_blank" href="http://localhost:8000/${cur.pdf}#page=${page}"
>${page}</a>, `
                }
                bracketLinks = bracketLinks.slice(0, -2)
                bracketLinks+=')'
            }
            inject = `<div class="card result">
            <div class="card-header result-title">
                <a target="_blank" href="http://localhost:8000/${cur.pdf}#page=${cur.pageNo[0]}">
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

        // this output is like
        // <div className="result">
        //     <div className="result-title">
        //      <a target="_blank" href="http://localhost:8000/Introduction%20to%20Public%20key%20cryptosystem.pdf#page=15">page
        //         - 15 : Introduction to Public key cryptosystem.pdf</a>
        //         </div>
        //     <p style="border: 1px solid black;">
        //     Public -Key Cryptosystem: <br>Confidentiality
        //     <br> <br></p>
        // </div>

        // titleAndUrls.forEach(cur => {
        //     let ne = document.createElement('div')
        //     ne.className = 'result'
        //     let ne2 = document.createElement('div')
        //     ne2.className = 'result-title'
        //     let lnk = document.createElement('a')
        //     lnk.target = '_blank'
        //     lnk.href = "http://localhost:8000/"+ cur.url.split('/')[cur.url.split('/').length - 1]
        //     lnk.innerText = cur.title
        //     ne2.appendChild(lnk)
        //     ne.appendChild(ne2)
        //     let content = document.createElement('p')
        //     content.innerText = cur.content;
        //     content.style.border = "1px solid black";
        //     ne.appendChild(content)
        //     searchList.appendChild(ne)
        // })
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