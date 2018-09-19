from flask import render_template, current_app
from flask import request, jsonify
from app.main import bp
from app.main.config import headers
import requests

'''
TO DO:

Make 3 JSON Endpoints using Yelp API

[X]/yelp/categories
--Only categories in the US

[]/yelp/businesses/search
• Requests a list of 10 matching businesses within a radius
• Accept the following query string parameters:
• latitude (required)
• longitude (required)
• radius (max of 1 mile, default of 1 mile)
• categories (optional)
Return a JSON list of business objects with IDs, names, and coordinates.

[]/yelp/businesses/details/<string:id>
Gets business details from Yelp using the provided ID. Return the full response under a
"data" key, as in the above examples.

'''

# Defaults
LONG = "30.267153"
LAT = "-97.743057"
RADIUS = "1609" # Meters
FOOD_CAT = "&categories="
FOOD_CAT_OP = ""
BUSNS_ID = "LFVtF9FeWZ3mavVPk0j1Gw"

# Yelp Endpoints
ALL_US_CATEGORIES_URL = "https://api.yelp.com/v3/categories?locale=en_US"
SEARCH_URL = "https://api.yelp.com/v3/businesses/search?latitude=" + LONG + "&longitude=" + LAT + "&limit=10&radius=" + RADIUS
BUSNS_DET_URL = "https://api.yelp.com/v3/businesses/" + BUSNS_ID

# Function for Requests
def getJSON(url, auth):
    r = requests.get(url, headers=auth)
    data = r.json()
    return data

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/yelp/categories')
def yelpCat():
    cat_dict = {"data":[]}
    data = getJSON(ALL_US_CATEGORIES_URL, headers)
    for x in data['categories']:
        cat_dict["data"].append(x['title'])
    resp = jsonify(cat_dict)
    return resp

@bp.route('/yelp/businesses/search')
def yelpBus():
    return render_template('index.html')

@bp.route('/yelp/businesses/details/<string:id>')
def yelpSingBus():
    return render_template('index.html')

# Error Handlin'

@bp.app_errorhandler(404)
def not_found(error):
    return "Quoth the Raven, 404"

@bp.app_errorhandler(500)
def internal_error(error):
    return "I will code 500 errorm And I will code 500 more, \
            just to be the internal server \
            error that fried down at your door. DAH DAH DAH"