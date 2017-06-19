#
#  Look up a weather forecast at the National Weather Service
#
import requests
import json

uri = "https://api.weather.gov/points/%s,%s/forecast"

class nws(object):

    def __init__(self, lat,lon):
        r = requests.get(uri % (lat,lon))
        j = json.loads(r.text)
        properties = j["properties"]
        self.updated = properties["updated"]
        periods = properties["periods"]
        current = periods[0]
        self.detailedForecast = current["detailedForecast"]

if __name__ == "__main__":
    n = nws(38.352, -122.672)
    print("updated:", n.updated)
    print(n.detailedForecast)

# That's all!
