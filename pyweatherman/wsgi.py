#
#  This is invoked from nginx config to launch this app.
#
from app import app
if __name__ == "__main__":
    app.run()
