# Code Comments Documentation

This document contains all comments extracted from the code files in this project.

## pandoraproject.py

### Module-level Documentation
```
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
```

### Import Comments
```
# Line 25: from flask import Flask, jsonify, render_template
#   - from: Python keyword that imports from a module
#   - flask: The Flask web framework module
#   - import: Python keyword to bring in functionality
#   - Flask: The main Flask class (creates web application instances)
#   - jsonify: Function that converts Python dictionaries to JSON format (for API responses)
#   - render_template: Function that takes HTML template files and fills in variables

# Line 26: import requests
#   - import: Python keyword
#   - requests: Third-party library for making HTTP requests (calling external APIs)
#   - This allows us to fetch data from the weather API

# Line 27: import logging
#   - import: Python keyword
#   - logging: Built-in Python module for recording events (debugging, errors, info)
#   - This lets us write messages to the console/terminal

# Line 28: from time import time
#   - from: Python keyword
#   - time: Built-in Python module for time-related functions
#   - import: Python keyword
#   - time: The time() function (returns current Unix timestamp)
#   - We use this to track when data was cached

# Line 29: from functools import lru_cache
#   - from: Python keyword
#   - functools: Built-in Python module with function tools
#   - import: Python keyword
#   - lru_cache: Function decorator for caching (we import it but don't use it currently)
```

### Flask App Initialization
```
# Line 31-34: Initialize Flask application
# Line 34: app = Flask(__name__)
#   - app: Variable name (we'll use this to define routes)
#   - =: Assignment operator (stores value in variable)
#   - Flask: The Flask class we imported
#   - (__name__): Passes the current module name to Flask
#     - __name__: Special Python variable that is '__main__' when script runs directly
#     - When imported, __name__ is the module name
#   - Flask uses __name__ to find templates and static files automatically
```

### Logging Configuration
```
# Line 36-43: Configure logging system
# Line 39-42: logging.basicConfig(...)
#   - logging: The logging module we imported
#   - .basicConfig: Function that sets up logging configuration
#   - (): Function call with parameters inside
#   - level=logging.INFO: Sets minimum log level to INFO (shows INFO, WARNING, ERROR, CRITICAL)
#   - format=...: Defines how log messages look (timestamp, name, level, message)

# Line 43: logger = logging.getLogger(__name__)
#   - logger: Variable name for our logger object
#   - =: Assignment operator
#   - logging: The logging module
#   - .getLogger: Function that creates/gets a logger instance
#   - (__name__): Passes module name (creates logger named after this file)
#   - We'll use logger.info(), logger.error(), etc. to write log messages
```

### LOCATIONS Dictionary Comments
```
# Line 45-65: LOCATIONS dictionary - stores location data
# Line 48: LOCATIONS = {
#   - LOCATIONS: Variable name (uppercase = constant, shouldn't change)
#   - =: Assignment operator
#   - {: Starts a dictionary (key-value pairs)
#   - This is a nested dictionary: dictionary inside a dictionary

# Line 49: "hallelujah_mountains": {
#   - "hallelujah_mountains": Dictionary key (string, used to look up this location)
#   - :: Separates key from value
#   - {: Starts another dictionary (the value for this key)

# Line 50: "name": "Hallelujah Mountains",
#   - "name": Key in inner dictionary
#   - :: Separates key from value
#   - "Hallelujah Mountains": Value (display name)
#   - ,: Separates dictionary entries

# Line 51: "lat": 29.13,
#   - "lat": Key (latitude)
#   - :: Separates key from value
#   - 29.13: Value (latitude coordinate, float number)

# Line 52: "lon": 110.48,
#   - "lon": Key (longitude)
#   - :: Separates key from value
#   - 110.48: Value (longitude coordinate, float number)

# Line 53: "image": "https://...",
#   - "image": Key
#   - :: Separates key from value
#   - "https://...": Value (URL to image)

# Line 54: "status": "Stable",
#   - "status": Key
#   - :: Separates key from value
#   - "Stable": Value (status text)

# Line 55: "status_color": "green"
#   - "status_color": Key
#   - :: Separates key from value
#   - "green": Value (CSS color name)

# Line 56: }, - Closes the inner dictionary, comma separates from next entry

# Line 57-64: Second location entry (same structure as above)

# Line 65: } - Closes the LOCATIONS dictionary
```

### Character Data Comments
```
# Character data dictionary - stores character information
# This makes it easy to modify pictures and descriptions for each character
```

### Cache Setup Comments
```
# Line 67-72: Cache setup for weather data
# Line 71: WEATHER_CACHE = {}
#   - WEATHER_CACHE: Variable name (uppercase = constant)
#   - =: Assignment operator
#   - {}: Empty dictionary (will store cached weather data)
#   - Format: {location_key: (data, timestamp), ...}

# Line 72: CACHE_DURATION = 10
#   - CACHE_DURATION: Variable name (uppercase = constant)
#   - =: Assignment operator
#   - 10: Value (seconds to keep data cached)
#   - # 10 seconds in seconds (reduced for real-time feel): Comment explaining the value
```

### Function Comments
```
# Line 75-132: Function to fetch weather from external API
# Line 75: def get_weather_from_api(lat, lon):
#   - def: Python keyword that defines a function
#   - get_weather_from_api: Function name
#   - (lat, lon): Parameters (values passed when function is called)
#     - lat: Parameter name (latitude)
#     - ,: Separates parameters
#     - lon: Parameter name (longitude)
#   - :: Ends function signature, starts function body

# Line 93: url = "https://api.open-meteo.com/v1/forecast"
#   - url: Variable name
#   - =: Assignment operator
#   - "https://...": String value (the API endpoint URL)

# Line 94-101: params dictionary - query parameters for API request
# Line 94: params = {
#   - params: Variable name
#   - =: Assignment operator
#   - {: Starts dictionary

# Line 95: "latitude": lat,
#   - "latitude": Key (API parameter name)
#   - :: Separates key from value
#   - lat: Value (uses the function parameter)

# Line 96: "longitude": lon,
#   - "longitude": Key (API parameter name)
#   - :: Separates key from value
#   - lon: Value (uses the function parameter)

# Line 97: "current_weather": "true",
#   - "current_weather": Key (API parameter)
#   - :: Separates key from value
#   - "true": Value (string, tells API to include current weather)

# Line 100: "hourly": "relativehumidity_2m,pressure_msl"
#   - "hourly": Key (API parameter)
#   - :: Separates key from value
#   - "relativehumidity_2m,pressure_msl": Value (comma-separated list of data types to request)

# Line 101: } - Closes params dictionary

# Line 103-132: try/except block for error handling
# Line 103: try:
#   - try: Python keyword (starts error handling block)
#   - :: Ends statement, starts try block
#   - Everything indented here will be attempted

# Line 107: response = requests.get(url, params=params, timeout=5)
#   - response: Variable name (stores the API response)
#   - =: Assignment operator
#   - requests: The requests module we imported
#   - .get: Method that makes HTTP GET request
#   - (url, params=params, timeout=5): Function arguments
#     - url: Positional argument (the API URL)
#     - params=params: Keyword argument (query parameters)
#     - timeout=5: Keyword argument (max seconds to wait)

# Line 112: response.raise_for_status()
#   - response: The response object from API call
#   - .raise_for_status: Method that checks HTTP status code
#   - (): Calls the method with no arguments
#   - If status is 400-599 (error), raises an exception

# Line 114: data = response.json()
#   - data: Variable name
#   - =: Assignment operator
#   - response: The response object
#   - .json: Method that parses JSON response
#   - (): Calls the method (converts JSON string to Python dictionary)

# Line 115: logger.info(f"Successfully fetched weather data for lat={lat}, lon={lon}")
#   - logger: The logger object we created
#   - .info: Method that logs informational message
#   - (): Function call
#   - f"...": f-string (formatted string, allows variables inside {})
#   - f"Successfully fetched...": Message text
#   - {lat}: Inserts lat variable value
#   - {lon}: Inserts lon variable value

# Line 116: return data
#   - return: Python keyword (exits function and returns value)
#   - data: Value to return (the weather data dictionary)

# Line 118-122: Exception handler for timeout errors
# Line 118: except requests.exceptions.Timeout:
#   - except: Python keyword (catches exceptions)
#   - requests.exceptions.Timeout: Specific exception type (timeout errors)
#   - :: Ends statement, starts exception handler block

# Line 121: logger.error(f"API request timed out for lat={lat}, lon={lon}")
#   - logger: Logger object
#   - .error: Method that logs error message
#   - (): Function call
#   - f"...": f-string with variables

# Line 122: return None
#   - return: Python keyword
#   - None: Python's null value (indicates no data/failure)

# Line 123-127: Exception handler for general request errors
# Line 123: except requests.exceptions.RequestException as e:
#   - except: Python keyword
#   - requests.exceptions.RequestException: General request exception type
#   - as e: Assigns exception object to variable 'e'
#   - :: Ends statement, starts handler block

# Line 126: logger.error(f"API request failed: {str(e)}")
#   - logger.error: Log error message
#   - f"...": f-string
#   - {str(e)}: Converts exception to string and inserts it

# Line 127: return None
#   - return: Python keyword
#   - None: Indicates failure

# Line 128-132: Exception handler for JSON parsing errors
# Line 128: except ValueError as e:
#   - except: Python keyword
#   - ValueError: Exception type (raised when JSON parsing fails)
#   - as e: Assigns exception to variable 'e'

# Line 131: logger.error(f"Failed to parse JSON response: {str(e)}")
#   - logger.error: Log error
#   - f"...": f-string with error message

# Line 132: return None
#   - return: Python keyword
#   - None: Indicates failure

# Line 135-158: Function to get cached weather data
# Line 135: def get_cached_weather(location_key):
#   - def: Python keyword (defines function)
#   - get_cached_weather: Function name
#   - (location_key): Parameter (the location identifier)
#   - :: Ends signature, starts body

# Line 145: if location_key in WEATHER_CACHE:
#   - if: Python keyword (starts conditional)
#   - location_key: Variable (the location identifier)
#   - in: Python keyword (checks if value exists in container)
#   - WEATHER_CACHE: The cache dictionary
#   - :: Ends condition, starts if block

# Line 146: data, timestamp = WEATHER_CACHE[location_key]
#   - data, timestamp: Two variables (tuple unpacking)
#   - =: Assignment operator
#   - WEATHER_CACHE: Cache dictionary
#   - [location_key]: Dictionary lookup (gets value for this key)
#   - The value is a tuple (data, timestamp), so we unpack it

# Line 150: if time() - timestamp < CACHE_DURATION:
#   - if: Python keyword
#   - time(): Function call (gets current Unix timestamp in seconds)
#   - -: Subtraction operator
#   - timestamp: Variable (when data was cached)
#   - <: Less than operator
#   - CACHE_DURATION: Constant (10 seconds)
#   - :: Ends condition, starts if block
#   - This checks if cache is still fresh (less than 10 seconds old)

# Line 151: logger.info(f"Returning cached weather data for {location_key}")
#   - logger.info: Log informational message
#   - f"...": f-string with variable

# Line 152: return data
#   - return: Python keyword
#   - data: Cached weather data to return

# Line 155: del WEATHER_CACHE[location_key]
#   - del: Python keyword (deletes item)
#   - WEATHER_CACHE: Cache dictionary
#   - [location_key]: Dictionary key to delete
#   - Removes expired cache entry

# Line 156: logger.info(f"Cache expired for {location_key}")
#   - logger.info: Log message

# Line 158: return None
#   - return: Python keyword
#   - None: No cached data available

# Line 161-168: Function to store data in cache
# Line 161: def set_cached_weather(location_key, data):
#   - def: Python keyword
#   - set_cached_weather: Function name
#   - (location_key, data): Two parameters
#   - :: Ends signature, starts body

# Line 167: WEATHER_CACHE[location_key] = (data, time())
#   - WEATHER_CACHE: Cache dictionary
#   - [location_key]: Dictionary key (location identifier)
#   - =: Assignment operator
#   - (data, time()): Tuple (two values stored together)
#     - data: Weather data to cache
#     - time(): Current timestamp (when cached)
#   - This stores both the data and when it was cached

# Line 168: logger.info(f"Cached weather data for {location_key}")
#   - logger.info: Log message
#   - f"...": f-string

# Line 171-181: Homepage route
# Line 173: @app.route('/')
#   - @: Decorator syntax (modifies function below)
#   - app: Flask application instance
#   - .route: Method that creates URL route
#   - ('/'): Route path (forward slash = homepage/root URL)
#   - When user visits http://localhost:5000/, this function runs

# Line 181: return render_template('index.html')
#   - return: Python keyword (sends response to browser)
#   - render_template: Flask function (loads and processes HTML template)
#   - ('index.html'): Template file name (in templates/ folder)
#   - This finds templates/index.html, processes it, returns HTML to browser

# Line 184-194: Wiki page route
# Line 186: @app.route('/wiki')
#   - @app.route: Decorator (creates route)
#   - ('/wiki'): Route path (when user visits /wiki, this runs)

# Line 194: return render_template('wiki.html')
#   - return: Sends response
#   - render_template: Flask function
#   - ('wiki.html'): Template file (templates/wiki.html)

# Line 197-211: Dynamic character page route
# Line 200: @app.route('/character/<character_name>')
#   - @app.route: Decorator
#   - ('/character/<character_name>'): Route with parameter
#     - /character/: Base path
#     - <character_name>: URL parameter (captures part of URL)
#     - Example: /character/jake → character_name = 'jake'
#     - Example: /character/neytiri → character_name = 'neytiri'
#   - This ONE route handles ALL character pages!

# Line 211: return render_template('character.html', character_name=character_name)
#   - return: Sends response
#   - render_template: Flask function
#   - ('character.html'): Template file name
#   - character_name=character_name: Passes variable to template
#     - First character_name: Variable name in template ({{ character_name }})
#     - Second character_name: Value from function parameter (from URL)
#   - Template can now use {{ character_name }} and it will be replaced with actual value
#   - character_data=character_data: Passes character data (image, description, stats)

# Line 214-293: Weather API endpoint route
# Line 217: @app.route('/get_weather/<location_key>')
#   - @app.route: Decorator
#   - ('/get_weather/<location_key>'): Route with parameter
#     - /get_weather/: Base path
#     - <location_key>: URL parameter (captures location identifier)
#     - Example: /get_weather/hallelujah_mountains → location_key = 'hallelujah_mountains'

# Line 234: if location_key not in LOCATIONS:
#   - if: Python keyword
#   - location_key: Parameter from URL
#   - not in: Python keyword (checks if value NOT in container)
#   - LOCATIONS: Dictionary of valid locations
#   - :: Ends condition, starts if block
#   - This validates the location exists

# Line 235: logger.warning(f"Invalid location key requested: {location_key}")
#   - logger.warning: Log warning message

# Line 236-239: return jsonify({...}), 404
#   - return: Sends response
#   - jsonify: Flask function (converts dict to JSON)
#   - ({...}): Dictionary with error info
#   - , 404: HTTP status code (404 = Not Found)

# Line 241: target = LOCATIONS[location_key]
#   - target: Variable name
#   - =: Assignment
#   - LOCATIONS: Dictionary
#   - [location_key]: Dictionary lookup (gets location data)

# Line 242: logger.info(f"Processing weather request for {target['name']}")
#   - logger.info: Log message
#   - target['name']: Gets 'name' value from location dictionary

# Line 245: cached_data = get_cached_weather(location_key)
#   - cached_data: Variable name
#   - =: Assignment
#   - get_cached_weather: Function we defined earlier
#   - (location_key): Argument (location identifier)

# Line 246-247: if cached_data:
#   - if: Python keyword
#   - cached_data: Variable (will be dict if found, None if not)
#   - In Python, non-empty dict is "truthy", None is "falsy"
#   - :: Ends condition, starts if block

# Line 247: return jsonify(cached_data)
#   - return: Sends response
#   - jsonify: Converts dict to JSON
#   - cached_data: The cached weather data

# Line 250: api_data = get_weather_from_api(target['lat'], target['lon'])
#   - api_data: Variable name
#   - =: Assignment
#   - get_weather_from_api: Function we defined
#   - (target['lat'], target['lon']): Arguments (latitude and longitude)

# Line 252-259: if api_data is None:
#   - if: Python keyword
#   - api_data: Variable
#   - is None: Checks if value is exactly None (API call failed)
#   - :: Ends condition, starts if block

# Line 255-259: return jsonify({...}), 500
#   - return: Sends error response
#   - jsonify: Converts to JSON
#   - {...}: Error dictionary
#   - , 500: HTTP status code (500 = Internal Server Error)

# Line 263: current_weather = api_data.get('current_weather', {})
#   - current_weather: Variable name
#   - =: Assignment
#   - api_data: Dictionary from API
#   - .get: Dictionary method (safely gets value)
#   - ('current_weather', {}): Arguments
#     - 'current_weather': Key to look up
#     - {}: Default value if key doesn't exist (empty dict)

# Line 268: hourly_data = api_data.get('hourly', {})
#   - hourly_data: Variable name
#   - =: Assignment
#   - api_data.get: Safely gets 'hourly' key
#   - ('hourly', {}): Key and default value

# Line 272: humidity = hourly_data.get('relativehumidity_2m', [None])[0] if hourly_data.get('relativehumidity_2m') else None
#   - humidity: Variable name
#   - =: Assignment
#   - hourly_data.get('relativehumidity_2m', [None]): Gets humidity array, default [None]
#   - [0]: Gets first element of array
#   - if hourly_data.get('relativehumidity_2m'): Only if array exists
#   - else None: Otherwise None
#   - This safely gets first humidity value if it exists

# Line 273: pressure = hourly_data.get('pressure_msl', [None])[0] if hourly_data.get('pressure_msl') else None
#   - Same pattern as humidity, but for pressure data

# Line 277-288: response_data dictionary - structure data for frontend
# Line 277: response_data = {
#   - response_data: Variable name
#   - =: Assignment
#   - {: Starts dictionary

# Line 278: "location": target['name'],
#   - "location": Key
#   - :: Separates key from value
#   - target['name']: Gets name from location dictionary

# Line 279: "temp": current_weather.get('temperature'),
#   - "temp": Key
#   - current_weather.get('temperature'): Safely gets temperature

# Line 280: "wind": current_weather.get('windspeed'),
#   - "wind": Key
#   - current_weather.get('windspeed'): Gets wind speed

# Line 281: "wind_direction": current_weather.get('winddirection'),
#   - "wind_direction": Key
#   - current_weather.get('winddirection'): Gets wind direction in degrees

# Line 282: "weather_code": current_weather.get('weathercode'),
#   - "weather_code": Key
#   - current_weather.get('weathercode'): Gets weather condition code

# Line 283: "humidity": humidity,
#   - "humidity": Key
#   - humidity: Variable we calculated earlier

# Line 284: "pressure": round(pressure, 2) if pressure else None,
#   - "pressure": Key
#   - round(pressure, 2): Rounds pressure to 2 decimal places
#   - if pressure: Only if pressure exists
#   - else None: Otherwise None

# Line 285: "image": target['image'],
#   - "image": Key
#   - target['image']: Gets image URL from location data

# Line 286: "status": target['status'],
#   - "status": Key
#   - target['status']: Gets status text

# Line 287: "status_color": target['status_color']
#   - "status_color": Key
#   - target['status_color']: Gets status color

# Line 288: } - Closes response_data dictionary

# Line 291: set_cached_weather(location_key, response_data)
#   - set_cached_weather: Function we defined
#   - (location_key, response_data): Arguments
#     - location_key: Where to store it
#     - response_data: What to store

# Line 293: return jsonify(response_data)
#   - return: Sends response
#   - jsonify: Converts dict to JSON
#   - response_data: The weather data dictionary

# Line 296-305: Server startup code
# Line 299: if __name__ == '__main__':
#   - if: Python keyword
#   - __name__: Special Python variable
#   - ==: Equality operator
#   - '__main__': String value (only true when script runs directly)
#   - :: Ends condition, starts if block
#   - This code only runs when you run the file directly (not when imported)

# Line 300: logger.info("Starting Pandora Weather Scanner server...")
#   - logger.info: Log message
#   - ("..."): Message string

# Line 305: app.run(debug=True, host='0.0.0.0', port=5000)
#   - app: Flask application instance
#   - .run: Method that starts the web server
#   - (debug=True, host='0.0.0.0', port=5000): Arguments
#     - debug=True: Auto-reloads on code changes, shows detailed errors
#     - host='0.0.0.0': Makes server accessible from other devices on network
#     - port=5000: Port number (default is 5000)
#   - This starts the web server and makes it listen for requests
```

## templates/character.html

### HTML Structure Comments
```
<!--
LESSON: HTML Document Type Declaration
=======================================
Line 1: <!DOCTYPE html>
  - <!DOCTYPE: HTML declaration tag (not a regular HTML tag)
  - html: Specifies HTML5 document type
  - This tells the browser "this is an HTML5 document"
  - Must be the FIRST line of every HTML file
-->

<!--
LESSON: HTML Root Element
=========================
Line 2: <html>
  - <html>: Root element (contains entire HTML document)
  - All other HTML elements go inside this
  - lang attribute could be added: <html lang="en">
-->

<!--
LESSON: HTML Head Section
=========================
Line 3: <head>
  - <head>: Container for metadata (not visible on page)
  - Contains: title, styles, scripts, meta tags
  - This section is processed by browser but not displayed
-->

<!--
LESSON: Page Title
=================
Line 4: <title>RDA Wiki - Character</title>
  - <title>: Sets browser tab title
  - "RDA Wiki - Character": Text shown in browser tab
  - Not visible on the page itself, only in tab
-->

<!--
LESSON: CSS Styles Section
=========================
Line 5: <style>
  - <style>: Tag that contains CSS code
  - CSS (Cascading Style Sheets) controls how elements look
  - All styles between <style> and </style> apply to this page
-->
```

### CSS Comments
```
/* Line 6-13: Body Element Styling */
/* body: CSS selector (targets <body> HTML element) */

/* Line 7: background-color: black; */
/*   - background-color: CSS property (sets background color) */
/*   - black: Color value (makes background black) */
/*   - ;: Ends CSS declaration */

/* Line 8: color: #0b500b; */
/*   - color: CSS property (sets text color) */
/*   - #0b500b: Hex color code (dark green) */

/* Line 9: font-family: monospace; */
/*   - font-family: CSS property (sets font) */
/*   - monospace: Font name (all characters same width, like code) */

/* Line 10: text-align: center; */
/*   - text-align: CSS property (horizontal alignment) */
/*   - center: Value (centers text horizontally) */

/* Line 11: margin-top: 50px; */
/*   - margin-top: CSS property (space above element) */
/*   - 50px: Value (50 pixels of space) */

/* Line 12: padding: 20px; */
/*   - padding: CSS property (space inside element) */
/*   - 20px: Value (20 pixels of space on all sides) */

/* Line 15-17: Navigation Styling */
/* nav: CSS selector (targets <nav> HTML element) */

/* Line 16: margin-bottom: 30px; */
/*   - margin-bottom: Space below navigation */

/* Line 19-26: Navigation Link Styling */
/* nav a: CSS selector (targets <a> tags inside <nav>) */
/*   - nav: Parent selector */
/*   - (space): Means "inside" or "descendant of" */
/*   - a: Child selector (anchor/link tags) */

/* Line 20: color: #00ff00; */
/*   - color: Text color */
/*   - #00ff00: Hex color (bright green) */

/* Line 21: text-decoration: none; */
/*   - text-decoration: Controls underline, etc. */
/*   - none: Removes default underline from links */

/* Line 22: padding: 10px 20px; */
/*   - padding: Space inside element */
/*   - 10px 20px: 10px top/bottom, 20px left/right */

/* Line 23: border: 2px solid #00ff00; */
/*   - border: Creates border around element */
/*   - 2px: Border width (2 pixels) */
/*   - solid: Border style (solid line) */
/*   - #00ff00: Border color (bright green) */

/* Line 24: margin: 0 10px; */
/*   - margin: Space outside element */
/*   - 0 10px: 0 top/bottom, 10px left/right */

/* Line 25: display: inline-block; */
/*   - display: Controls how element is laid out */
/*   - inline-block: Stays on same line but can have width/height */

/* Line 28-36: Content Container Styling */
/* #content: CSS ID selector (targets element with id="content") */
/*   - #: Indicates ID selector */
/*   - content: ID name */

/* Line 29: background-color: white; */
/*   - background-color: Background color */
/*   - white: Color value */

/* Line 30: color: black; */
/*   - color: Text color */
/*   - black: Color value */

/* Line 31: border: 2px solid #00ff00; */
/*   - border: Border around content box */

/* Line 32: padding: 20px; */
/*   - padding: Space inside content box */

/* Line 33: margin: 20px auto; */
/*   - margin: Space outside content box */
/*   - 20px: Top and bottom margin */
/*   - auto: Left and right margin (centers the box) */

/* Line 34: max-width: 800px; */
/*   - max-width: Maximum width of element */
/*   - 800px: Value (won't get wider than 800 pixels) */

/* Line 35: text-align: left; */
/*   - text-align: Horizontal text alignment */
/*   - left: Aligns text to left (overrides body's center) */

/* Line 38-44: Character Image Styling */
/* .character-image: CSS class selector (targets elements with class="character-image") */
/*   - .: Indicates class selector */
/*   - character-image: Class name */

/* Line 39: width: 300px; */
/*   - width: Element width */
/*   - 300px: Value (300 pixels wide) */

/* Line 40: height: 300px; */
/*   - height: Element height */
/*   - 300px: Value (300 pixels tall) */

/* Line 41: border: 2px solid #00ff00; */
/*   - border: Border around image */

/* Line 42: margin: 20px auto; */
/*   - margin: Space around image */
/*   - 20px: Top and bottom */
/*   - auto: Left and right (centers image) */

/* Line 43: display: block; */
/*   - display: Layout type */
/*   - block: Takes full width, starts on new line */

/* Line 46-50: Stats Section Styling */
/* .stats-section: CSS class selector */

/* Line 47: margin: 20px 0; */
/*   - margin: Space outside section */
/*   - 20px: Top and bottom */
/*   - 0: Left and right */

/* Line 48: padding: 15px; */
/*   - padding: Space inside section */

/* Line 49: border: 1px solid #00ff00; */
/*   - border: Border around stats section */

/* Line 52-56: Description Section Styling */
/* .description-section: CSS class selector */

/* Line 57: </style> - Closes the CSS styles section */

<!-- Line 58: </head> - Closes the head section -->
```

### Body and Navigation Comments
```
<!--
LESSON: HTML Body Section
=========================
Line 59: <body>
  - <body>: Container for visible page content
  - Everything inside <body> appears on the webpage
  - This is where users see content
-->

<!--
LESSON: Navigation Tabs
======================
Line 60-64: Navigation links to other pages
-->

<!--
Line 61: <nav>
  - <nav>: HTML5 semantic element (indicates navigation)
  - Groups navigation links together
  - Helps screen readers and search engines understand page structure
-->

<!--
Line 62: <a href="/">RADAR</a>
  - <a>: Anchor tag (creates hyperlink)
  - href="/": Link destination (forward slash = homepage)
  - RADAR: Link text (what user sees and clicks)
  - </a>: Closes anchor tag
-->

<!--
Line 63: <a href="/wiki">WIKI</a>
  - <a>: Anchor tag
  - href="/wiki": Link destination (wiki page)
  - WIKI: Link text
-->

<!-- Line 64: </nav> - Closes navigation section -->
```

### Template Variable Comments
```
<!--
Line 66: <h1>RDA WIKI - CHARACTER PROFILE</h1>
  - <h1>: Heading level 1 (largest heading)
  - RDA WIKI - CHARACTER PROFILE: Heading text
  - </h1>: Closes heading tag
-->

<!--
Line 68: <div id="content">
  - <div>: Division/container element (groups content)
  - id="content": Unique identifier (matches #content CSS selector)
  - This div will have white background, centered, max 800px wide
-->

<!--
LESSON: Jinja2 Template Variable - THE KEY TO DYNAMIC CONTENT!
===============================================================
Line 71: <h2>{{ character_name|title }}</h2>

Breaking it down:
-----------------
- <h2>: Heading level 2 (smaller than h1)
- { { } }: Jinja2 template syntax (Flask's template engine) - note: spaces added to avoid template parsing
- character_name: Variable name (passed from Flask route)
- |title: Filter (capitalizes first letter of each word)
- </h2>: Closes heading tag

How it works:
------------
1. Flask route receives URL: /character/jake
2. Flask extracts 'jake' from URL
3. Flask calls: render_template('character.html', character_name='jake')
4. Flask processes template, finds {{ character_name }}
5. Flask replaces {{ character_name }} with 'jake'
6. Flask applies |title filter: 'jake' becomes 'Jake'
7. Final HTML sent to browser: <h2>Jake</h2>

For different characters:
-------------------------
- /character/neytiri → <h2>Neytiri</h2>
- /character/kiri → <h2>Kiri</h2>
- /character/jake → <h2>Jake</h2>

Same template, different content!
-->

<!--
LESSON: Character Image with Dynamic Path
==========================================
Line 75-78: Image that changes based on character
-->

<!--
Line 75: <div style="text-align: center;">
  - <div>: Container element
  - style="...": Inline CSS (applies only to this element)
  - text-align: center: Centers content inside div
-->

<!--
Line 76: <img src="/static/{{ character_name }}_profile.jpg" ...>

Breaking it down:
-----------------
- <img>: Image element (displays picture)
- src="/static/{{ character_name }}_profile.jpg": Image source path
  - /static/: Flask's static files folder
  - {{ character_name }}: Template variable (gets replaced!)
  - _profile.jpg: Filename suffix

How it works:
------------
1. Flask processes template
2. Finds {{ character_name }} in src attribute
3. Replaces with actual character name

Examples:
--------
- For Jake: /static/jake_profile.jpg
- For Neytiri: /static/neytiri_profile.jpg
- For Kiri: /static/kiri_profile.jpg

Each character page looks for their own image file!

Other attributes:
----------------
- alt="{{ character_name|title }}": Alternative text (for screen readers)
- class="character-image": CSS class (applies styling)
- onerror="this.style.display='none'": JavaScript (hides image if file doesn't exist)
-->

<!--
Line 77: <p style="color: #666; font-style: italic;">[Image slot: ...]</p>
  - <p>: Paragraph element
  - style="...": Inline CSS (gray italic text)
  - [Image slot: ...]: Placeholder text (tells user what to add)
  - {{ character_data.image }}: Template variable (shows which file to add)
-->

<!-- Line 78: </div> - Closes image container -->
```

### Stats and Description Section Comments
```
<!--
LESSON: Stats Section
====================
Line 81-90: Placeholder for character statistics
-->

<!--
Line 81: <div class="stats-section">
  - <div>: Container element
  - class="stats-section": CSS class (applies .stats-section styles)
-->

<!--
Line 82: <h3>STATISTICS</h3>
  - <h3>: Heading level 3 (smaller than h2)
  - STATISTICS: Heading text
-->

<!--
Line 83: <p>[Stats section - Add character statistics here]</p>
  - <p>: Paragraph element
  - [Stats section...]: Placeholder text (user will replace this)
-->

<!--
Line 84-89: <ul> and <li> - Unordered List
Line 84: <ul>
  - <ul>: Unordered list (bullet points)
-->

<!--
Line 85: <li>Strength: [Add value]</li>
  - <li>: List item (one bullet point)
  - Strength: [Add value]: Placeholder text
-->

<!-- Line 86-88: More list items (same structure) -->

<!-- Line 89: </ul> - Closes list -->

<!-- Line 90: </div> - Closes stats section -->

<!--
LESSON: Description Section
==========================
Line 93-96: Placeholder for character description
-->

<!--
Line 93: <div class="description-section">
  - <div>: Container
  - class="description-section": CSS class
-->

<!--
Line 94: <h3>DESCRIPTION</h3>
  - <h3>: Heading level 3
-->

<!--
Line 95: <p>[Description section - Add character description here]</p>
  - <p>: Paragraph
  - [Description section...]: Placeholder text
-->

<!-- Line 96: </div> - Closes description section -->
```

### Additional Images and Back Button Comments
```
<!--
LESSON: Additional Images Section
=================================
Line 99-109: Placeholder for extra character images
-->

<!-- Line 99: <div class="description-section"> -->

<!--
Line 100: <h3>ADDITIONAL IMAGES</h3>
  - <h3>: Heading
-->

<!--
Line 101: <p>[Additional images section...]</p>
  - <p>: Paragraph with placeholder text
-->

<!--
LESSON: Jinja2 Loop for Additional Images
==========================================
This loop displays all images in the additional_images list.
If the list is empty, no images will be shown.
-->

<!-- Line 109: </div> - Closes additional images section -->

<!--
LESSON: Back Button
==================
Line 112-114: Link back to wiki page
-->

<!--
Line 112: <div style="...">
  - <div>: Container
  - style="...": Inline CSS (centers content, adds top margin)
-->

<!--
Line 113: <a href="/wiki" style="...">← Back to Wiki</a>
  - <a>: Anchor tag (hyperlink)
  - href="/wiki": Link destination (wiki page)
  - style="...": Inline CSS (green text, padding, border)
  - ← Back to Wiki: Link text (arrow + text)
-->

<!-- Line 114: </div> - Closes back button container -->

<!-- Line 115: </div> - Closes main content div -->

<!-- Line 116: </body> - Closes body section -->

<!-- Line 117: </html> - Closes HTML root element -->
```

## templates/index.html

### HTML Structure Comments
```
<!--
LESSON: HTML Document Structure
================================
HTML (HyperText Markup Language) is the structure of web pages.
- <!DOCTYPE html> tells the browser this is HTML5
- <html> is the root element
- <head> contains metadata (title, styles, scripts)
- <body> contains visible content
-->

<!-- LESSON: CSS (Cascading Style Sheets) -->
<!-- CSS controls how HTML elements look -->
```

### CSS Comments
```
/* LESSON: CSS Selectors and Properties */
/* body selector applies styles to the <body> element */

/* LESSON: Background image properties */

/* LESSON: ID selector (#) - targets element with id="result" */

/* LESSON: Class selector (.) - targets elements with class="status" */

/* LESSON: Element selector - targets all <button> elements */

/* LESSON: Pseudo-class selector (:hover) */
/* This style applies when you hover over the button */

/* LESSON: Disabled state styling */

/* LESSON: Child selector - targets <div> inside #result */
```

### HTML Body Comments
```
<!-- LESSON: HTML Comments -->
<!-- Comments help document your code but don't appear on the page -->

<!-- LESSON: Navigation Tabs -->
<!-- These links let users switch between pages -->

<!-- LESSON: HTML div element -->
<!-- div is a container element used for layout and styling -->

<!-- LESSON: HTML button with onclick event -->
<!-- onclick is an inline event handler that calls JavaScript when clicked -->

<!-- LESSON: JavaScript in HTML -->
<!-- Scripts can be in <head> or <body>. Putting at end of body is often better for performance -->
```

### JavaScript Comments
```
/**
 * LESSON: JavaScript Functions and Async/Await
 * ==============================================
 * 
 * async function = This function can use 'await' to wait for asynchronous operations
 * (like API calls) without blocking the browser
 * 
 * Parameters:
 *   sectorKey (string): The location identifier to scan
 */

// LESSON: DOM Manipulation
// document.getElementById() finds an element by its ID attribute

// LESSON: Disable buttons during request (prevent double-clicks)

// LESSON: Updating element content
// innerText sets plain text (strips HTML)
// innerHTML allows HTML tags (but be careful with user input!)

// LESSON: Fetch API - Modern way to make HTTP requests
// fetch() returns a Promise (an object representing future completion)
// await pauses execution until the Promise resolves

// LESSON: HTTP Status Codes
// response.ok is true if status is 200-299 (success)
// response.status contains the numeric status code

// LESSON: JSON Parsing
// response.json() parses the JSON response body

// LESSON: Template Literals (backticks)
// Template literals allow string interpolation with ${variable}
// They also preserve line breaks and formatting

// LESSON: Conditional rendering
// Only show data if it exists (not null/undefined)

// LESSON: Using innerHTML for styled content
// We can include HTML tags for styling

// LESSON: Updating CSS styles dynamically
// We can change any CSS property via JavaScript

// LESSON: Error handling for HTTP errors
// Try to parse error message from response

// LESSON: Try/Catch Error Handling
// catch blocks handle exceptions (network errors, parsing errors, etc.)
// console.error for debugging

// LESSON: Finally block
// Code in 'finally' always runs, whether there was an error or not
// This ensures buttons are re-enabled even if something goes wrong

// LESSON: Event Listeners (Alternative to inline onclick)
// This is a more modern approach, but inline onclick works fine for simple cases
// You could also use: button.addEventListener('click', () => scanSector('hallelujah_mountains'))
```

## templates/wiki.html

### CSS Comments
```
/* LESSON: CSS Class Selector */
/* .character-button targets elements with class="character-button" */

/* LESSON: CSS for images inside character buttons */

/* LESSON: Individual Color Classes for Character Names */
/* These classes override the default green color */
/* LESSON: CSS Specificity - We need to be MORE specific than .character-button span */
```

### HTML Comments
```
<!-- LESSON: Navigation Tabs -->

<!-- LESSON: Character Buttons with Images -->
<!-- LESSON: Button for Jake Sully -->
<!-- LESSON: Button for Neytiri -->
<!-- LESSON: Button for Colonel Miles Quaritch -->
<!-- LESSON: Button for Ronal (Fire Princess) -->
<!-- LESSON: Button for Kiri -->
<!-- LESSON: Button for Toruk -->
<!-- LESSON: Button for Tuk (Youngest Daughter) -->
<!-- LESSON: Button for Neteyam -->
<!-- LESSON: Button for Lo'ak -->
<!-- LESSON: Button for Tsireya -->
<!-- LESSON: Button for Tonowari -->

<!-- personal test for Varang-->

<!-- LESSON: JavaScript function for button clicks -->
```

### JavaScript Comments
```
// LESSON: window.location.href redirects to a new page
// This navigates to the character's individual page
```

