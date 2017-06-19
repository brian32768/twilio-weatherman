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
        return

    def fetch(self, zip):
        uri = "https://maps.googleapis.com/maps/api/geocode/json?key=%s&components=postal_code:%s" % (google_api_key,zip)
        #print(uri)
        response = None
        try:
            r = requests.get(uri)
            self.json = json.loads(r.text)
        except Exception as e:
            pass
        return

    def parse(self):
        """Parse json from Google and return a (lat,lon) tuple """
        geometry = ((self.json["results"])[0])["geometry"]
        location = geometry["location"]
        #print(location)
        return (location["lat"],location["lng"])
        
if __name__ == "__main__":
    g = geocode()
    # comment out next line to skip google lookup
    g.fetch("94931")
    latlon = g.parse()
    print(latlon)

# That's all!
