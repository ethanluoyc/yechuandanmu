const logo =[
" __  __          __                         ____                             ",
" \\ \\/ /__  _____/ /_  __  ______ _____     / __ \\____ _____  ____ ___  __  __",
"  \\  / _ \\/ ___/ __ \\/ / / / __ `/ __ \\   / / / / __ `/ __ \\/ __ `__ \\/ / / /",
"  / /  __/ /__/ / / / /_/ / /_/ / / / /  / /_/ / /_/ / / / / / / / / / /_/ / ",
" /_/\\___/\\___/_/ /_/\\__,_/\\__,_/_/ /_/  /_____/\\__,_/_/ /_/_/ /_/ /_/\\__,_/  ",
" Use the following keys to control this page: ",
" `d` to show and hide the Danmaku page;",
" `j` and `k` to make the opacity higher/lower;",
" `n` to toggle the display of the TinyURL;",
" made with <3 by Yicheng Luo and contributors."].join("\n");


$(document).ready(function() {
  console.log(logo);

  var danmuss = {};
  // Settings for the Danmu Player!
  var options = {
    left: 0,
    top: 0,
    height: screen.height,
    width: screen.width,
    zindex: 100,
    speed: 20000,
    sumtime: 900,
    danmuss: danmuss,
    default_font_color: '#FFFFFF',
    font_size_small: 50,
    font_size_big: 70,
    opacity: 1.0,
    top_botton_danmu_time: 6000
  };

  function _randomChoice(arr) {
    return arr[Math.floor(arr.length * Math.random())];
  }

  //initialize danmu player
  $('#danmu').danmu(options);

  // a selector for the danmu div
  var danmuPlayer = $('#danmu');

  var row_number = 0;
  var row_number_max = 7; //7 is the magic number of row_count below in my browser
  var danmu_count = 0;

  function show_danmu(danmuPlayer, msg) {
    //console.log(msg);
    clearTimeout(reset_row_number);
    var reset_row_number = setTimeout("row_number = 0", options.speed); // Reset to top after some time
    row_number += 1;
    if (row_number > row_number_max) {
      row_number = 0
    }
    var heig = danmuPlayer.height() / 1.5;
    var row_conut = parseInt(heig / options.font_size_big);
    var vertical_layer = 1.0 * row_number / row_number_max; // Math.random()
    var row = parseInt(row_conut * vertical_layer);
    var top_local = (row) * options.font_size_big;

    var a_danmu = '<div class=\'flying flying2\' id=\'linshi\'></div>';
    danmuPlayer.append(a_danmu);
    var fly_tmp_name = 'fly' + danmu_count.toString(); // parseInt(heig * Math.random()).toString();
    danmu_count += 1; // Give distinct identity

    $('#linshi').attr('id', fly_tmp_name);
    $('#' + fly_tmp_name).text(msg);
    $('#' + fly_tmp_name).css({
      'position': 'absolute',
      'top': top_local,
      'left': options.width,
      'font-size': _randomChoice([50, 60, 70]),
      'white-space': 'nowrap',
      'color': 'white',
      'opacity': 1.0
    });
    $('#' + fly_tmp_name).animate({
      left: -danmuPlayer.width() * 3
    },
      options.speed,
      function() {
        $(this).remove();
      });
  }

  var namespace = '/post';

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
    console.log('received: ' + msg.data);
    show_danmu(danmuPlayer, msg.data);
  });
});


// Bind keyboard shortcuts
$(document).ready(function() {
  $(document).bind('keydown', 'd', function() {
    if ($('#danmuholder').css("display") == 'none') {
      $('#danmuholder').fadeIn("slow", function() {
        $("#board-logo").fadeIn("slow", function() {
          $(".url-footer").fadeIn("slow");
        });
      });
    } else {
      $("#board-logo").fadeOut("slow", function() {
        $('#danmuholder').fadeOut("slow");
      });
      $(".url-footer").fadeOut("slow");

    }

  });

  $(document).bind('keydown', 'q', function() {
    $("#qrcode").fadeToggle("slow");
  });

  $(document).bind('keydown', 'n', function() {
    $(".url-footer").fadeToggle("slow");
  });
  // Toggle opacity of the Danmuplayer, use animate rather than fade to avoid texts from inner divs from being affected by the changes in opacity
  $(document).bind('keypress', 'j', function() {
    console.log('pressed');
    $("#danmu").animate({
      backgroundColor: "rgba(0,0,0,1)"
    }, 600);
  });

  $(document).bind('keypress', 'k', function() {
    console.log("pressed");
    $("#danmu").animate({
      backgroundColor: "rgba(0,0,0,0.7)"
    }, 600);
  });

});
