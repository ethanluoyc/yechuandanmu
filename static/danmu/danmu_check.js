CHECK = true;

var check_io = io.connect('//' + document.domain + ':' + location.port + '/check');

var post_io = io.connect('//' + document.domain + ':' + location.port + '/post');

post_io.on('connect', function() {
    console.log('post connected');
});

check_io.on('connect', function() {
    console.log('check connected');
});

check_io.on('check danmu', function(msg){
    console.log(msg);
    if (CHECK){$('#msg-queue tr:first').before('<tr><td>'+ msg.data+'</td></tr>');}
    else{
        console.log(msg);
        check_io.emit('approve danmu', {data: msg.data});
    }

});

//check_io.on('remove approval', function(msg){
//    $('#msg-queue tr:first').remove();
//});


$(document).ready(function(){
    $(document).bind('keydown', 'left', function() {

                $('#msg-queue tr:first').remove();
            });

    $(document).bind('keydown', 'right', function() {
                msg = $('#msg-queue tr:first').text();
                console.log(msg);
                check_io.emit('approve danmu', {data: msg});
                $('#msg-queue tr:first').remove();
            });
});