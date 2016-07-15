#!/usr/bin/env python

from flask_script import Manager, Shell, prompt_bool
from danmu import FeatureFlag, Danmaku, initdb, db
from danmu import app


def _make_context():
    return dict(app=app, db=db, FeatureFlag=FeatureFlag, Danmaku=Danmaku)

manager = Manager(app, with_default_commands=False)


@manager.option('-s', '--status', dest='status', default=None)
def supervise(status):
    if not status:
        status = 'on' if FeatureFlag.toggle_flag('supervise') else 'off'
    else:
        if status == 'on':
            f = True
        elif status == 'off':
            f = False
        status = FeatureFlag.toggle_flag('supervise', f)
    print('Supervise is now turned {0}'.format(status))


@manager.command
def dropdb():
    if prompt_bool(
        "Are you sure you want to lose all your data"):
        db.drop_all()


@manager.command
def createdb():
    initdb()

@manager.command
def run():
    from danmu import socketio
    socketio.run(app)

manager.add_command('shell', Shell(make_context=_make_context))

if __name__ == "__main__":
    manager.run()
