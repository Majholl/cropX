document.addEventListener('DOMContentLoaded', function() {
    const el = document.querySelector('#imform')
    const inputFiled = document.getElementById('inputGroupFile01');
    if (el){

    el.addEventListener('submit' , function(event){
            event.preventDefault()
            if (inputFiled.files.length > 0){
                document.getElementById('submitbtn').remove();
                document.getElementById('loadingmsg').style.display = 'block'
                el.submit()
            }else{
                alert('Nothing selected')}
            })

    }
   
});


