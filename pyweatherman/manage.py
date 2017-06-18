#
#  python manage.py cleardb
#  python manage.py initdb

from flask.ext.script import Manager

from login import app
from login.model import init_db, clear_db

manager = Manager(app)


@manager.command
def initdb():
    """Initialize database."""
    with app.app_context():
        init_db()


@manager.command
def cleardb():
    """Clear database."""
    with app.app_context():
        clear_db()


if __name__ == '__main__':
    manager.run()
