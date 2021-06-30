console.log("caricato")

$(document).ready(function(){
    $(".table").on('click', 'tr', function (e) {
        e.preventDefault();
        var id = $(this).attr('value');
        document.location.href = '/survey/' + id
    })
})


