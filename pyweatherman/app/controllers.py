#
#  Here are the routes (that is, the URL's) that this app supports.
#
from flask import render_template, request
from twilio.twiml.voice_response import VoiceResponse
from twilio.twiml.messaging_response import MessagingResponse
from app.helpers import twiml
from app import app
from . import nws

@app.route('/home/')
def home():
    print("Accessing home page, which really does nothing at all.")
    return render_template('home.html')

# curl http://127.0.0.1:5000/messaging --data-urlencode "to=+17078279200" --data-urlencode "from=+17078270003" --data-urlencode "body=The weather outside is lovely!"
    
@app.route('/messaging/', methods=['POST'])
def messaging():
    print("We received an SMS message. Send a reply")
    response = MessagingResponse()

    # Get location from the response, geocode?

    # Cotati
    lat = 38.352
    lon = -122.692

    # Sanity check on the location goes here

    # Get the forecast from NWS
    forecast = ""
    try:
        nws = nws(lat,lon) 
        forecast = nws.detailedForecast
    except Exception as e:
        forecast = "Forecast not available, " + e

    try:
        rval = response.message(forecast,
            to    = request.form['From'], from_ = request.form['To']) # Replying so remember to flip From and To!
        print('msg=',rval)
    except Exception as e:
        print("Exception building response to sms:", e)
        for k in request.form:
           print("  '%s':'%s'" % (k,request.form[k]))
    return twiml(response)

@app.route('/voice/', methods=['POST'])
def voice():
    print("We received a voice call. Say something")
    response = VoiceResponse()
#    response.message(say="Sunny. High near 99, with temperatures falling to around 95 in the afternoon. West southwest wind 9 to 14 mph, with gusts as high as 18 mph.")
    return twiml(response)

@app.route('/status/', methods=['POST'])
def status_update():
    print("We received a status update indicating call progress or some such thing.")
    response = None
    return twiml(response)

# That's all!
