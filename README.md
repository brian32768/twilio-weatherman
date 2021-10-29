# twilio-weatherman
Everyone wants to talk about the weather, including phone bots.

This is a Twilio app that will respond to sms and voice requests.

Looks like I wrote this before I learned about conda and docker. The WSGI code was written for Linux.
I've started to update it for Conda and Telegram.

## pyweatherman

The python flask version that I am currently writing.
There is another README file there with more details.

## nodeweatherman

I plan on doing a Node version.

# External services

## Twilio

Twilio handles SMS messages and voice calls for us.

## Google Geocoding

I use Google to geocode zip codes into lat,lon

## NOAA National Weather Service

The NWS takes the lat,lon from the geocoder and turns it into weather information.

Yes, the NWS has an API.
Learn more about it at https://forecast-v3.weather.gov/documentation

### Test NWS with curl

Some examples of curl to test NWS responses

  ```bash
  curl -H "Accept: application/vnd.noaa.dwml+xml;version=1" "https://api.weather.gov/points/38.332,-122.692"
  curl "https://api.weather.gov/points/38.332,-122.692/forecast"
  ```


