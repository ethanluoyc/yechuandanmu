# 叶串弹幕

A Flask app using Socket.IO to display live Danmaku. We used it with <3 for 叶串2015!

It uses [Flask-Sockets](https://github.com/kennethreitz/flask-sockets) for interface with Websocket protocol. Notice that this extension is not compatible with the latest version of socket.io.

The actual app runs on Heroku. Notice that you need to use Eventlet. I also used Gunicorn as the WSGI server.

NOTE: We also have a companion app https://github.com/wxhemiao/yechuandanmu-client

Brought to you by NJC CLDDS, proud to be an NJCian!

国初华会, 薪火相传.

## CHANGELOG
29 July 2016
- Deployed for Yechuan 2016 (千面佛). Many thanks to [JoeyTeng](https://github.com/JoeyTeng)
who helped with this year's upgrade and testing.

06 July 2016

- The site now has a PostgresSQL backend to track all the Danmus exchanged during hosting.
- Refactored the code to be better organized
- Updated the auditing page to use React for UI.
- Upgraded Flask-SocketIO version.

31 July 2015
- First iteration made by Yicheng Luo with help from [Jimmy He](https://github.com/wxhemiao), a great success during Yechuan 2015!


## LICENSE
MIT
