#! /usr/bin/env python
import os

from flask.ext.script import Manager, Shell, Command
from flask.ext.migrate import Migrate, MigrateCommand

from flaskfilled import create_app, db
from flaskfilled.models import Cookie

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db)


class DBInit(Command):
    '''Creates database tables from sqlalchemy models'''

    def __init__(self, db):
        self.db = db

    def run(self):
        self.db.create_all()


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db_init', DBInit(db))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
