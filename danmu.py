# -*- coding: utf-8 -*-
import os
from flask import Flask, render_template, request, flash, jsonify
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

import config

CONFIG = config.ProdConfig if os.environ.get('DANMU_SERVER_ENV') == 'prod' \
    else config.DevConfig
app = Flask(__name__)
app.config.from_object(CONFIG)

db = SQLAlchemy(app)
socketio = SocketIO(app)

STATUS_FLAGS = {
    'waiting': 0,
    'approved': 1,
    'disproved': 2
}


class Danmaku(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    msg = db.Column(db.String(80))
    status = db.Column(db.Integer, nullable=False)

    def __init__(self, msg):
        self.msg = msg
        self.status = STATUS_FLAGS['waiting']

    def to_dict(self):
        return dict(id=self.id, data=self.msg, status=self.status)

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)

db.create_all()
db.session.commit()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/post', methods=['GET', 'POST'])
def post_message():

    def mk_danmaku(msg):
        d = Danmaku(msg)
        db.session.add(d)
        db.session.commit()
        return d

    if request.method == 'POST':
        msg = request.form['message']
        if msg:
            if len(msg) <= 80:
                danmaku = mk_danmaku(msg)
                if "master" in request.form:
                    socketio.emit('post danmu',
                                  danmaku.to_dict(),
                                  namespace='/post')
                    return 0, 200
                socketio.emit('check danmu',
                              danmaku.to_dict(),
                              namespace='/check')
                if request.headers['X-Requested-With'] == 'XMLHttpRequest':
                    return jsonify({'status': 0,
                                    'messages': [{'body': 'Post succeeded :)',
                                                  'category': 'success'}]}), 200
                flash(u'Post succeeded :)', 'success')
            else:
                if request.headers['X-Requested-With'] == 'XMLHttpRequest':
                    return jsonify({'status': 1,
                                    'messages': [{'body': u'The message is too long, max length is 80', 'category': 'danger'}]})
                flash(u'The message is too long, max length is 80', 'danger')
                return render_template('post_form.html')
        return jsonify({'status': 0,
                        'messages': [{'body': 'Cannot be empty',
                                      'category': 'danger'}]}), 400

    return render_template('post_form.html')


@app.route('/check', methods=['GET'])
def check_danmu():
    return render_template('check.html')


@socketio.on('approve danmu', namespace='/check')
def approve_danmu(msg):
    app.logger.info(msg)
    if 'data' in msg:
        d = Danmaku.get_by_id(msg['id'])
        d.status = STATUS_FLAGS['approved']
        d.save()
        socketio.emit('post danmu', {'data': msg['data']}, namespace='/post')


@socketio.on('disprove danmu', namespace='/check')
def disprove_danmu(msg):
    app.logger.info(msg)
    if 'data' in msg:
        d = Danmaku.get_by_id(msg['id'])
        d.status = STATUS_FLAGS['disproved']
        d.save()


@socketio.on('connect', namespace='/post')
def post_connect():
    app.logger.info('Board posting connected')


@socketio.on('connect', namespace='/check')
def check_connect():
    app.logger.info('Checking connected')

# @socketio.on('disconnect', namespace='/post')
# def test_disconnect():
#     print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app)
