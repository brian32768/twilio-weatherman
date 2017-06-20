from flask import Flask
import os
application = Flask(__name__)

@application.route("/hello")
def root():
    return "Hello, world!"

if __name__ == "__main__":
    application.run()
