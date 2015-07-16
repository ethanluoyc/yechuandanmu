#coding=utf-8

from flask import Flask, render_template, request, flash
from flask.ext.socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cldds_safeword'
app.config['DEBUG'] = True
socketio = SocketIO(app)

class DanMu(object):
    def __init__(text, color, size, time, isnew=False):
        pass

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/post', methods=['GET', 'POST'])
def post_message():
    if request.method == 'POST':
        msg = request.form['message'].encode('utf8')
        if msg:
            if len(msg) > 20:
                flash(u'The message is too long', 'danger')
                return render_template('post_form.html')
            socketio.emit('post danmu', {'data': msg}, namespace='/test')
            flash(u'提交成功:)','success')
    return render_template('post_form.html')

@socketio.on('connect', namespace='/test')
def test_connect():
    print ('Client connected')

#
# @socketio.on('disconnect', namespace='/test')
# def test_disconnect():
#     print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app)
