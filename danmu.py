# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, flash
from flask.ext.socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cldds_safeword'
app.config['DEBUG'] = True
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/post', methods=['GET', 'POST'])
def post_message():
    if request.method == 'POST':
        msg = request.form['message']
        if msg:
            if len(msg) > 30:
                flash(u'The message is too long', 'danger')
                return render_template('post_form.html')
            socketio.emit('post danmu', {'data': msg}, namespace='/post')
            flash(u'Post succeeded :)', 'success')
    return render_template('post_form.html')


@socketio.on('connect', namespace='/post')
def test_connect():
    print ('Client connected')


# @socketio.on('disconnect', namespace='/post')
# def test_disconnect():
#     print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app)
