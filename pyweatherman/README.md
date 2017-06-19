# Receive updates on the weather via a phone.
Everyone wants to talk about the weather, even phone bots.

This is a Twilio app written in Python and Flask that will respond to
sms and voice requests with information on weather conditions.

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
  
## 2. Set up environment variables

I don't want my credentials stored in github so I put them into these environment variables:

I keep these in a shell script outside of this github project.

## Run

If you are not still running in the virtual environment from the first step, 
source venv/bin/activate

  ```bash
   python manage.py runserver
  ```

You have to go to twilio.com and set up a phone number to point at this service.

Currently I expose my development server on all IP addresses (see run.py), but it's behind a firewall.
You could limit it to localhost and hide it behind a proxy or ngrok.

To allow access from Twilio I put the following into my nginx server:

 # Act as a proxy for a flask instance, this is not for production!
 # In real life you want to use uWSGI to run flask apps.
     location /twilio/ {
            proxy_pass http://127.0.0.1:5000/;
     }

This will accept URLs such as https://bellman.wildsong.biz/twilio/status/
and send them to http://127.0.0.1:5000/status

# Sample POST from Twilio, after passing through nginx proxy.

 'NumSegments':'1'
 'From':'+15413687383'
 'FromCountry':'US'
 'Body':'send me a forecast'
 'MessageSid':'SMeba3e3587744372d61acb477f8dfa4bf'
 'FromZip':'97333'
 'FromState':'OR'
 'AccountSid':'ACa2b8661e01408dd8160ee8a26a00d448'
 'AddOns':'{"status":"successful","message":null,"code":null,"results":{}}'
 'SmsStatus':'received'
 'ToCountry':'US'
 'FromCity':'CORVALLIS'
 'SmsMessageSid':'SMeba3e3587744372d61acb477f8dfa4bf'
 'ToState':'CA'
 'ApiVersion':'2010-04-01'
 'ToZip':'95472'
 'NumMedia':'0'
 'SmsSid':'SMeba3e3587744372d61acb477f8dfa4bf'
 'To':'+17078279200'
 'ToCity':'SEBASTOPOL'
