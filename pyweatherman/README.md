# Receive updates on the weather via a phone.

## What this is

This is a Twilio app written in Python and Flask that will respond to
sms and voice requests with information on weather conditions.

Currently the weather report is just the forecast for the immediate future.
The source is the NOAA National Weather Service.

## What it does

### Responds to SMS messages and phone calls.

If you send a 5 digit zip code in an SMS, it will look that up and
then send a weather report back for that area.

If you send anything else in the SMS body, or leave it empty,
it will use your phone number as your location.

### Response to voice calls

You call the number and it says the weather report.

In this case it always uses caller id to determine location. If you
have a mobile phone number from Butte, Montana then that's the report you
will get, no matter where you are.

## How to make it work

This project is written and tested with Python 3, but it might work with Python 2.7 as well.

To pull a copy of the code from github,

  ```bash
  git clone github.com:brian32768/twilio-weatherman.git
  cd twilio-weatherman/pyweatherman
  ```

Now you need to do a little prep work before you can run the app.

## 1. Set up a virtual environment for Python and install dependencies

```bash
  virtualenv venv
  source venv/bin/activate
  pip install -r requirements.txt
  ```
## 2. Set up Google API key

The geocoder in app/geocode.py uses Google's service to convert your
zip code into a location in (lat,lon) format.  That means you have to
set up a Google API key and put it into your environment. You can get
a (free) key here:
https://developers.google.com/maps/documentation/geocoding/get-api-key

The key is good for up to 2500 geocode operations a day.  I don't
include my key here because I don't want you to use up my geocodes.

You must set GOOGLE_API_KEY before you run manage.py or you will get a runtime error.

## 3. Make the services accessible to Twilio

There are three URLs handled by this app, "/messaging/", "/voice/", and "/status/".
They all accept POST data from Twilio.

For testing there is one more you can hit from a browser directly, "/home/".

The flask script runs on localhost (port 127.0.0.1) so you have to
allow Twilio to access it. For testing running the flask service is
fine, so I add this to my nginx server. You could use ngrok as an
alternative if you don't have a web server.

  bash```
  # Act as a proxy for a flask instance, this is not for production!
  # In real life you want to use uWSGI to run flask apps.
     location /twilio/ {
            proxy_pass http://127.0.0.1:5000/;
     }
  ```
  
This will accept URLs such as https://bellman.wildsong.biz/twilio/status/
and send them to http://127.0.0.1:5000/status/

## 4. Set up a phone number

Buy a phone number from Twilio and then point it this service.  You
have to put the URL that is accessible from Twilio into the slots for
SMS and Voice.  You can also put one in for call status updates, but
that is not necessary.

The URLs will depend on how you set up a proxy in the previous step.
They have to be accessible from Twilio, so the 127.0.0.1 version won't
work.

## 5. Run the service

If you are not still running in the virtual environment from the first step, 
source venv/bin/activate

  ```bash
   python manage.py runserver
  ```

If your browser is running on the same machine as the service you should be able to hit
http://127.0.0.1:5000/home/ and see a results page.

If you have properly set up a proxy, then you should be able to hit it through the proxy now too.
For me this means https://bellman.wildsong.biz/twilio/home/

# Test results for various add-ons

I experimented a bit with Twilio caller id add-ons and did not find any benefits for this app.
I only tested with SMS, maybe they work better with voice calls.

If you turn on the add-on "IceHook Systems Scout" you will see
something like this for my Google Voice Corvallis number, Lane county
(wrong)

  'AddOns':'{"status":"successful","message":null,"code":null,"results":{"icehook_scout":{"request_sid":"XR2632bbf7aa3249994a0bd1f9bcff1650","status":"successful","message":null,"code":null,"result":{"timezone":"America/Los_Angeles","administrative_area_level_3":null,"administrative_area_level_2":"Lane County","administrative_area_level_1":"Oregon","administrative_area_level_1_short":"OR","locality":"Eugene","sublocality_level_1":null,"postal_code":"97401","point_of_interest":null,"neighborhood":"Downtown","clli":"EUGNOR53","country":"United States","country_short":"US","lata":"670","ocn":"076F","operating_company_name":"Bandwidth SMSEnabled","operating_company_type":"clec","ported":true,"location_routing_number":"+15416310367","line_type":"voip"}}}}'

For my cellphone it shows Contra Costa county, (wrong)

  'AddOns':'{"status":"successful","message":null,"code":null,"results":{"icehook_scout":{"request_sid":"XR5fb81c7a977970a68e84934f6e4ed93f","status":"successful","message":null,"code":null,"result":{"timezone":"America/Los_Angeles","administrative_area_level_3":null,"administrative_area_level_2":"Contra Costa County","administrative_area_level_1":"California","administrative_area_level_1_short":"CA","locality":"Concord","sublocality_level_1":null,"postal_code":"94520","point_of_interest":null,"neighborhood":null,"clli":"CNCRCALZ","country":"United States","country_short":"US","lata":"722","ocn":"6529","operating_company_name":"T-Mobile USA, Inc.","operating_company_type":"wireless","ported":true,"location_routing_number":"+14156900000","line_type":"mobile"}}}}'

"Whitepages Pro Caller Identification"

Google: Shows correct city and zip, also has (probably) zip code centroid lat lon

'AddOns':'{"status":"successful","message":null,"code":null,"results":{"whitepages_pro_caller_id":{"request_sid":"XR7c7652cf56e59cc062d32531964f5586","status":"successful","message":null,"code":null,"result":{"results":[{"id":{"key":"Phone.a0af6fef-a2e1-4b08-cfe3-bc7128b6855c.Durable","type":"Phone"},"line_type":"NonFixedVOIP","belongs_to":[],"associated_locations":[{"id":{"key":"Location.8c6d2664-3d79-4ce9-b611-9107175cf82c.Durable","type":"Location"},"type":"CityPostalCode","valid_for":null,"legal_entities_at":null,"city":"Corvallis","postal_code":"97330","zip4":null,"state_code":"OR","country_code":"US","is_receiving_mail":null,"not_receiving_mail_reason":null,"usage":null,"delivery_point":null,"address_type":null,"lat_long":{"latitude":44.6364,"longitude":-123.2804,"accuracy":"PostalCode"},"is_deliverable":null,"standard_address_line1":"","standard_address_line2":"","is_historical":false}],"is_valid":true,"phone_number":"5413687383","country_calling_code":"1","carrier":"Google Voice","is_prepaid":null}],"messages":[]}}}}'

Ting phone: shows Sebastopol which matches the phone exchange (827-xxxx) but not my address and not my location.

  'AddOns':'{"status":"successful","message":null,"code":null,"results":{"whitepages_pro_caller_id":{"request_sid":"XRcfa0fd7548beb99e28f3e161c497f7c5","status":"successful","message":null,"code":null,"result":{"results":[{"id":{"key":"Phone.a8676fef-a2e1-4b08-cfe3-bc7128b74bcb.Durable","type":"Phone"},"line_type":"Mobile","belongs_to":[],"associated_locations":[{"id":{"key":"Location.7a5df8c6-0d8f-43c1-bca1-acaf43436d3d.Durable","type":"Location"},"type":"CityPostalCode","valid_for":null,"legal_entities_at":null,"city":"Sebastopol","postal_code":"95472","zip4":null,"state_code":"CA","country_code":"US","is_receiving_mail":null,"not_receiving_mail_reason":null,"usage":null,"delivery_point":null,"address_type":null,"lat_long":{"latitude":38.3844,"longitude":-122.8597,"accuracy":"PostalCode"},"is_deliverable":null,"standard_address_line1":"","standard_address_line2":"","is_historical":false}],"is_valid":true,"phone_number":"7078270003","country_calling_code":"1","carrier":"T-Mobile USA","is_prepaid":null}],"messages":[]}}}}'

"Twilio Caller Name" is not useful, there is NO information in there.

Google
'AddOns':'{"status":"successful","message":null,"code":null,"results":{"twilio_caller_name":{"request_sid":"XR2d9791f8717553df678072bb9ac398ab","status":"successful","message":null,"code":null,"result":{"caller_name":{"caller_name":null,"caller_type":null,"error_code":null},"phone_number":"+15413687383"}}}}'

Ting
  'AddOns':'{"status":"successful","message":null,"code":null,"results":{"twilio_caller_name":{"request_sid":"XRbd77ada6ef64ff55c8418c5b6f0e3752","status":"successful","message":null,"code":null,"result":{"caller_name":{"caller_name":null,"caller_type":null,"error_code":null},"phone_number":"+17078270003"}}}}'

Next Caller's "Advanced Caller Id" is 10 cents and useless

Tracfone
'AddOns':'{"status":"successful","message":null,"code":null,"results":{"nextcaller_advanced_caller_id":{"request_sid":"XR511ecd6ba88d78ae2b8a7553b0f02b6e","status":"successful","message":null,"code":null,"result":{"records":[{"id":"0e4e8f6d826ddd209cf0dd33ac392d","first_name":"","first_pronounced":"","middle_name":"","last_name":"","name":"","phone":[{"number":"5416026708","carrier":"Verizon Wireless","line_type":"Mobile"}],"address":[],"relatives":[],"email":"","linked_emails":[],"social_links":[],"age":"","education":"","gender":"","high_net_worth":"","home_owner_status":"","household_income":"","length_of_residence":"","marital_status":"","market_value":"","occupation":"","presence_of_children":""}]}}}}'

