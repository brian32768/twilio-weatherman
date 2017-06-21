#
#
#

if __name__ == "__main__":

    latlon = (38.352, -122.692)
    weather = get_weather(latlon,"Cotati")
    print("%d : %s" % (len(weather[0]), weather[0]))
    print("%d : %s" % (len(weather[1]), weather[1]))

