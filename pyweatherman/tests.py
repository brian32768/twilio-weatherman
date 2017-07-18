#
#
#
from utils.helpers import get_weather, twiml
from utils.geocode import geocode

if __name__ == "__main__":

    # utils.geocode
    g = geocode()

    # test caching
    g.search(postalcode="94931")
    g.search(postalcode="94931")
    g.search(postalcode="94931")
    g.search(postalcode="94931")
    g.search(postalcode="94931")

    # comment out next line to skip google lookup and use sample json
    g.search(postalcode="94931")
    if not g.parse():
        print("Status ", g.status)
    else:
        latlon = g.latlon
        print("Latlon of '%s' is %s" % (g.locality, g.latlon))

    g.search(address="Cotati")
    if not g.parse():
        print("Status ", g.status)
    else:
        latlon = g.latlon
        print("Latlon of '%s' is %s" % (g.locality, g.latlon))

    g.search(address="Asilomar")
    if not g.parse():
        print("Status ", g.status)
    else:
        latlon = g.latlon
        print("Latlon of '%s' is %s" % (g.locality, g.latlon))

    g.search(address="Newport")
    if not g.parse():
        print("Status ", g.status)
    else:
        latlon = g.latlon
        print("Latlon of '%s'/'%s' is %s" % (g.short_place, g.long_place, g.latlon))

    g.search(address="Newport, OR")
    if not g.parse():
        print("Status ", g.status)
    else:
        latlon = g.latlon
        print("Latlon of '%s'/'%s' is %s" % (g.short_place, g.long_place, g.latlon))

    g.search(address="Newport, OR")
    if not g.parse():
        print("Status ", g.status)
    else:
        latlon = g.latlon
        print("Latlon of '%s'/'%s' is %s" % (g.short_place, g.long_place, g.latlon))

    g.search(address="Paris")
    if not g.parse():
        print("Status ", g.status)
    else:
        latlon = g.latlon
        print("Latlon of '%s'/'%s' is %s" % (g.short_place, g.long_place, g.latlon))


    # utils.helpers
    
    #latlon = (38.352, -122.692)
    weather = get_weather(latlon,"Cotati")
    print("%d : %s" % (len(weather[0]), weather[0]))
    print("%d : %s" % (len(weather[1]), weather[1]))

    #xml = twiml(response)
    #print(xml)


    
