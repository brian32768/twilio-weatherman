# Import flask and template operators
from flask import Flask, render_template

# Import SQLAlchemy, see http://pythonhosted.org/Flask-SQLAlchemy/
#from flask.ext.sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)

# Load configurations
app.config.from_object('config')

# Define the database object which is imported by modules and controllers
# The database is defined in the app config file. For testing we use sqlite.
db = SQLAlchemy(app)

########################################################################
# HTTP error handlers

@app.errorhandler(403)
def forbidden_403(exception):
    return render_template('403.html'), 403

@app.errorhandler(404)
def not_found_404(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error_500(error):
    db.session.rollback()
    return render_template('500.html'), 500

########################################################################

from . import controllers

# Import a module / component using its blueprint handler variable (mod_auth)
from app.mod_auth.controllers import mod_auth as auth_module

# Register blueprint(s)
app.register_blueprint(auth_module)
# app.register_blueprint(xyz_module)
# ..

# That's all!
