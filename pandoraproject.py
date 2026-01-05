from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)

# 1. The Data Setup
LOCATIONS = {
    "hallelujah_mountains": {
        "name": "Hallelujah Mountains", 
        "lat": 29.13, 
        "lon": 110.48,
        # NEW LINE: A direct link to a picture of Zhangjiajie (the real mountains)
        "image": "https://miro.medium.com/v2/resize:fit:1400/format:webp/1*PPxE0RqyWyLXb8wAliU15g.jpeg"
    },
    "eastern_sea": {
        "name": "Eastern Sea", 
        "lat": 3.20, 
        "lon": 73.22,
        # NEW LINE: A direct link to a tropical reef
        "image": "https://i.natgeofe.com/n/da379044-8eab-4a53-b9a7-d9cfbf314179/GettyImages-143949963.jpg"
    }
}

# The Homepage Route
@app.route('/')
def home():
    return render_template('index.html')


# 2. The Route (The Door)
@app.route('/get_weather/<location_key>')
def get_weather(location_key):
    # Check if the location exists in our dictionary
    if location_key not in LOCATIONS:
        return jsonify({"error": "Unknown location"}), 404

    # Get the real coordinates
    target = LOCATIONS[location_key]
    
    # 3. The API Call (Talking to the outside world)
    # We ask open-meteo.com for the data
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": target['lat'], 
        "longitude": target['lon'], 
        "current_weather": "true"
    }
    
    # requests.get is like opening a browser tab in code
    response = requests.get(url, params=params)
    data = response.json()
    
    # 4. The Response (Serving the dish)
    
    return jsonify({
        "location": target['name'],
        "temp": data['current_weather']['temperature'],
        "wind": data['current_weather']['windspeed'],
        "image": target['image']  # <--- ADD THIS LINE
    })

# 5. Start the Server
if __name__ == '__main__':
    app.run(debug=True)