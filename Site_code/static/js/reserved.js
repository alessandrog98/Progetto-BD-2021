console.log("caricato")

$(document).ready(function(){
    $(".table").on('click', 'tr', function (e) {
        e.preventDefault();
        var id = $(this).attr('value');
        window.location.href = 'http://127.0.0.1:5000/survey/'+id+'/summary_questions/'
    })
})


