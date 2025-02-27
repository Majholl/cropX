document.addEventListener('DOMContentLoaded' , async function() {

    let scrollCointainer = document.querySelector('.container-images');
    let backbtn = document.getElementById('previous-img');
    let nxtbtn = document.getElementById('next-img');

    scrollCointainer.addEventListener('wheel', (evnt)=>{
        
        scrollCointainer.scrollLeft += evnt.deltaY;
    }  , {passive: true})


    nxtbtn.addEventListener('click' , (event)=>{
        event.preventDefault();
        scrollCointainer.scrollLeft += 900;

    })

    backbtn.addEventListener('click' , (event)=>{
        event.preventDefault();
        scrollCointainer.scrollLeft -= 900;
        
    })

})








const activeImg = function(event) {
    event.preventDefault();
    let imgactivate = event.target
    let showImgsbtndiv = document.getElementById('imgsbuttondiv');
    showImgsbtndiv.style.display = 'flex';

    let baseurl = `${window.location.protocol}//${window.location.host}`
    let imgNewUrl = imgactivate.src.replace(baseurl, "");

    let dropdownItems = document.getElementsByClassName('dropdown-item');
    let btnDanger = document.getElementById('removebtn').setAttribute('data-src' , imgNewUrl)
    let getImgs = document.getElementsByClassName('img-class');

    for (let i=0 ; i < getImgs.length ; i++){
        getImgs[i].classList.remove('active');}


   for(let i=0; i < dropdownItems.length ; i++){
        dropdownItems[i].setAttribute('data-src' ,imgNewUrl)}

   imgactivate.classList.add('active')  
}











document.addEventListener('click', async function (event) {
    if (event.target.classList.contains('dropdown-item')) {
        event.preventDefault();
    
        let RotateAngle = parseInt(event.target.getAttribute('data-rotate'));
        let ImgSrc = event.target.getAttribute('data-src');


        const csrfToken = document.cookie.split(';');
        let csrfTokenValue = '';
        csrfToken.forEach(cookie => {
            let [name, value] = cookie.trim().split('=');
            csrfTokenValue = value;
        });

        const dataToSendServer = {
            imagepath: ImgSrc,
            imageangle: RotateAngle
        };


        try {
            
            let response = await fetch(`${window.location.protocol}//${window.location.host}/rotate/`, {
                method: 'POST',
                headers: { 'content-type': 'application/json', 'X-CSRFToken': csrfTokenValue },
                body: JSON.stringify(dataToSendServer)
            });

            let result = await response.json();
            if (result.status == 200) {
                let ImgElement = document.querySelector(`img[src="${ImgSrc}"]`);
                ImgElement.src = result.data;

                console.log(':-Img requested rotated-:');}


        } catch (err) {
            console.log("Error updating image:", err);
        }
    }
});









document.addEventListener('click' , async function(event){
    if (event.target.classList.contains('delete-btn')){
        event.preventDefault();

        let ImgSrc = event.target.getAttribute('data-src');
       
        const csrfToken = document.cookie.split(';');
        let csrfTokenValue = '';
        csrfToken.forEach(cookie =>{
            let [name , value ] =cookie.trim().split('=');
            csrfTokenValue = value;
        });

        const dataToSendServer = {
            imagepath : ImgSrc};

        try {
            let response = await fetch(`${window.location.protocol}//${window.location.host}/remove/` , {
                method:'POST',
                headers :{'content-type':'application/json' , 'X-CSRFToken':csrfTokenValue},
                body : JSON.stringify(dataToSendServer)});

            let result = await response.json();
            if (result.status == 200){
                let RemoveImg = document.querySelector(`img[data-src="${ImgSrc}"]`);
                RemoveImg.closest('.images-list').remove()
                console.log(`Image removed successfully`);}
                let showImgsbtndiv = document.getElementById('imgsbuttondiv');
                showImgsbtndiv.style.display = 'none';

        } catch (err) {

            console.log("Error removing image:", err);
        }

    }
})









document.addEventListener('DOMContentLoaded', async function () {
    let sortedList = [];
    
    new Sortable(document.getElementById("orderimglist"), {
        animation: 150,
        ghostClass: "dragging",
        onEnd: async function (evt) {

            sortedList = Array.from(evt.from.children).map(item => item.dataset.src);
            const csrfToken = document.cookie.split(';');

            let csrfTokenValue = '';
            csrfToken.forEach(cookie =>{
            let [name , value ] =cookie.trim().split('=');
            csrfTokenValue = value;});

            const dataToSendServer = {imageorder : sortedList,};


            let response = await fetch(`http://${window.location.host}/reorder/` , {
                method:'POST',
                headers :{'content-type':'application/json' , 'X-CSRFToken':csrfTokenValue},
                body : JSON.stringify(dataToSendServer),});
                    

            let result = await response.json();
                if (result.status == 200){
                    console.log(result.data)};

            console.log('sorted Order ' , sortedList)}});

})    











document.addEventListener('DOMContentLoaded', function() {
    let saveInput = document.getElementById('reordersaveing');
    if (saveInput) {
        saveInput.addEventListener('submit', async function(event) {
            event.preventDefault();
            let buttonText = document.getElementById('saveandoutput');
            let disableFeatures = document.getElementById('imgsbuttondiv').style.display = 'none'
            buttonText.disabled = true;
            buttonText.textContent = 'Downloading process started';
            let userId = document.getElementById('reordersaveing').getAttribute('action').split('/')[2];
            const csrfToken = document.cookie.split(';');
            let csrfTokenValue = '';
            csrfToken.forEach(cookie => {
                let [name, value] = cookie.trim().split('=');
                csrfTokenValue = value;
            });

            let response = await fetch(`http://${window.location.host}/download/`, {
                method: 'POST',
                headers: { 'content-type': 'application/json', 'X-CSRFToken': csrfTokenValue },
                body: JSON.stringify({ data: 'download the file' }),
            });

            let result = await response.json();
                if (result.status == 200) {
                    console.log(response.status)
        };
    
})
}
})




