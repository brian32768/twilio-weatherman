#
#  Here are the routes (that is, the URL's) that this app supports.
#
from flask import render_template, request
from twilio.twiml.voice_response import VoiceResponse
from twilio.twiml.messaging_response import MessagingResponse
from app.helpers import twiml
from app import app
from app import nws

@app.route('/home/')
def home():
    print("Accessing home page, which really does nothing at all.")
    return render_template('home.html')

# curl http://127.0.0.1:5000/messaging --data-urlencode "to=+17078279200" --data-urlencode "from=+17078270003" --data-urlencode "body=The weather outside is lovely!"

def get_forecast(lat,lon):
    """ Get the forecast from NWS """
    forecast = ""
    try:
        n = nws.nws(lat,lon)
        n.parse()
        forecast = n.detailedForecast
    except Exception as e:
        forecast = "Forecast not available, " + e

    print('msg=',forecast)
    return forecast

@app.route('/messaging/', methods=['POST'])
def messaging():
    print("We received an SMS message. Sending a reply")
    response = MessagingResponse()

    # Development, dump out the POST so we can see what add-ons are doing
    for k in request.form:
        print("'%s':'%s'" % (k,request.form[k]))

    # Get location from the response, geocode? callerid?

    # Sanity check on the location goes here
    lat = 38.352
    lon = -122.692
    forecast = get_forecast(lat,lon)

    try:
        rval = response.message(forecast,
                                to   = request.form['From'],
                                from_ = request.form['To'] # Replying so remember to flip From and To!
                                )
    except Exception as e:
        print("Exception building response:", e)

    return twiml(response)

@app.route('/voice/', methods=['POST'])
def voice():
    print("We received a voice call. Say something")
    response = VoiceResponse()

    # Development, dump out the POST so we can see what add-ons are doing
    for k in request.form:
        print("'%s':'%s'" % (k,request.form[k]))

    try:
        city = "Forecast for " + request.form["CallerCity"] + '. '
    except KeyError:
        city = "Forecast: "
    
    try:
        zip = request.form["CallerZip"]
    except KeyError:
        zip = ''
    print("Caller zip = ", zip)
    
    # Sanity check on the location goes here
    lat = 38.352
    lon = -122.692
    forecast = get_forecast(lat,lon)

    try:
        rval = response.say(city + forecast)
    except Exception as e:
        print("Exception building response:", e)
    return twiml(response)

@app.route('/status/', methods=['POST'])
def status_update():
    response = None

    # Development, dump out the POST so we can see what add-ons are doing
    print("------------------- STATUS ------------------ ")
    for k in request.form:
        print("'%s':'%s'" % (k,request.form[k]))
    print("------------------- ------ ------------------ ")

    return twiml(response)

# That's all!
