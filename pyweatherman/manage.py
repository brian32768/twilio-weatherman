#
#   To start the service:
#     python manage.py runserver
#
from app import app
from flask_script import Manager, Server

manager = Manager(app)

@manager.command
def test():
    """Run unit tests."""
    pass

if __name__ == '__main__':

    # override localhost
    server = Server(host="0.0.0.0", port=5000)
    manager.add_command("runserver",server)

    manager.run()
