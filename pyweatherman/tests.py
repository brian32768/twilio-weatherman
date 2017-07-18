#
#
#
from utils.helpers import get_weather, twiml
from utils.geocode import geocode

if __name__ == "__main__":

    # utils.geocode

    g = geocode()
    # comment out next line to skip google lookup and use sample json
    g.search(postalcode="94931")
    g.parse()
    latlon = g.latlon
    print("Latlon of '%s' is %s" % (g.locality, g.latlon))

    g.search(address="Cotati")
    g.parse()
    latlon = g.latlon
    print("Latlon of '%s' is %s" % (g.locality, g.latlon))

    g.search(address="Paris")
    g.parse()
    latlon = g.latlon
    print("Latlon of '%s' is %s" % (g.locality, g.latlon))

    exit(0)

    # utils.helpers
    
    #latlon = (38.352, -122.692)
    weather = get_weather(latlon,"Cotati")
    print("%d : %s" % (len(weather[0]), weather[0]))
    print("%d : %s" % (len(weather[1]), weather[1]))

    #xml = twiml(response)
    #print(xml)


    
