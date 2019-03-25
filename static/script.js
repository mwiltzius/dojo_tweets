$(document).ready(function(){
    $('#email').keyup(function(){
        var data = $('#registration').serialize()
        $.ajax({
            method: 'POST',
            url: '/email',
            data: data
        })
        .done(function(res){
            $('#emailerror').html(res)
        })
    })
})