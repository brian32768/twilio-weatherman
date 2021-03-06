import flask
from utils.nws import nws

def twiml(resp):
    resp = flask.Response(str(resp))
    resp.headers['Content-Type'] = 'text/xml'
    return resp

def get_weather(latlon,locality):
    """ Get the weather conditions and forecast.
    Returns a tuple with a short format message and long messge. 
    The short message will contain only the forecast if the long message > 160 """

    n = nws(latlon)

    short_msg = long_msg = ''

    conditions = n.getObservations()
    if conditions:
        if locality:
            long_msg = "Conditions for %s: " % locality + conditions
        else:
            long_msg = "Current conditions: " + conditions

    forecast = n.getForecast()
    if forecast:
        short_msg = "Forecast for %s:" % locality + forecast

    if conditions:
        long_msg += " Forecast: " + forecast
    else:
        long_msg = short_msg
    
    if not long_msg: 
        short_msg = long_msg = "Weather information not available at this time."
    elif len(long_msg) <= 160:
        short_msg = long_msg

    return (short_msg, long_msg)

# That's all!


            
