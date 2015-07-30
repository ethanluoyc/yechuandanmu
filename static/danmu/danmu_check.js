CHECK = true;

var socket = io.connect('//' + document.domain + ':' + location.port + '/check');

socket.on('connect', function() {
    console.log('check connected');
});

socket.on('check danmu', function(msg){
    console.log(msg);
    if (CHECK){
        $('#msg-queue').append('<tr><td>'+ msg.data+'</td></tr>');
    }
    else{
        console.log(msg);
        socket.emit('approve danmu', {data: msg.data});
}});

$(document).ready(function(){
    $(document).bind('keydown', 'left', function() {
                $('#msg-queue tr:first').remove();
            });

    $(document).bind('keydown', 'right', function() {
        var msg = $('#msg-queue tr:first').text();
        if (msg.length != 0) {
            console.log('Sent: ' + msg);
            socket.emit('approve danmu', {data: msg});
            $('#msg-queue tr:first').remove();
        }else{
            console.log('Empty Queue!');
        }
    });
});
