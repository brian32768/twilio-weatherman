#
#  Look up a weather forecast at the National Weather Service
#
from __future__ import print_function
import os
import geojson
import requests

baseuri  = "https://api.weather.gov/"
pointuri = baseuri + "points/%s,%s/"

def c_to_f(c):
    """Input: Temperature in celsius (or possibly None)
    Returns a human-friendly string in Fahrenheit. """
    try:
        f = "%d degrees" % round(c * 9 / 5 + 32,0)
    except Exception as e:
        f = "temperature not available"
        pass
    return f

def ms_to_mph(ms):
    """Input: wind speed in meters/second,
    Returns a human friendly string in mph. """
    try:
        mph = float(ms) * 2.236936
        if mph<1:
            ws = "wind speed: calm"
        else:
            ws = "wind speed: %d mph" % round(mph,0)
    except Exception as e:
        ws = '' # Don't report anything if there is no wind speed reading available
        pass
    return ws

class nws(object):
    def __init__(self, latlon):
        self.latlon = latlon
        self.updated = self.detailedForecast = None
        return

    def getForecast(self):
        """ Return a human-readable forecast. """
        r = requests.get(pointuri % self.latlon + "/forecast")
        j = geojson.loads(r.text)
        properties = j["properties"]
        periods = properties["periods"]
        current = periods[0]
        self.forecastUpdated = properties["updated"]
        self.detailedForecast = current["detailedForecast"]
        return self.detailedForecast
    
    def getStations(self):
        """Return the list of stations for a given point, sorted by proximity. """
        r = requests.get(pointuri % self.latlon + 'stations')
        j = geojson.loads(r.text)
        #print(geojson.dumps(j,indent=4))

        stations = []
        for feature in j["features"]:
            #print(feature)
            properties = feature["properties"]
            stations.append((properties["stationIdentifier"], properties["name"]))
            pass

        return stations

    def getObservations(self):
        """ Return a human-readable string containing current weather observations. """
    
        # Sometimes the first station does not have any observations so
        # we have to loop until we get at least the temperature.
        stations = self.getStations()
        for stationId,stationName in stations:
            #print(station)
            r = requests.get(baseuri + "stations/%s/observations/current" % stationId)
            j = geojson.loads(r.text)
            #print(geojson.dumps(j,indent=4))
            temperature = None
            conditions = None
            try:
                properties = j["properties"]
                temperature_c = (properties["temperature"])["value"]
                temperature = c_to_f(temperature_c)
                windspeed   = ms_to_mph((properties["windSpeed"])["value"])
                description = properties["textDescription"]
                conditions = "%s, %s, %s." % (description, temperature, windspeed)
                self.stationName = stationName
                self.conditions = conditions
                pass
            except KeyError as e:
                print(stationName,"empty")
                pass
            if temperature:
                # Windspeed and description would be good but not worth waiting for
                break

        return conditions

if __name__ == "__main__":
    latlon   = (38.352, -122.692) # Cotati
    n = nws(latlon)
    forecast = n.getForecast()
    print(forecast)
    conditions = n.getObservations()
    print(n.stationName,conditions)

# That's all!
