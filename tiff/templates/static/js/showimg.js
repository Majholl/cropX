document.addEventListener('click', async function (event){
    if (event.target.classList.contains('dropdown-item')){
        event.preventDefault();
    
        let RotateAngle = parseInt(event.target.getAttribute('data-rotate'));
        let ImgSrc = event.target.getAttribute('data-src');
        console.log(`rotate Angle ${RotateAngle} for IMG ${ImgSrc}`);

        const csrfToken = document.cookie.split(';');
        let csrfTokenValue = '';
        csrfToken.forEach(cookie =>{
            let [name , value ] =cookie.trim().split('=');
            csrfTokenValue = value;
        });

        const dataToSendServer = {
            imagepath : ImgSrc,
            imageangle : RotateAngle};

        let response = await fetch('http://127.0.0.1:8000/rotate/' , {
            method:'POST',
            headers :{'content-type':'application/json' , 'X-CSRFToken':csrfTokenValue},
            body : JSON.stringify(dataToSendServer)});

        let result = await response.json();
        if (result.status == 200){
            let ImgElement = document.querySelector(`img[data-src="${ImgSrc}"`);
            ImgElement.src = result.data};

};
})









document.addEventListener('click' , async function(event){
    if (event.target.classList.contains('delete-btn')){
        event.preventDefault();

        let ImgSrc = event.target.getAttribute('data-src');
        console.log(`Img ${ImgSrc}`);

        const csrfToken = document.cookie.split(';');
        let csrfTokenValue = '';
        csrfToken.forEach(cookie =>{
            let [name , value ] =cookie.trim().split('=');
            csrfTokenValue = value;
        });

        const dataToSendServer = {
            imagepath : ImgSrc};

        let response = await fetch('http://127.0.0.1:8000/remove/' , {
            method:'POST',
            headers :{'content-type':'application/json' , 'X-CSRFToken':csrfTokenValue},
            body : JSON.stringify(dataToSendServer)});

        let result = await response.json();
        if (result.status == 200){
            let RemoveImg = event.target.closest('.container-images');
            await RemoveImg.remove();
            console.log(`Image removed successfully`);
        }

    }
})









document.addEventListener('DOMContentLoaded', async function () {
    let sortedList = [];

    new Sortable(document.getElementById("image-list"), {
        animation: 150,
        ghostClass: "dragging",
        onEnd: function (evt) {
            sortedList = Array.from(evt.from.children).map(item => item.dataset.src);
            console.log('sorted Order ' , sortedList)}});

            
    document.getElementById('reordersaveing').addEventListener('submit' , async function (event){
        event.preventDefault();


        const csrfToken = document.cookie.split(';');
        let csrfTokenValue = '';
        csrfToken.forEach(cookie =>{
            let [name , value ] =cookie.trim().split('=');
            csrfTokenValue = value;
        });


        const dataToSendServer = {
            imagepath : sortedList,};


        let response = await fetch('http://127.0.0.1:8000/reorder/' , {
            method:'POST',
            headers :{'content-type':'application/json' , 'X-CSRFToken':csrfTokenValue},
            body : JSON.stringify(dataToSendServer),});
        

        let result = await response.json();
        if (result.status == 200){
            console.log(result.data)};

    });
})