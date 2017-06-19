#
#  Look up a weather forecast at the National Weather Service
#
import requests
import json

uri = "https://api.weather.gov/points/%s,%s/forecast"

class nws(object):

    def __init__(self):
        self.json = self.updated = self.detailedForecast = None
        return

    def fetch(self,latlon):
        r = requests.get(uri % latlon)
        self.json = json.loads(r.text)
        return

    def parse(self):
        properties = self.json["properties"]
        periods = properties["periods"]
        current = periods[0]
        self.updated = properties["updated"]
        self.detailedForecast = current["detailedForecast"]
        return

if __name__ == "__main__":
    n = nws()
    n.fetch((38.352, -122.672))
    n.parse()
    print("updated:", n.updated)
    print(n.detailedForecast)

# That's all!
