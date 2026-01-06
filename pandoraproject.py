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
# Line 25: from flask import Flask, jsonify, render_template
#   - from: Python keyword that imports from a module
#   - flask: The Flask web framework module
#   - import: Python keyword to bring in functionality
#   - Flask: The main Flask class (creates web application instances)
#   - jsonify: Function that converts Python dictionaries to JSON format (for API responses)
#   - render_template: Function that takes HTML template files and fills in variables
from flask import Flask, jsonify, render_template

# Line 26: import requests
#   - import: Python keyword
#   - requests: Third-party library for making HTTP requests (calling external APIs)
#   - This allows us to fetch data from the weather API
import requests

# Line 27: import logging
#   - import: Python keyword
#   - logging: Built-in Python module for recording events (debugging, errors, info)
#   - This lets us write messages to the console/terminal
import logging

# Line 28: from time import time
#   - from: Python keyword
#   - time: Built-in Python module for time-related functions
#   - import: Python keyword
#   - time: The time() function (returns current Unix timestamp)
#   - We use this to track when data was cached
from time import time

# Line 29: from functools import lru_cache
#   - from: Python keyword
#   - functools: Built-in Python module with function tools
#   - import: Python keyword
#   - lru_cache: Function decorator for caching (we import it but don't use it currently)
from functools import lru_cache

# Line 31-34: Initialize Flask application
# Line 34: app = Flask(__name__)
#   - app: Variable name (we'll use this to define routes)
#   - =: Assignment operator (stores value in variable)
#   - Flask: The Flask class we imported
#   - (__name__): Passes the current module name to Flask
#     - __name__: Special Python variable that is '__main__' when script runs directly
#     - When imported, __name__ is the module name
#   - Flask uses __name__ to find templates and static files automatically
app = Flask(__name__)

# Line 36-43: Configure logging system
# Line 39-42: logging.basicConfig(...)
#   - logging: The logging module we imported
#   - .basicConfig: Function that sets up logging configuration
#   - (): Function call with parameters inside
#   - level=logging.INFO: Sets minimum log level to INFO (shows INFO, WARNING, ERROR, CRITICAL)
#   - format=...: Defines how log messages look (timestamp, name, level, message)
logging.basicConfig(
    level=logging.INFO,  # Only show INFO level and above (not DEBUG)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'  # Format: "2024-01-15 10:30:45 - __main__ - INFO - message"
)

# Line 43: logger = logging.getLogger(__name__)
#   - logger: Variable name for our logger object
#   - =: Assignment operator
#   - logging: The logging module
#   - .getLogger: Function that creates/gets a logger instance
#   - (__name__): Passes module name (creates logger named after this file)
#   - We'll use logger.info(), logger.error(), etc. to write log messages
logger = logging.getLogger(__name__)

# Line 45-65: LOCATIONS dictionary - stores location data
# Line 48: LOCATIONS = {
#   - LOCATIONS: Variable name (uppercase = constant, shouldn't change)
#   - =: Assignment operator
#   - {: Starts a dictionary (key-value pairs)
#   - This is a nested dictionary: dictionary inside a dictionary
LOCATIONS = {
    # Line 49: "hallelujah_mountains": {
    #   - "hallelujah_mountains": Dictionary key (string, used to look up this location)
    #   - :: Separates key from value
    #   - {: Starts another dictionary (the value for this key)
    "hallelujah_mountains": {
        # Line 50: "name": "Hallelujah Mountains",
        #   - "name": Key in inner dictionary
        #   - :: Separates key from value
        #   - "Hallelujah Mountains": Value (display name)
        #   - ,: Separates dictionary entries
        "name": "Hallelujah Mountains", 
        
        # Line 51: "lat": 29.13,
        #   - "lat": Key (latitude)
        #   - :: Separates key from value
        #   - 29.13: Value (latitude coordinate, float number)
        "lat": 29.13,  # Latitude (north/south position on Earth)
        
        # Line 52: "lon": 110.48,
        #   - "lon": Key (longitude)
        #   - :: Separates key from value
        #   - 110.48: Value (longitude coordinate, float number)
        "lon": 110.48,  # Longitude (east/west position on Earth)
        
        # Line 53: "image": "https://...",
        #   - "image": Key
        #   - :: Separates key from value
        #   - "https://...": Value (URL to image)
        "image": "https://miro.medium.com/v2/resize:fit:1400/format:webp/1*PPxE0RqyWyLXb8wAliU15g.jpeg",
        
        # Line 54: "status": "Stable",
        #   - "status": Key
        #   - :: Separates key from value
        #   - "Stable": Value (status text)
        "status": "Stable",
        
        # Line 55: "status_color": "green"
        #   - "status_color": Key
        #   - :: Separates key from value
        #   - "green": Value (CSS color name)
        "status_color": "green"
    },  # Line 56: }, - Closes the inner dictionary, comma separates from next entry
    
    # Line 57-64: Second location entry (same structure as above)
    "eastern_sea": {
        "name": "Eastern Sea", 
        "lat": 3.20, 
        "lon": 73.22,
        "image": "static/eastern_sea.png",
        "status": "RDA Activity Detected",
        "status_color": "red"
    }
}  # Line 65: } - Closes the LOCATIONS dictionary

# Line 67-72: Cache setup for weather data
# Line 71: WEATHER_CACHE = {}
#   - WEATHER_CACHE: Variable name (uppercase = constant)
#   - =: Assignment operator
#   - {}: Empty dictionary (will store cached weather data)
#   - Format: {location_key: (data, timestamp), ...}
WEATHER_CACHE = {}

# Line 72: CACHE_DURATION = 10
#   - CACHE_DURATION: Variable name (uppercase = constant)
#   - =: Assignment operator
#   - 10: Value (seconds to keep data cached)
#   - # 10 seconds in seconds (reduced for real-time feel): Comment explaining the value
CACHE_DURATION = 10  # 10 seconds in seconds (reduced for real-time feel)


# Line 75-132: Function to fetch weather from external API
# Line 75: def get_weather_from_api(lat, lon):
#   - def: Python keyword that defines a function
#   - get_weather_from_api: Function name
#   - (lat, lon): Parameters (values passed when function is called)
#     - lat: Parameter name (latitude)
#     - ,: Separates parameters
#     - lon: Parameter name (longitude)
#   - :: Ends function signature, starts function body
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
    # Line 93: url = "https://api.open-meteo.com/v1/forecast"
    #   - url: Variable name
    #   - =: Assignment operator
    #   - "https://...": String value (the API endpoint URL)
    url = "https://api.open-meteo.com/v1/forecast"
    
    # Line 94-101: params dictionary - query parameters for API request
    # Line 94: params = {
    #   - params: Variable name
    #   - =: Assignment operator
    #   - {: Starts dictionary
    params = {
        # Line 95: "latitude": lat,
        #   - "latitude": Key (API parameter name)
        #   - :: Separates key from value
        #   - lat: Value (uses the function parameter)
        "latitude": lat,
        
        # Line 96: "longitude": lon,
        #   - "longitude": Key (API parameter name)
        #   - :: Separates key from value
        #   - lon: Value (uses the function parameter)
        "longitude": lon,
        
        # Line 97: "current_weather": "true",
        #   - "current_weather": Key (API parameter)
        #   - :: Separates key from value
        #   - "true": Value (string, tells API to include current weather)
        "current_weather": "true",
        
        # Line 100: "hourly": "relativehumidity_2m,pressure_msl"
        #   - "hourly": Key (API parameter)
        #   - :: Separates key from value
        #   - "relativehumidity_2m,pressure_msl": Value (comma-separated list of data types to request)
        "hourly": "relativehumidity_2m,pressure_msl"  # Get humidity and pressure too
    }  # Line 101: } - Closes params dictionary
    
    # Line 103-132: try/except block for error handling
    # Line 103: try:
    #   - try: Python keyword (starts error handling block)
    #   - :: Ends statement, starts try block
    #   - Everything indented here will be attempted
    try:
        # Line 107: response = requests.get(url, params=params, timeout=5)
        #   - response: Variable name (stores the API response)
        #   - =: Assignment operator
        #   - requests: The requests module we imported
        #   - .get: Method that makes HTTP GET request
        #   - (url, params=params, timeout=5): Function arguments
        #     - url: Positional argument (the API URL)
        #     - params=params: Keyword argument (query parameters)
        #     - timeout=5: Keyword argument (max seconds to wait)
        response = requests.get(url, params=params, timeout=5)
        
        # Line 112: response.raise_for_status()
        #   - response: The response object from API call
        #   - .raise_for_status: Method that checks HTTP status code
        #   - (): Calls the method with no arguments
        #   - If status is 400-599 (error), raises an exception
        response.raise_for_status()
        
        # Line 114: data = response.json()
        #   - data: Variable name
        #   - =: Assignment operator
        #   - response: The response object
        #   - .json: Method that parses JSON response
        #   - (): Calls the method (converts JSON string to Python dictionary)
        data = response.json()
        
        # Line 115: logger.info(f"Successfully fetched weather data for lat={lat}, lon={lon}")
        #   - logger: The logger object we created
        #   - .info: Method that logs informational message
        #   - (): Function call
        #   - f"...": f-string (formatted string, allows variables inside {})
        #   - f"Successfully fetched...": Message text
        #   - {lat}: Inserts lat variable value
        #   - {lon}: Inserts lon variable value
        logger.info(f"Successfully fetched weather data for lat={lat}, lon={lon}")
        
        # Line 116: return data
        #   - return: Python keyword (exits function and returns value)
        #   - data: Value to return (the weather data dictionary)
        return data
        
    # Line 118-122: Exception handler for timeout errors
    # Line 118: except requests.exceptions.Timeout:
    #   - except: Python keyword (catches exceptions)
    #   - requests.exceptions.Timeout: Specific exception type (timeout errors)
    #   - :: Ends statement, starts exception handler block
    except requests.exceptions.Timeout:
        # Line 121: logger.error(f"API request timed out for lat={lat}, lon={lon}")
        #   - logger: Logger object
        #   - .error: Method that logs error message
        #   - (): Function call
        #   - f"...": f-string with variables
        logger.error(f"API request timed out for lat={lat}, lon={lon}")
        
        # Line 122: return None
        #   - return: Python keyword
        #   - None: Python's null value (indicates no data/failure)
        return None
        
    # Line 123-127: Exception handler for general request errors
    # Line 123: except requests.exceptions.RequestException as e:
    #   - except: Python keyword
    #   - requests.exceptions.RequestException: General request exception type
    #   - as e: Assigns exception object to variable 'e'
    #   - :: Ends statement, starts handler block
    except requests.exceptions.RequestException as e:
        # Line 126: logger.error(f"API request failed: {str(e)}")
        #   - logger.error: Log error message
        #   - f"...": f-string
        #   - {str(e)}: Converts exception to string and inserts it
        logger.error(f"API request failed: {str(e)}")
        
        # Line 127: return None
        #   - return: Python keyword
        #   - None: Indicates failure
        return None
        
    # Line 128-132: Exception handler for JSON parsing errors
    # Line 128: except ValueError as e:
    #   - except: Python keyword
    #   - ValueError: Exception type (raised when JSON parsing fails)
    #   - as e: Assigns exception to variable 'e'
    except ValueError as e:
        # Line 131: logger.error(f"Failed to parse JSON response: {str(e)}")
        #   - logger.error: Log error
        #   - f"...": f-string with error message
        logger.error(f"Failed to parse JSON response: {str(e)}")
        
        # Line 132: return None
        #   - return: Python keyword
        #   - None: Indicates failure
        return None


# Line 135-158: Function to get cached weather data
# Line 135: def get_cached_weather(location_key):
#   - def: Python keyword (defines function)
#   - get_cached_weather: Function name
#   - (location_key): Parameter (the location identifier)
#   - :: Ends signature, starts body
def get_cached_weather(location_key):
    """
    LESSON: Caching Strategy
    -------------------------
    Caching stores frequently accessed data in memory to avoid repeated API calls.
    This improves performance and reduces load on external services.
    
    Returns:
        dict or None: Cached weather data if valid, None if cache expired or missing
    """
    # Line 145: if location_key in WEATHER_CACHE:
    #   - if: Python keyword (starts conditional)
    #   - location_key: Variable (the location identifier)
    #   - in: Python keyword (checks if value exists in container)
    #   - WEATHER_CACHE: The cache dictionary
    #   - :: Ends condition, starts if block
    if location_key in WEATHER_CACHE:
        # Line 146: data, timestamp = WEATHER_CACHE[location_key]
        #   - data, timestamp: Two variables (tuple unpacking)
        #   - =: Assignment operator
        #   - WEATHER_CACHE: Cache dictionary
        #   - [location_key]: Dictionary lookup (gets value for this key)
        #   - The value is a tuple (data, timestamp), so we unpack it
        data, timestamp = WEATHER_CACHE[location_key]
        
        # Line 150: if time() - timestamp < CACHE_DURATION:
        #   - if: Python keyword
        #   - time(): Function call (gets current Unix timestamp in seconds)
        #   - -: Subtraction operator
        #   - timestamp: Variable (when data was cached)
        #   - <: Less than operator
        #   - CACHE_DURATION: Constant (10 seconds)
        #   - :: Ends condition, starts if block
        #   - This checks if cache is still fresh (less than 10 seconds old)
        if time() - timestamp < CACHE_DURATION:
            # Line 151: logger.info(f"Returning cached weather data for {location_key}")
            #   - logger.info: Log informational message
            #   - f"...": f-string with variable
            logger.info(f"Returning cached weather data for {location_key}")
            
            # Line 152: return data
            #   - return: Python keyword
            #   - data: Cached weather data to return
            return data
        else:
            # Line 155: del WEATHER_CACHE[location_key]
            #   - del: Python keyword (deletes item)
            #   - WEATHER_CACHE: Cache dictionary
            #   - [location_key]: Dictionary key to delete
            #   - Removes expired cache entry
            del WEATHER_CACHE[location_key]
            
            # Line 156: logger.info(f"Cache expired for {location_key}")
            #   - logger.info: Log message
            logger.info(f"Cache expired for {location_key}")
    
    # Line 158: return None
    #   - return: Python keyword
    #   - None: No cached data available
    return None


# Line 161-168: Function to store data in cache
# Line 161: def set_cached_weather(location_key, data):
#   - def: Python keyword
#   - set_cached_weather: Function name
#   - (location_key, data): Two parameters
#   - :: Ends signature, starts body
def set_cached_weather(location_key, data):
    """
    LESSON: Storing data in cache
    ------------------------------
    We store the data along with a timestamp so we know when it was cached.
    """
    # Line 167: WEATHER_CACHE[location_key] = (data, time())
    #   - WEATHER_CACHE: Cache dictionary
    #   - [location_key]: Dictionary key (location identifier)
    #   - =: Assignment operator
    #   - (data, time()): Tuple (two values stored together)
    #     - data: Weather data to cache
    #     - time(): Current timestamp (when cached)
    #   - This stores both the data and when it was cached
    WEATHER_CACHE[location_key] = (data, time())
    
    # Line 168: logger.info(f"Cached weather data for {location_key}")
    #   - logger.info: Log message
    #   - f"...": f-string
    logger.info(f"Cached weather data for {location_key}")


# Line 171-181: Homepage route
# Line 173: @app.route('/')
#   - @: Decorator syntax (modifies function below)
#   - app: Flask application instance
#   - .route: Method that creates URL route
#   - ('/'): Route path (forward slash = homepage/root URL)
#   - When user visits http://localhost:5000/, this function runs
@app.route('/')
def home():
    """
    LESSON: Route Handler Function
    -------------------------------
    This function handles requests to the homepage.
    It renders an HTML template and returns it to the browser.
    """
    # Line 181: return render_template('index.html')
    #   - return: Python keyword (sends response to browser)
    #   - render_template: Flask function (loads and processes HTML template)
    #   - ('index.html'): Template file name (in templates/ folder)
    #   - This finds templates/index.html, processes it, returns HTML to browser
    return render_template('index.html')


# Line 184-194: Wiki page route
# Line 186: @app.route('/wiki')
#   - @app.route: Decorator (creates route)
#   - ('/wiki'): Route path (when user visits /wiki, this runs)
@app.route('/wiki')
def wiki():
    """
    LESSON: Wiki Page Route
    ------------------------
    This function handles requests to the /wiki URL.
    It renders the wiki.html template.
    """
    # Line 194: return render_template('wiki.html')
    #   - return: Sends response
    #   - render_template: Flask function
    #   - ('wiki.html'): Template file (templates/wiki.html)
    return render_template('wiki.html')


# Line 197-211: Dynamic character page route
# Line 200: @app.route('/character/<character_name>')
#   - @app.route: Decorator
#   - ('/character/<character_name>'): Route with parameter
#     - /character/: Base path
#     - <character_name>: URL parameter (captures part of URL)
#     - Example: /character/jake → character_name = 'jake'
#     - Example: /character/neytiri → character_name = 'neytiri'
#   - This ONE route handles ALL character pages!
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
    # Line 211: return render_template('character.html', character_name=character_name)
    #   - return: Sends response
    #   - render_template: Flask function
    #   - ('character.html'): Template file name
    #   - character_name=character_name: Passes variable to template
    #     - First character_name: Variable name in template ({{ character_name }})
    #     - Second character_name: Value from function parameter (from URL)
    #   - Template can now use {{ character_name }} and it will be replaced with actual value
    return render_template('character.html', character_name=character_name)


# Line 214-293: Weather API endpoint route
# Line 217: @app.route('/get_weather/<location_key>')
#   - @app.route: Decorator
#   - ('/get_weather/<location_key>'): Route with parameter
#     - /get_weather/: Base path
#     - <location_key>: URL parameter (captures location identifier)
#     - Example: /get_weather/hallelujah_mountains → location_key = 'hallelujah_mountains'
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
    # Line 234: if location_key not in LOCATIONS:
    #   - if: Python keyword
    #   - location_key: Parameter from URL
    #   - not in: Python keyword (checks if value NOT in container)
    #   - LOCATIONS: Dictionary of valid locations
    #   - :: Ends condition, starts if block
    #   - This validates the location exists
    if location_key not in LOCATIONS:
        # Line 235: logger.warning(f"Invalid location key requested: {location_key}")
        #   - logger.warning: Log warning message
        logger.warning(f"Invalid location key requested: {location_key}")
        
        # Line 236-239: return jsonify({...}), 404
        #   - return: Sends response
        #   - jsonify: Flask function (converts dict to JSON)
        #   - ({...}): Dictionary with error info
        #   - , 404: HTTP status code (404 = Not Found)
        return jsonify({
            "error": "Invalid location",
            "message": f"Location '{location_key}' not found"
        }), 404  # 404 = Not Found HTTP status code
    
    # Line 241: target = LOCATIONS[location_key]
    #   - target: Variable name
    #   - =: Assignment
    #   - LOCATIONS: Dictionary
    #   - [location_key]: Dictionary lookup (gets location data)
    target = LOCATIONS[location_key]
    
    # Line 242: logger.info(f"Processing weather request for {target['name']}")
    #   - logger.info: Log message
    #   - target['name']: Gets 'name' value from location dictionary
    logger.info(f"Processing weather request for {target['name']}")
    
    # Line 245: cached_data = get_cached_weather(location_key)
    #   - cached_data: Variable name
    #   - =: Assignment
    #   - get_cached_weather: Function we defined earlier
    #   - (location_key): Argument (location identifier)
    cached_data = get_cached_weather(location_key)
    
    # Line 246-247: if cached_data:
    #   - if: Python keyword
    #   - cached_data: Variable (will be dict if found, None if not)
    #   - In Python, non-empty dict is "truthy", None is "falsy"
    #   - :: Ends condition, starts if block
    if cached_data:
        # Line 247: return jsonify(cached_data)
        #   - return: Sends response
        #   - jsonify: Converts dict to JSON
        #   - cached_data: The cached weather data
        return jsonify(cached_data)
    
    # Line 250: api_data = get_weather_from_api(target['lat'], target['lon'])
    #   - api_data: Variable name
    #   - =: Assignment
    #   - get_weather_from_api: Function we defined
    #   - (target['lat'], target['lon']): Arguments (latitude and longitude)
    api_data = get_weather_from_api(target['lat'], target['lon'])
    
    # Line 252-259: if api_data is None:
    #   - if: Python keyword
    #   - api_data: Variable
    #   - is None: Checks if value is exactly None (API call failed)
    #   - :: Ends condition, starts if block
    if api_data is None:
        # Line 255-259: return jsonify({...}), 500
        #   - return: Sends error response
        #   - jsonify: Converts to JSON
        #   - {...}: Error dictionary
        #   - , 500: HTTP status code (500 = Internal Server Error)
        return jsonify({
            "error": "Weather service unavailable",
            "message": "Failed to fetch weather data. Please try again later.",
            "location": target['name']
        }), 500
    
    # Line 263: current_weather = api_data.get('current_weather', {})
    #   - current_weather: Variable name
    #   - =: Assignment
    #   - api_data: Dictionary from API
    #   - .get: Dictionary method (safely gets value)
    #   - ('current_weather', {}): Arguments
    #     - 'current_weather': Key to look up
    #     - {}: Default value if key doesn't exist (empty dict)
    current_weather = api_data.get('current_weather', {})
    
    # Line 268: hourly_data = api_data.get('hourly', {})
    #   - hourly_data: Variable name
    #   - =: Assignment
    #   - api_data.get: Safely gets 'hourly' key
    #   - ('hourly', {}): Key and default value
    hourly_data = api_data.get('hourly', {})
    
    # Line 272: humidity = hourly_data.get('relativehumidity_2m', [None])[0] if hourly_data.get('relativehumidity_2m') else None
    #   - humidity: Variable name
    #   - =: Assignment
    #   - hourly_data.get('relativehumidity_2m', [None]): Gets humidity array, default [None]
    #   - [0]: Gets first element of array
    #   - if hourly_data.get('relativehumidity_2m'): Only if array exists
    #   - else None: Otherwise None
    #   - This safely gets first humidity value if it exists
    humidity = hourly_data.get('relativehumidity_2m', [None])[0] if hourly_data.get('relativehumidity_2m') else None
    
    # Line 273: pressure = hourly_data.get('pressure_msl', [None])[0] if hourly_data.get('pressure_msl') else None
    #   - Same pattern as humidity, but for pressure data
    pressure = hourly_data.get('pressure_msl', [None])[0] if hourly_data.get('pressure_msl') else None
    
    # Line 277-288: response_data dictionary - structure data for frontend
    # Line 277: response_data = {
    #   - response_data: Variable name
    #   - =: Assignment
    #   - {: Starts dictionary
    response_data = {
        # Line 278: "location": target['name'],
        #   - "location": Key
        #   - :: Separates key from value
        #   - target['name']: Gets name from location dictionary
        "location": target['name'],
        
        # Line 279: "temp": current_weather.get('temperature'),
        #   - "temp": Key
        #   - current_weather.get('temperature'): Safely gets temperature
        "temp": current_weather.get('temperature'),
        
        # Line 280: "wind": current_weather.get('windspeed'),
        #   - "wind": Key
        #   - current_weather.get('windspeed'): Gets wind speed
        "wind": current_weather.get('windspeed'),
        
        # Line 281: "wind_direction": current_weather.get('winddirection'),
        #   - "wind_direction": Key
        #   - current_weather.get('winddirection'): Gets wind direction in degrees
        "wind_direction": current_weather.get('winddirection'),
        
        # Line 282: "weather_code": current_weather.get('weathercode'),
        #   - "weather_code": Key
        #   - current_weather.get('weathercode'): Gets weather condition code
        "weather_code": current_weather.get('weathercode'),
        
        # Line 283: "humidity": humidity,
        #   - "humidity": Key
        #   - humidity: Variable we calculated earlier
        "humidity": humidity,
        
        # Line 284: "pressure": round(pressure, 2) if pressure else None,
        #   - "pressure": Key
        #   - round(pressure, 2): Rounds pressure to 2 decimal places
        #   - if pressure: Only if pressure exists
        #   - else None: Otherwise None
        "pressure": round(pressure, 2) if pressure else None,
        
        # Line 285: "image": target['image'],
        #   - "image": Key
        #   - target['image']: Gets image URL from location data
        "image": target['image'],
        
        # Line 286: "status": target['status'],
        #   - "status": Key
        #   - target['status']: Gets status text
        "status": target['status'],
        
        # Line 287: "status_color": target['status_color']
        #   - "status_color": Key
        #   - target['status_color']: Gets status color
        "status_color": target['status_color']
    }  # Line 288: } - Closes response_data dictionary
    
    # Line 291: set_cached_weather(location_key, response_data)
    #   - set_cached_weather: Function we defined
    #   - (location_key, response_data): Arguments
    #     - location_key: Where to store it
    #     - response_data: What to store
    set_cached_weather(location_key, response_data)
    
    # Line 293: return jsonify(response_data)
    #   - return: Sends response
    #   - jsonify: Converts dict to JSON
    #   - response_data: The weather data dictionary
    return jsonify(response_data)


# Line 296-305: Server startup code
# Line 299: if __name__ == '__main__':
#   - if: Python keyword
#   - __name__: Special Python variable
#   - ==: Equality operator
#   - '__main__': String value (only true when script runs directly)
#   - :: Ends condition, starts if block
#   - This code only runs when you run the file directly (not when imported)
if __name__ == '__main__':
    # Line 300: logger.info("Starting Pandora Weather Scanner server...")
    #   - logger.info: Log message
    #   - ("..."): Message string
    logger.info("Starting Pandora Weather Scanner server...")
    
    # Line 305: app.run(debug=True, host='0.0.0.0', port=5000)
    #   - app: Flask application instance
    #   - .run: Method that starts the web server
    #   - (debug=True, host='0.0.0.0', port=5000): Arguments
    #     - debug=True: Auto-reloads on code changes, shows detailed errors
    #     - host='0.0.0.0': Makes server accessible from other devices on network
    #     - port=5000: Port number (default is 5000)
    #   - This starts the web server and makes it listen for requests
    app.run(debug=True, host='0.0.0.0', port=5000)
