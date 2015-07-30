# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, flash
from flask.ext.socketio import SocketIO, emit

# import logging
#
# logging.basicConfig()

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
            if "master" in request.form:
                socketio.emit('post danmu', {'data': msg}, namespace='/post')
                return ''
            if len(msg) > 80:
                flash(u'The message is too long, max length is 20', 'danger')
                return render_template('post_form.html')
            socketio.emit('check danmu', {'data': msg}, namespace='/check')
            flash(u'Post succeeded :)', 'success')
    return render_template('post_form.html')


@app.route('/check', methods=['GET'])
def check_danmu():
    return render_template('check.html')


@socketio.on('approve danmu', namespace='/check')
def approve_danmu(msg):
    app.logger.info(msg)
    if 'data' in msg:
        socketio.emit('post danmu', {'data': msg['data']}, namespace='/post')


@socketio.on('connect', namespace='/post')
def test_connect():
    app.logger.info('Board posting connected')


@socketio.on('connect', namespace='/check')
def test_check_connect():
    app.logger.info('Checking connected')

# @socketio.on('disconnect', namespace='/post')
# def test_disconnect():
#     print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app)
