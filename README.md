# twilio-weatherman
Everyone wants to talk about the weather, including phone bots.

This is a Twilio app that will respond to sms and voice requests.

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

Test it with curl
   ```bash
   curl "https://api.weather.gov/points/38.332,-122.692/forecast"
   ```

Learn more about it at https://forecast-v3.weather.gov/documentation
