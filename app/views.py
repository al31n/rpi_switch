from flask import render_template, request
from app import app
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

pins = {
    4 : {'name': 'LAMP SWITCH', 'state': GPIO.LOW }
}

for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

@app.route("/")
def index():
    for pin in pins:
        pins[pin]['state'] = GPIO.input(pin)
    templateDatea = {
        'pins' : pins
    }
    return render_template('index.html', **templateData)

@app.route("/<changePin>/<action>")
def action(changePin, action):
    changePin = int(changePin)
    deviceName = pins[changePin]['name']

    if action == "on":
        GPIO.output(changePin, GPIO.HIGH)
        message = deviceName + " is on."
    elif action == "off":
        GPIO.output(changePin, GPIO.LOW)
        message = deviceName + " is off."
    elif action == "toggle":
        GPIO.output(changePin, not GPIO.input(changePin))
        message = "Toggled " + deviceName + "."

    # update pin state
    for pin in pins:
        pins[pin]['state'] = GPIO.input(pin)

    templateData = {
        'message' : message,
        'pins' : pins
    }

    return render_template('index.html', **templateData)
