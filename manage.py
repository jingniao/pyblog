#!/usr/bin/env python

# from app import create_app, db
# from app.models import User, Role
from blog import app, db
from blog.models import User, Article
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
# app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Article=Article)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
if __name__ == '__main__':
    manager.run()
