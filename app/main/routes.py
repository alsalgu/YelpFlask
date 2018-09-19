from flask import render_template, current_app
from flask import request, jsonify
from app.main import bp
from app.main.config import API_KEY_YELP

'''
TO DO:

Make 3 JSON Endpoints using Yelp API

/yelp/categories
Only categories in the US

/yelp/businesses/search
• Requests a list of 10 matching businesses within a radius
• Accept the following query string parameters:
• latitude (required)
• longitude (required)
• radius (max of 1 mile, default of 1 mile)
• categories (optional)
Return a JSON list of business objects with IDs, names, and coordinates.

/yelp/businesses/details/<string:id>
Gets business details from Yelp using the provided ID. Return the full response under a
"data" key, as in the above examples.

'''

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/yelp/categories')
def yelpCat():
    return render_template('index.html')

@bp.route('/yelp/businesses/search')
def yelpBus():
    return render_template('index.html')

@bp.route('/yelp/businesses/details/<string:id>')
def yelpSingBus():
    return render_template('index.html')