from flask_script import Manager

from danmu import app, socketio

manager = Manager(app)

@manager.command
def run():
    socketio.run(app)


if __name__ == "__main__":
    manager.run()
