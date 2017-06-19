#
#  This is the code we need to run pyweatherman as a wsgi app from nginx
#  instead of standalone (python manage.py runserver)
#
from app import app
if __name__ == "__main__":
    app.run()
