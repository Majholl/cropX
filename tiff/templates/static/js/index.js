document.addEventListener('DOMContentLoaded', function() {
    const el = document.querySelector('#imform')
    el.addEventListener('submit' , function(event){
        event.preventDefault()
        document.getElementById('submitbtn').remove();
        document.getElementById('loadingmsg').style.display = 'block'
        el.submit()
        
})});


