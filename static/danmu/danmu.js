$(document).ready(function() {

    var danmuss = {
        1: [{
            "text": "哈哈哈",
            "color": "red",
            "size": "0",
            "position": "0"
        }, {
            "text": "233333",
            "color": "red",
            "size": "0",
            "position": "0"
        }],
        3: [{
            "text": "poi",
            "color": "red",
            "size": "1",
            "position": "0"
        }, {
            "text": "2333",
            "color": "#FFFFFF",
            "size": "0",
            "position": "0"
        }],
        10: [{
            "text": "XXX真好",
            "color": "#FFFFFF",
            "size": "0",
            "position": "2"
        }]
    };
    // settings for the Danmu Player
    var options = {
        left: 0,
        top: 0,
        height: screen.height,
        width: screen.width,
        zindex: 100,
        speed: 20000,
        sumtime: 900,
        danmuss: danmuss,
        default_font_color: "#FFFFFF",
        font_size_small: 50,
        font_size_big: 70,
        opacity: 1.0,
        top_botton_danmu_time: 6000
    };

    function _randomChoice(arr) {
        return arr[Math.floor(arr.length * Math.random())];
    }

    //initialize danmu player
    $("#danmu").danmu(options);

    var danmuPlayer = $('#danmu'); // a selector for the danmu div

    function show_danmu(danmuPlayer, msg) {
        var heig = danmuPlayer.height();
        var row_conut = parseInt(heig / options.font_size_big);
        var row = parseInt(row_conut * Math.random());
        var top_local = (row) * options.font_size_big;

        var a_danmu = "<div class='flying flying2' id='linshi'></div>";
        danmuPlayer.append(a_danmu);
        fly_tmp_name = "fly" + parseInt(heig * Math.random()).toString();

        $("#linshi").attr("id", fly_tmp_name);
        $("#" + fly_tmp_name).text(msg);
        $("#" + fly_tmp_name).css({
            "position": "absolute",
            "top": top_local,
            "left": options.width,
            "font-size": _randomChoice([50, 60, 70]),
            "white-space": "nowrap",
            "color": "white",
            "opacity": 1.0
            }
        );
        $("#" + fly_tmp_name).animate({left: -danmuPlayer.width() * 3},
        options.speed, function() {$(this).remove();});
    }

    namespace = '/post';

    // the socket.io documentation recommends sending an explicit package upon connection
    var socket = io.connect('//' + document.domain + ':' + location.port + namespace);

    socket.on('connect', function() {
        console.log('connected');
    });

    socket.on('disconnect', function() {
        console.log('disconnected');
    });

    // receive and display danmu
    socket.on('post danmu', function(msg) {
        console.log('received: '+ msg);
        // $('#board').append('<br>Received #' + msg.data);
        show_danmu(danmuPlayer, msg.data);
    });
});
