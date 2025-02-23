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

        let response = await fetch(`http://${window.location.host}/rotate/` , {
            method:'POST',
            headers :{'content-type':'application/json' , 'X-CSRFToken':csrfTokenValue},
            body : JSON.stringify(dataToSendServer)});



        let result = await response.json();
        if (result.status == 200){
            console.log(result.data)
            
            let ImgElement = document.querySelector(`img[data-src="${ImgSrc}"]`);
            let queryonDataSrc = document.querySelectorAll(`[data-src=${CSS.escape(ImgSrc)}]`);

            ImgElement.src = result.data;

            queryonDataSrc.forEach(elm =>{
                elm.setAttribute('data-src', result.data);
            })}

        else{
            alert(result.data)
        }
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

        let response = await fetch(`http://${window.location.host}/remove/` , {
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
            let saveInput = document.getElementById('saveandoutput');
            
            saveInput.disabled = true;
            saveInput.textContent = 'Downloading process started';
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
