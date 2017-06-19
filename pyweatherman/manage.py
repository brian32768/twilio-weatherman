#
#   To start the service:
#     python manage.py runserver
#
from app import app
from flask_script import Manager
manager = Manager(app)

@manager.command
def test():
    """Run unit tests."""
    pass

if __name__ == '__main__':
    manager.add_command("runserver",server)
    manager.run()
