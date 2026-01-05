#import the flask class
#blue print for the server 
from flask import Flask, jsonify 
import requests

#build the server object 
#__name__ tells flask its running in this file
app = Flask(__name__)

#python dictionary
# key value pairs
# key = name, value = Hallelujah Mountains
LOCATIONS = {
    "hallelujah_mountains": {
        "name": "Hallelujah Mountains",
        "lat": 29.13,
        "lon": 110.48
    }
}