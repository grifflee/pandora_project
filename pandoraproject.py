"""
Pandora Weather Scanner - Flask Application
============================================

This application simulates a weather scanning system for locations on Pandora.
It demonstrates several important web development concepts:

1. RESTful API design - routes that return JSON data
2. External API integration - fetching real weather data
3. Error handling - gracefully handling failures
4. Caching - reducing API calls for better performance
5. Logging - tracking what happens in your application

LESSON: Import statements
-------------------------
We import modules that give us functionality:
- Flask: Web framework for creating web applications
- jsonify: Converts Python dictionaries to JSON responses
- render_template: Renders HTML templates
- requests: Makes HTTP requests to external APIs
- logging: Records events in your application (for debugging)
- time: Used for timestamp operations
- functools: Provides tools for working with functions (we use lru_cache)
"""
from flask import Flask, jsonify, render_template
import requests
import logging
from time import time
from functools import lru_cache

# Initialize Flask application
# LESSON: Flask(__name__) creates a Flask instance
# __name__ tells Flask where to find templates and static files
app = Flask(__name__)

# LESSON: Configure logging
# Logging helps you debug and monitor your application
# Level INFO means it will log informational messages and above (WARNING, ERROR, CRITICAL)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# LESSON: Data Structure - Dictionary of Dictionaries
# This is a nested dictionary. Each location is a key with a value that's another dictionary
# This structure makes it easy to look up location data by key
LOCATIONS = {
    "hallelujah_mountains": {
        "name": "Hallelujah Mountains", 
        "lat": 29.13,  # Latitude (north/south position on Earth)
        "lon": 110.48,  # Longitude (east/west position on Earth)
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

# LESSON: Simple cache dictionary
# This stores recent API responses so we don't hit the API every time
# Key: location_key, Value: tuple of (data, timestamp)
# We'll expire cache entries after 5 minutes (300 seconds)
WEATHER_CACHE = {}
CACHE_DURATION = 300  # 5 minutes in seconds


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
        # LESSON: Additional API parameters
        # We can request more data fields from the API
        "hourly": "relativehumidity_2m,pressure_msl"  # Get humidity and pressure too
    }
    
    try:
        # LESSON: Making HTTP requests
        # requests.get() sends a GET request to the URL with parameters
        # timeout=5 means if the server doesn't respond in 5 seconds, give up
        response = requests.get(url, params=params, timeout=5)
        
        # LESSON: HTTP Status Codes
        # 200 = success, 404 = not found, 500 = server error, etc.
        # response.raise_for_status() will raise an exception if status is not 200-299
        response.raise_for_status()
        
        data = response.json()
        logger.info(f"Successfully fetched weather data for lat={lat}, lon={lon}")
        return data
        
    except requests.exceptions.Timeout:
        # LESSON: Specific exception handling
        # We catch specific exceptions to provide better error messages
        logger.error(f"API request timed out for lat={lat}, lon={lon}")
        return None
    except requests.exceptions.RequestException as e:
        # LESSON: Catching general request exceptions
        # This catches network errors, connection errors, etc.
        logger.error(f"API request failed: {str(e)}")
        return None
    except ValueError as e:
        # LESSON: JSON parsing errors
        # If the response isn't valid JSON, json() will raise ValueError
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
        # LESSON: Time comparison
        # time() returns current Unix timestamp (seconds since 1970)
        # We check if cache is still fresh (less than CACHE_DURATION seconds old)
        if time() - timestamp < CACHE_DURATION:
            logger.info(f"Returning cached weather data for {location_key}")
            return data
        else:
            # Cache expired, remove it
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


# LESSON: Flask Route Decorator
# @app.route('/') tells Flask: "When someone visits the root URL (/), run this function"
@app.route('/')
def home():
    """
    LESSON: Route Handler Function
    -------------------------------
    This function handles requests to the homepage.
    It renders an HTML template and returns it to the browser.
    """
    return render_template('index.html')


# LESSON: Creating a New Route
# @app.route('/wiki') creates a new page at the URL /wiki
@app.route('/wiki')
def wiki():
    """
    LESSON: Wiki Page Route
    ------------------------
    This function handles requests to the /wiki URL.
    It renders the wiki.html template.
    """
    return render_template('wiki.html')


# LESSON: Dynamic Route with Parameter
# <location_key> is a URL parameter - it captures part of the URL
# Example: /get_weather/hallelujah_mountains -> location_key = "hallelujah_mountains"
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
    # LESSON: Input Validation
    # Always validate user input! Never trust data from URLs or forms.
    if location_key not in LOCATIONS:
        logger.warning(f"Invalid location key requested: {location_key}")
        return jsonify({
            "error": "Invalid location",
            "message": f"Location '{location_key}' not found"
        }), 404  # 404 = Not Found HTTP status code
    
    target = LOCATIONS[location_key]
    logger.info(f"Processing weather request for {target['name']}")
    
    # LESSON: Check cache first (faster, reduces API calls)
    cached_data = get_cached_weather(location_key)
    if cached_data:
        return jsonify(cached_data)
    
    # LESSON: Fetch from API if not in cache
    api_data = get_weather_from_api(target['lat'], target['lon'])
    
    if api_data is None:
        # LESSON: Error Response
        # Return a JSON error response with appropriate HTTP status code (500 = server error)
        return jsonify({
            "error": "Weather service unavailable",
            "message": "Failed to fetch weather data. Please try again later.",
            "location": target['name']
        }), 500
    
    # LESSON: Data Processing and Transformation
    # We extract and format the data we need from the API response
    current_weather = api_data.get('current_weather', {})
    
    # LESSON: Dictionary .get() method
    # .get() returns None (or a default value) if key doesn't exist
    # This is safer than direct access which would raise KeyError if missing
    hourly_data = api_data.get('hourly', {})
    
    # LESSON: List comprehension and safe access
    # We try to get the first value from hourly data arrays if they exist
    humidity = hourly_data.get('relativehumidity_2m', [None])[0] if hourly_data.get('relativehumidity_2m') else None
    pressure = hourly_data.get('pressure_msl', [None])[0] if hourly_data.get('pressure_msl') else None
    
    # LESSON: Building Response Dictionary
    # We structure the data we want to send back to the frontend
    response_data = {
        "location": target['name'],
        "temp": current_weather.get('temperature'),
        "wind": current_weather.get('windspeed'),
        "wind_direction": current_weather.get('winddirection'),  # NEW: Wind direction in degrees
        "weather_code": current_weather.get('weathercode'),  # NEW: Weather condition code
        "humidity": humidity,  # NEW: Relative humidity percentage
        "pressure": round(pressure, 2) if pressure else None,  # NEW: Atmospheric pressure (rounded to 2 decimals)
        "image": target['image'],
        "status": target['status'],
        "status_color": target['status_color']
    }
    
    # LESSON: Cache the response for future requests
    set_cached_weather(location_key, response_data)
    
    return jsonify(response_data)


# LESSON: Python's __name__ == '__main__' pattern
# This code only runs when the script is executed directly (not when imported)
# This is the standard way to start a Flask development server
if __name__ == '__main__':
    logger.info("Starting Pandora Weather Scanner server...")
    # LESSON: Flask.run() parameters
    # debug=True: Auto-reloads on code changes and shows detailed error pages
    # host='0.0.0.0': Makes server accessible from other devices on your network
    # port=5000: The port number (default is 5000)
    app.run(debug=True, host='0.0.0.0', port=5000)