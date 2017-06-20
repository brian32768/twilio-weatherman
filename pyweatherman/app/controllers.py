#
#  Here are the routes (that is, the URL's) that this app supports.
#
from flask import render_template, request
from twilio.twiml.voice_response import VoiceResponse
from twilio.twiml.messaging_response import MessagingResponse
from app.helpers import twiml
from app import app
from app import nws
from app import geocode

@app.route('/home/')
def home():
    print("Accessing home page, which really does nothing at all.")
    return render_template('home.html')

def get_forecast(latlon):
    """ Get the forecast from NWS """
    forecast = ""
    try:
        n = nws.nws()
        n.fetch(latlon)
        n.parse()
        forecast = n.detailedForecast
    except Exception as e:
        forecast = "not available, " + e

    return forecast

@app.route('/messaging/', methods=['POST'])
def messaging():
    print("------------ SMS MESSAGE RECEIVED ---------- ")
    
    response = MessagingResponse()

    # For development, dump out the POST so we can see what is sent to us.
    # This is especially useful for testing add-ons.
    #for k in request.form: print("'%s':'%s'" % (k,request.form[k]))

    # Sending a ZIP as the message overrides caller id zip.
    locality = None
    zip = None
    body = None
    try:
        body = request.form["Body"].strip()
        print("TXT='%s'" % body)

        if len(body)==5 and body.isdigit():
            zip = body
    except Exception as e:
        print("Could not read body.", e)

    if not zip:
        # No zip in message body so try caller id zip and locality
        try:
            zip = request.form["FromZip"]
            print("Caller zip = ", zip)
        except KeyError:
            print("Zip is not available.")
        try:
            locality = request.form["FromCity"]
        except KeyError:
            locality = None
            print("City is not available.")

    if not zip:
        forecast = "Could not determine location, sorry. Forecast not available."

    else:
        place = geocode.geocode()
        place.fetch(zip)
        place.parse()
        latlon = place.latlon  
        if not locality:
            locality = place.locality
    
        # Sanity check on the location goes here
        preamble = "Forecast: "
        if locality:
            print("You are near %s." % locality)
            preamble = "Forecast for %s: " % locality
        print('Geocoded location for %s is %s' % (zip,latlon))

        #latlon = (38.352, -122.692) # Cotati
        forecast = preamble + get_forecast(latlon)

    print("Replying: '%s'" % forecast)
    try:
        # We're replying so remember to flip From and To!
        rval = response.message(forecast, to = request.form['From'], from_ = request.form['To'])
        # rval contains XML that will be sent
    except Exception as e:
        print("Exception sending reply:", e)

    return twiml(response)

@app.route('/voice/', methods=['POST'])
def voice():
    print("------------ VOICE CALL RECEIVED ---------- ")
    response = VoiceResponse()

    # For development, dump out the POST so we can see what is sent to us.
    # This is especially useful for testing add-ons.
    #for k in request.form: print("'%s':'%s'" % (k,request.form[k]))

    try:
        city = "Forecast for " + request.form["CallerCity"] + ': '
    except KeyError:
        city = "Forecast: "
    
    try:
        zip = request.form["CallerZip"]
    except KeyError:
        zip = ''
    print("Caller zip = ", zip)

    # In a more perfect world, geocode and weather lookups would be
    # done asynchronously so that the caller can listen to MOH or
    # something while lookups takes place.

    if not zip:
        forecast = "Could not determine location, sorry. Forecast not available."
    else:
        place = geocode.geocode()
        place.fetch(zip)
        place.parse()
        latlon = place.latlon

        # Sanity check on the location goes here
        print("Geocoded location for %s is %s." % (zip,latlon))

        #latlon = (38.352, -122.692) # Cotati
        forecast = city + get_forecast(latlon)
    
    print("Saying '%s'" % forecast)
    try:
        rval = response.say(forecast)
        # rval contains XML that will be sent
    except Exception as e:
        print("Exception in response :", e)
        
    return twiml(response)

@app.route('/status/', methods=['POST'])
def status_update():
    print("--------------- STATUS : %s -------------- " % request.form["CallStatus"])
    # Development, dump out the POST so we can see what add-ons are doing
#    for k in request.form:
#        print("'%s':'%s'" % (k,request.form[k]))
#    print("------------------- ------ ------------------ ")
    response = None
    return twiml(response)

# That's all!
