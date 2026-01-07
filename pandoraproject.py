from flask import Flask, jsonify, render_template
import requests
import logging
from time import time
from functools import lru_cache

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

LOCATIONS = {
    "hallelujah_mountains": {
        "name": "Hallelujah Mountains", 
        "lat": 29.13,
        # "lon": 110.48,
        "image": "https://miro.medium.com/v2/resize:fit:1400/format:webp/1*PPxE0RqyWyLXb8wAliU15g.jpeg",
        "status": "Stable",
        "status_color": "green"
    },
    "eastern_sea": {
        "name": "Eastern Sea", 
        "lat": 3.20, 
        "lon": 73.22,
        "image": "static/eastern_sea.png",
        "status": "RDA Activity Detected",
        "status_color": "red"
    }
}

CHARACTERS = {
    "jake": {
        "name": "Jake Sully",
        "image": "jake_sully.jpg",
        "additional_images": [],
        "description": "[Description]: Jake sully is the main character of the Avatar franchise",
        "stats": {
            "strength": "98",
            "speed": "88",
            "intelligence": "90",
            "combat": "99"
        }
    },
    "neytiri": {
        "name": "Neytiri",
        "image": "neytiri.jpg",
        "additional_images": [],
        "description": "[Description section - Add character description here]",
        "stats": {
            "strength": "[Add value]",
            "speed": "[Add value]",
            "intelligence": "[Add value]",
            "combat": "[Add value]"
        }
    },
    "colonel": {
        "name": "Colonel Miles Quaritch",
        "image": "colonel_quaritch.jpeg",
        "additional_images": [],
        "description": "[Description section - Add character description here]",
        "stats": {
            "strength": "[Add value]",
            "speed": "[Add value]",
            "intelligence": "[Add value]",
            "combat": "[Add value]"
        }
    },
    "ronal": {
        "name": "Ronal",
        "image": "ronal.jpg",
        "additional_images": [],
        "description": "[Description section - Add character description here]",
        "stats": {
            "strength": "[Add value]",
            "speed": "[Add value]",
            "intelligence": "[Add value]",
            "combat": "[Add value]"
        }
    },
    "kiri": {
        "name": "Kiri",
        "image": "kiri.jpg",
        "additional_images": [],
        "description": "[Description section - Add character description here]",
        "stats": {
            "strength": "[Add value]",
            "speed": "[Add value]",
            "intelligence": "[Add value]",
            "combat": "[Add value]"
        }
    },
    "toruk": {
        "name": "Toruk",
        "image": "toruk.jpg",
        "additional_images": [],
        "description": "[Description section - Add character description here]",
        "stats": {
            "strength": "[Add value]",
            "speed": "[Add value]",
            "intelligence": "[Add value]",
            "combat": "[Add value]"
        }
    },
    "tuk": {
        "name": "Tuk",
        "image": "tuk.jpg",
        "additional_images": [],
        "description": "[Description section - Add character description here]",
        "stats": {
            "strength": "[Add value]",
            "speed": "[Add value]",
            "intelligence": "[Add value]",
            "combat": "[Add value]"
        }
    },
    "neteyam": {
        "name": "Neteyam",
        "image": "neteyam.jpg",
        "additional_images": [],
        "description": "[Description section - Add character description here]",
        "stats": {
            "strength": "[Add value]",
            "speed": "[Add value]",
            "intelligence": "[Add value]",
            "combat": "[Add value]"
        }
    },
    "loak": {
        "name": "Lo'ak",
        "image": "loak.jpg",
        "additional_images": [],
        "description": "[Description section - Add character description here]",
        "stats": {
            "strength": "[Add value]",
            "speed": "[Add value]",
            "intelligence": "[Add value]",
            "combat": "[Add value]"
        }
    },
    "tsireya": {
        "name": "Tsireya",
        "image": "tsireya.jpg",
        "additional_images": [],
        "description": "[Description section - Add character description here]",
        "stats": {
            "strength": "[Add value]",
            "speed": "[Add value]",
            "intelligence": "[Add value]",
            "combat": "[Add value]"
        }
    },
    "tonowari": {
        "name": "Tonowari",
        "image": "tonowari.jpg",
        "additional_images": [],
        "description": "[Description section - Add character description here]",
        "stats": {
            "strength": "[Add value]",
            "speed": "[Add value]",
            "intelligence": "[Add value]",
            "combat": "[Add value]"
        }
    },
    "varang": {
        "name": "Varang",
        "image": "varang.jpg",
        "additional_images": [],
        "description": "[Description section - Add character description here]",
        "stats": {
            "strength": "[Add value]",
            "speed": "[Add value]",
            "intelligence": "[Add value]",
            "combat": "[Add value]"
        }
    }
}

WEATHER_CACHE = {}

CACHE_DURATION = 10


def get_weather_from_api(lat, lon):
    """
    LESSON: Function Definition and Documentation
    ----------------------------------------------
    This function fetches weather data from an external API.
    
    Parameters:
        lat (float): Latitude coordinate
        lon (float): Longitude coordinate
    
    Returns:
        dict: Weather data from the API, or None if request fails
    
    LESSON: Error Handling with try/except
    ---------------------------------------
    try/except blocks let you handle errors gracefully instead of crashing.
    This is crucial for production applications!
    """
    url = "https://api.open-meteo.com/v1/forecast"
    
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": "true",
        "hourly": "relativehumidity_2m,pressure_msl"
    }
    
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        logger.info(f"Successfully fetched weather data for lat={lat}, lon={lon}")
        return data
        
    except requests.exceptions.Timeout:
        logger.error(f"API request timed out for lat={lat}, lon={lon}")
        return None
        
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {str(e)}")
        return None
        
    except ValueError as e:
        logger.error(f"Failed to parse JSON response: {str(e)}")
        return None


def get_cached_weather(location_key):
    """
    LESSON: Caching Strategy
    -------------------------
    Caching stores frequently accessed data in memory to avoid repeated API calls.
    This improves performance and reduces load on external services.
    
    Returns:
        dict or None: Cached weather data if valid, None if cache expired or missing
    """
    if location_key in WEATHER_CACHE:
        data, timestamp = WEATHER_CACHE[location_key]
        
        if time() - timestamp < CACHE_DURATION:
            logger.info(f"Returning cached weather data for {location_key}")
            return data
        else:
            del WEATHER_CACHE[location_key]
            logger.info(f"Cache expired for {location_key}")
    
    return None


def set_cached_weather(location_key, data):
    """
    LESSON: Storing data in cache
    ------------------------------
    We store the data along with a timestamp so we know when it was cached.
    """
    WEATHER_CACHE[location_key] = (data, time())
    logger.info(f"Cached weather data for {location_key}")


@app.route('/')
def home():
    """
    LESSON: Route Handler Function
    -------------------------------
    This function handles requests to the homepage.
    It renders an HTML template and returns it to the browser.
    """
    return render_template('index.html')


@app.route('/wiki')
def wiki():
    """
    LESSON: Wiki Page Route
    ------------------------
    This function handles requests to the /wiki URL.
    It renders the wiki.html template.
    """
    return render_template('wiki.html')


@app.route('/map')
def map_page():
    """
    Map Page Route
    --------------
    This function handles requests to the /map URL.
    It renders the map.html template showing a map of Pandora.
    """
    return render_template('map.html')


@app.route('/character/<character_name>')
def character_page(character_name):
    """
    LESSON: Character Page Route
    -----------------------------
    This function handles requests to character pages.
    It renders the character.html template and passes the character name.
    
    Parameters:
        character_name (str): The name of the character from the URL
    """
    character_data = CHARACTERS.get(character_name, {
        "name": character_name.title(),
        "image": f"{character_name}.jpg",
        "additional_images": [],
        "description": "[Description section - Add character description here]",
        "stats": {
            "strength": "[Add value]",
            "speed": "[Add value]",
            "intelligence": "[Add value]",
            "combat": "[Add value]"
        }
    })
    
    return render_template('character.html', character_name=character_name, character_data=character_data)


@app.route('/get_weather/<location_key>')
def get_weather(location_key):
    """
    LESSON: Main Weather Endpoint
    -----------------------------
    This endpoint:
    1. Validates the location key
    2. Checks cache for recent data
    3. Fetches from API if needed
    4. Processes and returns weather data
    
    LESSON: Error Handling in Routes
    ---------------------------------
    We use try/except to handle errors and return appropriate HTTP status codes.
    """
    if location_key not in LOCATIONS:
        logger.warning(f"Invalid location key requested: {location_key}")
        return jsonify({
            "error": "Invalid location",
            "message": f"Location '{location_key}' not found"
        }), 404
    
    target = LOCATIONS[location_key]
    logger.info(f"Processing weather request for {target['name']}")
    
    cached_data = get_cached_weather(location_key)
    
    if cached_data:
        return jsonify(cached_data)
    
    api_data = get_weather_from_api(target['lat'], target['lon'])
    
    if api_data is None:
        return jsonify({
            "error": "Weather service unavailable",
            "message": "Failed to fetch weather data. Please try again later.",
            "location": target['name']
        }), 500
    
    current_weather = api_data.get('current_weather', {})
    hourly_data = api_data.get('hourly', {})
    humidity = hourly_data.get('relativehumidity_2m', [None])[0] if hourly_data.get('relativehumidity_2m') else None
    pressure = hourly_data.get('pressure_msl', [None])[0] if hourly_data.get('pressure_msl') else None
    
    response_data = {
        "location": target['name'],
        "temp": current_weather.get('temperature'),
        "wind": current_weather.get('windspeed'),
        "wind_direction": current_weather.get('winddirection'),
        "weather_code": current_weather.get('weathercode'),
        "humidity": humidity,
        "pressure": round(pressure, 2) if pressure else None,
        "image": target['image'],
        "status": target['status'],
        "status_color": target['status_color']
    }
    
    set_cached_weather(location_key, response_data)
    
    return jsonify(response_data)


if __name__ == '__main__':
    logger.info("Starting Pandora Weather Scanner server...")
    app.run(debug=True, host='0.0.0.0', port=5000)
