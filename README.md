#叶串弹幕
A Flask app using Socket.IO to display live Danmaku. We used it with <3 for 叶串2015!

It uses [Flask-Sockets](https://github.com/kennethreitz/flask-sockets) for interface with Websocket protocol. Notice that this extension is not compatible with the latest version of socket.io.

Without Jimmy's last-minute help, this project may not be possible.

The actual app is implemented on Heroku. Notice that you need to use Gevent. I also used Gunicorn as the WSGI server.

