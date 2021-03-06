#
#  Here are the routes (that is, the URL's) that this app supports.
#
from __future__ import print_function
from flask import render_template, request
from twilio.twiml.voice_response import VoiceResponse
from twilio.twiml.messaging_response import MessagingResponse
from app import app
from utils.helpers import twiml,get_weather
from utils import geocode

@app.route('/weather/')
def home():
    """ Send the weather info back via browser. """
    return render_template('weather.html')

@app.route('/messaging/', methods=['POST'])
def messaging():
    sender = request.form['From']
    print("------ SMS MESSAGE RECEIVED FROM %s ------ " % sender)

    # For development, dump out the POST so we can see what is sent to us.
    # This is especially useful for testing add-ons.
    #for k in request.form: print("'%s':'%s'" % (k,request.form[k]))

    response = MessagingResponse()
    
    # Does the message body have something in it?
    # It could be a zip code or a locality (address)
    txtmsg = None
    try:
        body = request.form["Body"].strip()
        if len(body) > 1:
            print("Body='%s'" % body)
            txtmsg = body
    except Exception as e:
        print("Could not read message body.", e)

    zip = locality = None
    if txtmsg:
        if txtmsg.isdigit() and len(txtmsg)==5:
            zip = txtmsg
        else:
            locality = txtmsg
    else:
        # try caller id zip and locality
        try:
            zip = request.form["FromZip"]
        except KeyError:
            pass
        try:
            locality = request.form["FromCity"]
        except KeyError:
            locality = None
            pass

    if not zip and not locality:
        # With no input, I cannot even guess where you are! Oh!
        msg = "Could not determine location, sorry. Weather information not available."
    else:
        place = geocode.geocode()
        place.search(address=locality, postalcode=zip)

        shortmsg = "Sorry, I can't tell where you are!"
        if place.parse():
            latlon = place.latlon  
            if place.short_place:
                # This will be a better name than what I typed
                locality = place.short_place
    
            if not latlon or not latlon[0] or not latlon[1]:
                if zip:
                    shortmsg += " I tried zip code '%s'." % zip
                elif locality:
                    shortmsg += " I looked for '%s'." % locality
            else:
                print("Geocode result for %s %s = %s." % (place.locality,zip,latlon))
                (shortmsg, longmsg) = get_weather(latlon,locality)

    print("Replying: '%s'" % shortmsg)
    try:
        # We're replying so remember to flip From and To!
        rval = response.message(shortmsg, to = sender, from_ = request.form['To'])
        # rval contains XML that will be sent
    except Exception as e:
        print("Exception buiding reply:", e)

    return twiml(response)

@app.route('/voice/', methods=['POST'])
def voice():
    # For development, dump out the POST so we can see what is sent to us.
    # This is especially useful for testing add-ons.
    #for k in request.form: print("'%s':'%s'" % (k,request.form[k]))

    sender = request.form['From']
    print("----- VOICE CALL RECEIVED FROM %s ----- " % sender)

    response = VoiceResponse()

    locality = ""
    try:
        locality = request.form["CallerCity"]
    except KeyError:
        pass
    
    zip = ''
    try:
        zip = request.form["CallerZip"]
    except KeyError:
        pass

    have_callerid = True
    try:
        # This spells "anonymous", Google uses it.
        if request.form['From'] == "+266696687": 
            have_callerid = False
    except KeyError:
        pass

    # In a more perfect world, geocode and weather lookups would be
    # done asynchronously so that the caller can listen to MOH or
    # something while lookups takes place.
    # In testing so far though, nearly all the work is done by the second ring.

    if not locality and not zip:
        for k in request.form: print("'%s':'%s'" % (k,request.form[k]))
        if have_callerid:
            longmsg = "Sorry, I could not determine your location from caller eye dee. Weather information not available."
        else:
            longmsg = "Sorry, but caller eye dee is not available for your number, so I could not determine your location."
    else:
        place = geocode.geocode()
        place.search(address=locality,postalcode=zip)

        longmsg = "Sorry, but I cannot tell where you are."
        if place.parse():
            latlon = place.latlon
            if place.long_place:
                locality = place.long_place

            # Sanity check on the location goes here
            if not latlon or not latlon[0] or not latlon[1]:
                print("Geocode failed for %s" % zip)
                if locality:
                    longmsg += " Your city is %s." % locality
                if zip:
                    longmsg += " Your zip code is %." % ' '.join([x for x in zip])
            else:
                print("Geocode result for %s %s = %s." % (place.locality,zip,latlon))
                (shortmsg, longmsg) = get_weather(latlon,locality)
    
    print("Saying '%s'" % longmsg)
    try:
        rval = response.say(longmsg)
        # rval contains XML that will be sent
    except Exception as e:
        print("Exception building reply :", e)
        
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
