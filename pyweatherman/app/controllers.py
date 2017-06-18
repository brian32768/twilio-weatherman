from flask import render_template

from app import app

@app.route('/home/')
def home():
    print("Accessing home page, which really does nothing at all.")
    return render_template('home.html')

@app.route('/sms/')
def sms():
    print("We received an SMS message. Send a reply")
    return render_template('sms.xml')

@app.route('/voice/')
def voice():
    print("We received a voice call. Say something")
    return render_template('voice.xml')

@app.route('/status_update/')
def status-update():
    print("We received a status update indicating call progress or some such thing.")
    return render_template('status_update.html')

# That's all!
