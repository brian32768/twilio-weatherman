# Import flask and template operators
from flask import Flask, render_template

# Define the WSGI application object
app = Flask(__name__)

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
#    db.session.rollback()
    return render_template('500.html'), 500

########################################################################

from . import controllers

# That's all!
