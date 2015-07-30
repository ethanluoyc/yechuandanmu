CHECK = true;

var socket = io.connect('//' + document.domain + ':' + location.port + '/check');

socket.on('connect', function() {
    console.log('check connected');
});

socket.on('check danmu', function(msg){
    console.log(msg);
    if (CHECK){
        $('#msg-queue tr:last').after('<tr><td>'+ msg.data+'</td></tr>');
    }
    else{
        console.log(msg);
        socket.emit('approve danmu', {data: msg.data});
        // io.of('/post').emit('post danmu', {data: msg.data});
}});

$(document).ready(function(){
    $(document).bind('keydown', 'left', function() {
                $('#msg-queue tr:first').remove();
            });

    $(document).bind('keydown', 'right', function() {
        msg = $('#msg-queue tr:first').text();
        console.log('Sent: ' + msg.data);
        socket.emit('approve danmu', {data: msg.data});
        $('#msg-queue tr:first').remove();
    });
});
