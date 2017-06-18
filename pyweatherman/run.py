#
#  Python web application that will respond to requests from Twilio.
#  Run it to test... python run.py
#
from app import app

if __name__ == '__main__':
    app.debug = True

    print "Current app configuration:"
    for i in app.config:
        print '   ', i, ':', app.config[i]
    print ""
    print "URL map:"
    print app.url_map

    app.run()
