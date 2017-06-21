#
#  Look up the lat,lon for a zip code.
#
import requests
import json
import os

google_api_key = os.environ["GOOGLE_API_KEY"]

class geocode(object):

    # Load sample so we can test without doing a fetch from Google.
    json = {'status': 'OK', 'results': [{'address_components': [{'types': ['postal_code'], 'short_name': '94931', 'long_name': '94931'}, {'types': ['locality', 'political'], 'short_name': 'Cotati', 'long_name': 'Cotati'}, {'types': ['administrative_area_level_2', 'political'], 'short_name': 'Sonoma County', 'long_name': 'Sonoma County'}, {'types': ['administrative_area_level_1', 'political'], 'short_name': 'CA', 'long_name': 'California'}, {'types': ['country', 'political'], 'short_name': 'US', 'long_name': 'United States'}], 'formatted_address': 'Cotati, CA 94931, USA', 'types': ['postal_code'], 'geometry': {'viewport': {'southwest': {'lat': 38.299015, 'lng': -122.760056}, 'northeast': {'lat': 38.3539759, 'lng': -122.66663}}, 'location_type': 'APPROXIMATE', 'bounds': {'southwest': {'lat': 38.299015, 'lng': -122.760056}, 'northeast': {'lat': 38.3539759, 'lng': -122.66663}}, 'location': {'lat': 38.3272883, 'lng': -122.7237843}}, 'place_id': 'ChIJ0a2xlX9KhIAR6aHsyne6UrA'}]}
    
    def __init__(self):
        self.updated = ''
        self.detailedResponse = ''
        self.locality = ''
        self.latlon = None

    def fetch(self, zip):
        uri = "https://maps.googleapis.com/maps/api/geocode/json?key=%s&components=postal_code:%s" % (google_api_key,zip)
        #print(uri)
        response = None
        try:
            r = requests.get(uri)
            self.json = json.loads(r.text)
        except Exception as e:
            print("geocode.fetch(%s) failed with" % zip,e)
            return False
        return True

    def parse(self):
        """Parse json from Google and return a (lat,lon) tuple """
        #print(json.dumps(self.json,indent=4))
        try:
            results = (self.json["results"])[0]
        except Exception as e:
            print("geocode.parse() failed with",e)
            return False
        
        address_components = results["address_components"]
        self.locality = None
        for c in address_components:
            if "locality" in c["types"]:
                self.locality = c["short_name"]
                break
        geometry = results["geometry"]
        location = geometry["location"]
        
        #print(location)
        self.latlon = location["lat"],location["lng"]
        return True

# That's all!
