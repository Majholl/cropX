document.addEventListener('click', async function (event) {
    if (event.target.classList.contains('dropdown-item')) {
        event.preventDefault();
    
        let RotateAngle = parseInt(event.target.getAttribute('data-rotate'));
        let ImgSrc = event.target.getAttribute('data-src');
        

        const csrfToken = document.cookie.split(';');
        let csrfTokenValue = '';
        csrfToken.forEach(cookie => {
            let [name, value] = cookie.trim().split('=');
            if (name =='csrftoken'){
            csrfTokenValue = value;}
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
                let ImgElement = document.querySelector(`img[data-src="${ImgSrc}"]`);
                let newSrc = result.data + "?t=" + new Date().getTime(); 
                ImgElement.src = newSrc
                console.log("ImgElement Rotated successfully")
            }
                
        } catch (err) {
            console.log("Error updating image:", err);
        }
    }
});






document.addEventListener('click', async function(event) {
   
  
    if (event.target.classList.contains('softdelete-btn')) {
        let ImgSrc = event.target.getAttribute('data-src');
        let softRemove = document.querySelector(`[data-src="${ImgSrc}"]`);
        event.preventDefault();

        if (softRemove) {
            event.preventDefault();
       
            softRemove.querySelector('a').remove();
            softRemove.querySelector('div').remove();

            let pInfo = document.createElement('p');
            pInfo.classList.add('removeimgp');
            pInfo.textContent = 'Are you sure to remove this Image?';
            softRemove.appendChild(pInfo);

           
            let btonUndo = document.createElement('button');
            btonUndo.type = 'submit';
            btonUndo.classList.add('btn', 'btn-light', 'funbtns', 'undo-btn');
            btonUndo.id = 'Undo';
            btonUndo.setAttribute('data-src', ImgSrc);

            let iIconUndo = document.createElement('i');
            iIconUndo.classList.add('fa', 'fa-rotate-left');
            btonUndo.appendChild(iIconUndo);
            btonUndo.appendChild(document.createTextNode('No , don\'t delete the image'));

           
            let btonPermDelete = document.createElement('button');
            btonPermDelete.type = 'submit';
            btonPermDelete.classList.add('btn', 'btn-light', 'funbtns', 'harddelete-btn');
            btonPermDelete.id = 'removebtnhard';
            btonPermDelete.setAttribute('data-src', ImgSrc);

            let iIconPermDelete = document.createElement('i');
            iIconPermDelete.classList.add('fa', 'fa-trash');
            btonPermDelete.appendChild(iIconPermDelete);
            btonPermDelete.appendChild(document.createTextNode('Yes , remove the image'));

            softRemove.appendChild(btonUndo);
            softRemove.appendChild(btonPermDelete);
        }
    }

   
    if (event.target.classList.contains('undo-btn')) {
        event.preventDefault();
        let ImgSrc = event.target.getAttribute('data-src');
        let undoFunc = document.querySelector(`[data-src="${ImgSrc}"]`);
        if (undoFunc) {
            undoFunc.querySelector('p').remove();
            undoFunc.querySelectorAll('button').forEach(button => button.remove());

            
            let createAtag = document.createElement('a');
            createAtag.href = ImgSrc;
            createAtag.setAttribute("data-lightbox", "mygallery");
            createAtag.setAttribute("data-src", ImgSrc);

            let createImg = document.createElement('img');
            createImg.src = ImgSrc;
            createImg.classList.add("img-class");
            createImg.setAttribute("data-src", ImgSrc);
            createImg.style.width = '350px';
            createImg.style.height = '450px';

            createAtag.appendChild(createImg);
            undoFunc.appendChild(createAtag);

            
            const div = document.createElement('div');
            div.setAttribute('id', 'imgsbuttons-id');
            div.setAttribute('class', 'imgsbuttons-cls');

           
            const rotateButton = document.createElement('button');
            rotateButton.setAttribute('type', 'button');
            rotateButton.setAttribute('class', 'btn btn-light funbtns dropdown-toggle');
            rotateButton.setAttribute('id', 'rotateimg');
            rotateButton.setAttribute('data-bs-toggle', 'dropdown');

            const rotateIcon = document.createElement('i');
            rotateIcon.setAttribute('class', 'fa fa-sync fa-solid');
            rotateButton.appendChild(rotateIcon);
            rotateButton.appendChild(document.createTextNode(' Rotate '));

            const ul = document.createElement('ul');
            ul.setAttribute('class', 'dropdown-menu');

            const rotationAngles = [45, 90, 180, 270, 360];
            rotationAngles.forEach(angle => {
                const li = document.createElement('li');
                const a = document.createElement('a');
                a.setAttribute('class', 'dropdown-item');
                a.setAttribute('id', 'dropdownitem');
                a.setAttribute('data-rotate', angle);
                a.setAttribute('data-src', ImgSrc);  
                a.appendChild(document.createTextNode(`${angle} Deg`));
                li.appendChild(a);
                ul.appendChild(li);
            });

            div.appendChild(rotateButton);
            div.appendChild(ul);

            
            const deleteButton = document.createElement('button');
            deleteButton.setAttribute('type', 'submit');
            deleteButton.setAttribute('class', 'btn btn-light funbtns softdelete-btn');
            deleteButton.setAttribute('id', 'removebtn');
            deleteButton.setAttribute('data-src', ImgSrc);

            const deleteIcon = document.createElement('i');
            deleteIcon.setAttribute('class', 'fa fa-trash');
            deleteButton.appendChild(deleteIcon);
            deleteButton.appendChild(document.createTextNode(' Delete '));

            div.appendChild(deleteButton);
            undoFunc.appendChild(div);

        }
    }



    if (event.target.classList.contains('harddelete-btn')) {
        let ImgSrc = event.target.getAttribute('data-src');
        let hardRemove = document.querySelector(`[data-src="${ImgSrc}"]`);
        event.preventDefault();
        
        
        const csrfToken = document.cookie.split(';');
        let csrfTokenValue = '';
        csrfToken.forEach(cookie => {
            let [name, value] = cookie.trim().split('=');
            if (name =='csrftoken'){
            csrfTokenValue = value;}
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
               hardRemove.remove()
            }
        } catch (err) {
            
            console.log("Error removing image:", err);
        }

    }
})



        
document.addEventListener('DOMContentLoaded', async function () {
    let sortedList = [];
    
    new Sortable(document.getElementById("imgorder"), {
        animation: 150,
        ghostClass: "dragging",
        onEnd: async function (evt) {

            sortedList = Array.from(evt.from.children).map(item => item.dataset.src);
            const csrfToken = document.cookie.split(';');

            let csrfTokenValue = '';
            csrfToken.forEach(cookie =>{
            let [name , value ] =cookie.trim().split('=');
            if (name =='csrftoken'){
                csrfTokenValue = value;}});
            
            const dataToSendServer = {imageorder : sortedList,};


            let response = await fetch(`${window.location.protocol}//${window.location.host}/reorder/` , {
                method:'POST',
                headers :{'content-type':'application/json' , 'X-CSRFToken':csrfTokenValue},
                body : JSON.stringify(dataToSendServer),});
                    

            let result = await response.json();
                if (result.status == 200){
                    console.log(result.data)};

            console.log('sorted Order ' , sortedList)}});

})    








document.addEventListener('DOMContentLoaded', async function() {
    let formCalling = document.getElementById('reordersaveing'); 

    formCalling.addEventListener('submit', async function(event) {
        event.preventDefault();
        let downloadBtn = document.getElementById('saveandoutput');
        downloadBtn.disabled = true;
        downloadBtn.textContent = 'Downloading...';
       
        formCalling.submit(); 
        
    });
});








