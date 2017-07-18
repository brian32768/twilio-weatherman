#
#  Look up the lat,lon for a zip code.
#
import requests
import json
import os

google_api_key = os.environ["GOOGLE_API_KEY"]

class geocode(object):

    # cache = {}

    # Load sample so we can test without doing a fetch from Google.
    json = {'status': 'OK', 'results': [{'address_components': [{'types': ['postal_code'], 'short_name': '94931', 'long_name': '94931'}, {'types': ['locality', 'political'], 'short_name': 'Cotati', 'long_name': 'Cotati'}, {'types': ['administrative_area_level_2', 'political'], 'short_name': 'Sonoma County', 'long_name': 'Sonoma County'}, {'types': ['administrative_area_level_1', 'political'], 'short_name': 'CA', 'long_name': 'California'}, {'types': ['country', 'political'], 'short_name': 'US', 'long_name': 'United States'}], 'formatted_address': 'Cotati, CA 94931, USA', 'types': ['postal_code'], 'geometry': {'viewport': {'southwest': {'lat': 38.299015, 'lng': -122.760056}, 'northeast': {'lat': 38.3539759, 'lng': -122.66663}}, 'location_type': 'APPROXIMATE', 'bounds': {'southwest': {'lat': 38.299015, 'lng': -122.760056}, 'northeast': {'lat': 38.3539759, 'lng': -122.66663}}, 'location': {'lat': 38.3272883, 'lng': -122.7237843}}, 'place_id': 'ChIJ0a2xlX9KhIAR6aHsyne6UrA'}]}
    
    def __init__(self):
        self.updated = ''
        self.detailedResponse = ''
        self.locality = ''
        self.latlon = None


    def search(self, address="", postalcode="", country="US"):

#        hash = (address + "|" + postalcode + "|" + country).upper()
#        if hash in self.cache:
#            print("hit!")
#            self.json = self.cache[hash]
#            return True

        parameters = {
            "key" : google_api_key,
            "components" : "country:%s"%country
        }

        if postalcode:
            parameters["components"] = "postal_code:%s" %postalcode
        if address:
            parameters["address"] = address
            
        uri = "https://maps.googleapis.com/maps/api/geocode/json"
        response = None
        try:
            r = requests.get(uri, params=parameters)
            self.json = json.loads(r.text)
        except Exception as e:
            print("geocode.search(%s) failed with" % zip,e)
            return False

#        if len(self.cache) > 1000:
#            del self.cache
#            self.cache = {}
#        self.cache[hash] = self.json
        
        return True


    def parse(self):
        """Parse json from Google and return a (lat,lon) tuple """
        #print(json.dumps(self.json,indent=4))

        result_count = 0
        self.status = ""
        try:
            self.status = self.json["status"]
            list_results = self.json["results"]
            #print(list_results)

            # Paris gives 8 results but Newport gives only 1
            result_count = len(list_results)
            #print("result_count",result_count)
            
            results = list_results[0]
            
        except Exception as e:
            print("geocode.parse() failed with",e)
            return False

        if self.status != "OK":
            return False

        self.locality = self.short_state = self.long_state = ""
        address_components = results["address_components"]
        for c in address_components:
            if "locality" in c["types"]:
                self.locality = c["short_name"]
            elif "administrative_area_level_1" in c["types"]:
                self.short_state = c["short_name"]
                self.long_state = c["long_name"]

        geometry = results["geometry"]
        location = geometry["location"]
        
        #print(location)
        self.latlon = location["lat"],location["lng"]

        # Try to make return names that make sense

        # Only tack on state if there is more than one result
        self.short_place = self.locality
        if result_count > 1 and self.short_state:
            if self.short_place: self.short_place += " "
            self.short_place += self.short_state

        # Long place name always gets state tacked on
        self.long_place = self.locality
        if self.long_state:
            if self.long_place: self.long_place += ", "
            self.long_place += self.long_state

        return True

# That's all!
