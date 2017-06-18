# Keep only non-secret things here.
#
# Secret parts of the configuration need to come from the environment
# so they don't leak into a source repository.#
#

import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

#SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/users.sqlite3'
#DATABASE_CONNECT_OPTIONS = {}

# How many cores do we have?
# Assume one thread for web requests and one for background tasks
THREADS_PER_PAGE = 2

# Protection against cross-site scripting
CSRF_ENABLED     = True
CSRF_SESSION_KEY = "mysecretsaresafehere"

# Cookie stuff
PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
REMEMBER_COOKIE_DURATION = timedelta(days=30)
SECRET_KEY = 'foobarbaz'
