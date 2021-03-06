from flask import render_template, current_app, redirect
from flask import request, jsonify, url_for, flash
from app.main import bp
from app.main.secrets import headers
from app.main.forms import searchYelpForm, businessIDForm
import requests


# Function for Requests
# url = yelp Fusion API endpoint
# auth = headers from app.main.secrets
def getJSON(url, auth):
    r = requests.get(url, headers=auth)
    data = r.json()
    return data


# Homepage
@bp.route('/')
def index():
    return render_template('index.html')


# List of yelp api categories, all
@bp.route('/yelp/categories')
def yelpCat():
    # Custom JSON dict
    cat_dict = {"data": []}
    # All categories endpoint set to US location
    ALL_US_CATEGORIES_URL = "https://api.yelp.com/v3/categories?locale=en_US"
    # Request
    data = getJSON(ALL_US_CATEGORIES_URL, headers)
    # Iterate list of categories and
    # append it to predefined dict by title
    for x in data['categories']:
        cat_dict["data"].append(x['title'])
    resp = jsonify(cat_dict)
    return resp


# Form to search and return yelp api list
@bp.route('/yelp/businesses/search', methods=['GET', 'POST'])
def yelpBus():
    search_results = {"data": []}
    # WTForm
    form = searchYelpForm()
    if form.validate_on_submit():
        # Assign data to relevant variables
        LONG = str(form.longitude.data)
        LAT = str(form.latitude.data)
        RADIUS = str(form.radius.data)
        # Build yelp endpoint with search terms
        SEARCH_URL = "https://api.yelp.com/v3/businesses/search?latitude=" + \
            LAT + "&longitude=" + LONG + "&limit=10&radius=" + RADIUS
        # Categories field is optional
        # only add it if its filled
        # Otherwise, error
        if form.categories.data:
            FOOD_CAT = "&categories="
            FOOD_CAT_OP = form.categories.data
            url = SEARCH_URL + FOOD_CAT + FOOD_CAT_OP
            data = getJSON(url, headers)
            resp = jsonify(data)
            for x in data["businesses"]:
                entry = {"id": x["id"], "name": x["name"],
                         "coordinates":
                             {"latitude": x["coordinates"]["latitude"],
                              "longitude": x["coordinates"]["longitude"]}}
                search_results["data"].append(entry)
            resp = jsonify(search_results)
            return resp
        data = getJSON(SEARCH_URL, headers)
        if "error" in data:
            error_desc = data["error"]["description"]
            error_code = data["error"]["code"]
            flash("Sorry there was an error.")
            flash(error_code)
            flash(error_desc)
            return redirect(url_for('main.yelpBus'))
        for x in data["businesses"]:
            entry = {"id": x["id"], "name": x["name"],
                     "coordinates":
                         {"latitude": x["coordinates"]["latitude"],
                          "longitude": x["coordinates"]["longitude"]}}
            search_results["data"].append(entry)
        resp = jsonify(search_results)
        return resp
    return render_template('search.html', form=form)


@bp.route('/yelp/businesses/details/', methods=['GET', 'POST'])
def businessDetails():
    form = businessIDForm()
    if form.validate_on_submit():
        BUSNS_ID = form.business_id.data
        return redirect(url_for('main.yelpSingBus', id=BUSNS_ID))
    return render_template('business-details.html', form=form)


@bp.route('/yelp/businesses/details/<string:id>')
def yelpSingBus(id):
    business_details = {"data": []}
    BUSNS_DET_URL = "https://api.yelp.com/v3/businesses/" + id
    data = getJSON(BUSNS_DET_URL, headers)
    if "error" in data:
        error_desc = data["error"]["description"]
        flash("Sorry there was an error.")
        flash(error_desc)
        return redirect(url_for('main.businessDetails'))
    business_details["data"].append(data)
    resp = jsonify(business_details)
    return resp


# Error Handlin'
@bp.app_errorhandler(404)
def not_found(error):
    flash("Quoth the Raven, 404")
    return redirect(url_for('main.index'))


@bp.app_errorhandler(500)
def internal_error(error):
    flash("I will code 500 errors And I will code 500 more")
    flash("Just to be the internal server error")
    flash("that fried down right at your door. DAH DAH DAH")
    return redirect(url_for('main.index'))
