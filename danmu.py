# -*- coding: utf-8 -*-
import os
from flask import Flask, render_template, request, flash, jsonify
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
import config


def create_app(cfg=None):
    app = Flask(__name__)
    if not cfg:
        cfg = config.ProdConfig if os.environ.get('DANMU_SERVER_ENV') == 'prod' \
    else config.DevConfig
    app.config.from_object(cfg)
    return app

app = create_app()
db = SQLAlchemy(app)
socketio = SocketIO(app)

STATUS_FLAGS = {
    'waiting': 0,
    'approved': 1,
    'disproved': 2
}


def initdb():
    db.create_all()
    db.session.commit()

    def add_supervise_flag():
        flag = FeatureFlag.get_flag('supervise')
        if not flag:
            flag = FeatureFlag('supervise')
            db.session.add(flag)
            db.session.commit()

    add_supervise_flag()


class Danmaku(db.Model):
    MAX_LENGTH = 80
    id = db.Column(db.Integer, primary_key=True)
    msg = db.Column(db.String(80))
    status = db.Column(db.Integer, nullable=False)

    def __init__(self, msg, **kwargs):
        self.msg = msg
        self.status = STATUS_FLAGS['waiting']
        super(Danmaku, self).__init__(**kwargs)

    def to_dict(self):
        return dict(id=self.id, data=self.msg, status=self.status)

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)

    def validate(self):
        if not self.msg:
            raise DanmakuNonEmpty('Danmaku cannot be empty')
        if len(self.msg) > Danmaku.MAX_LENGTH:
            raise DanmakuTooLong('Danmaku exceeds max length ({0})'
                                 .format(Danmaku.MAX_LENGTH))

    def save(self):
        db.session.add(self)
        return db.session.commit()


class DanmakuValidateException(Exception):
    """Base class for Validation exception for danmaku"""


class DanmakuTooLong(DanmakuValidateException):
    "raised when Danmaku is too long"


class DanmakuNonEmpty(DanmakuValidateException):
    "raised when Danmaku is either None or empty (aka '')"


class SUPERVISE_STATUS:
    ENABLED = True
    DISABLED = False


class FeatureFlag(db.Model):
    name = db.Column(db.String(80), primary_key=True)
    status = db.Column(db.Boolean)

    def __init__(self, name, status=STATUS_FLAGS['waiting']):
        self.name = name
        self.status = True # Default to true

    @classmethod
    def get_flag(cls, name):
        return cls.query.get(name)

    @classmethod
    def toggle_flag(cls, name, status=None):
        flag = cls.get_flag(name)
        if not status:
            if flag.status:
                flag.status = False
            else:
                flag.status = True
        else:
            flag.status = bool(status)
        db.session.commit()
        return flag.status

    def save(self):
        db.session.add(self)
        return db.session.commit()



# Below are routes for the application

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/post', methods=['GET', 'POST'])
def post_message():
    def _is_ajax():
        return request\
            .headers.get('X-Requested-With', None) == 'XMLHttpRequest'

    def _respond_with_exn(exn):
        err_message = exn.message
        if request.headers.get('X-Requested-With', None) == 'XMLHttpRequest':
            return jsonify({'status': 1,
                            'messages': [{'body': err_message,
                                          'category': 'danger'}]}), 400
        flash(err_message, 'danger')
        return render_template('post_form.html')

    if request.method == 'GET':
        return render_template('post_form.html')

    # Handle `POST`
    try:
        msg = request.form['message']
        danmaku = Danmaku(msg)
        supervise_flag = FeatureFlag.get_flag('supervise')
        danmaku.validate()
        danmaku.save()

        if ('master' in request.form) or (not supervise_flag.status):
            danmaku.status = STATUS_FLAGS['approved']
            danmaku.save()
            socketio.emit('post danmu', danmaku.to_dict(), namespace='/post')
        else:
            socketio.emit('check danmu', danmaku.to_dict(), namespace='/check')

    except (DanmakuTooLong, DanmakuNonEmpty), e:
        return _respond_with_exn(e)
    else:
        if request.headers.get('X-Requested-With', None) == 'XMLHttpRequest':
            return jsonify({'status': 0,
                            'messages': [{'body': 'Post succeeded :)',
                                          'category': 'success'}]}), 200
        flash(u'Post succeeded :)', 'success')
        return render_template('post_form.html')


@app.route('/check', methods=['GET'])
def check_danmu():
    return render_template('check.html')


@socketio.on('approve danmu', namespace='/check')
def approve_danmu(msg):
    app.logger.debug(msg)
    if 'data' in msg:
        d = Danmaku.get_by_id(msg['id'])
        d.status = STATUS_FLAGS['approved']
        db.session.commit()
        socketio.emit('post danmu', {'data': msg['data']}, namespace='/post')


@socketio.on('disprove danmu', namespace='/check')
def disprove_danmu(msg):
    app.logger.debug(msg)
    if 'data' in msg:
        d = Danmaku.get_by_id(msg['id'])
        d.status = STATUS_FLAGS['disproved']
        db.session.commit()


@socketio.on('connect', namespace='/post')
def board_connect():
    app.logger.debug('Board posting connected')


@socketio.on('disconnect', namespace='/post')
def board_disconnect():
    app.logger.debug('Board posting disconnected')


@socketio.on('connect', namespace='/check')
def check_connect():
    app.logger.debug('Checking connected')


@socketio.on('disconnect', namespace='/check')
def check_disconnect():
    app.logger.debug('Checking disconnected')


if __name__ == '__main__':
    socketio.run(app)
