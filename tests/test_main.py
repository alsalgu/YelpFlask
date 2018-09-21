from flask import url_for
from app.main.forms import businessIDForm
from app.main.forms import searchYelpForm


# Ensure routes return expected status codes.
def test_routes(client):
    # I've sorted route functions to plug into flask's url_for
    # Seperated them into the request.methods expected of them
    routes = {"GET": ['main.index',
                      'main.yelpCat',
                      'main.yelpBus',
                      'main.yelpSingBus',
                      'main.businessDetails'],
              "POST": ['main.yelpBus',
                       'main.businessDetails'],
              "404": ['/fake-path',
                      '/yelp/businesses/details/fake-id']}
    # Could change at any given time
    # Its a business id from the yelp api
    # So if there's a failure, check if this is still valid on yelp.
    valid_ID = "LFVtF9FeWZ3mavVPk0j1Gw"

    # Iterate through the routes in the dict.key GET
    # 200 OK expected
    for route in routes["GET"]:
        # main.yelpSingBus requires a business id to return valid.
        if route == 'main.yelpSingBus':
            assert client.get(url_for(route, id=valid_ID)).status_code == 200
        else:
            assert client.get(url_for(route)).status_code == 200

    # Iterate through the routes in the dict.key POST
    # 200 OK expected.
    for route in routes["POST"]:
        assert client.post(url_for(route)).status_code == 200

    # Iterate through the routes in the dict.key 404
    # Redirect expected due to error handler.
    for route in routes["404"]:
        assert client.get(route).status_code == 302


# Ensure POST with valid data returns JSON dump with expected results
def test_ID_post(client):
    # WTForm for business ID search
    # Again, data is from Yelp's API so if it fails
    # Check business id first.
    form = businessIDForm(business_id="LFVtF9FeWZ3mavVPk0j1Gw",
                          viewBusiness=True)
    # Post data from appropriate route and follow redirects
    resp = client.post(url_for('main.businessDetails'),
                       follow_redirects=True, data=form.data)
    # "data" should be in the JSON result
    assert "data" in resp.json
    # And since data is valid, there shouldn't be an error
    assert "error" not in resp.json['data'][0]


# Same as above but with business details form
def test_search_post(client):
    form = searchYelpForm(latitude='30.2672',
                          longitude='-97.7431',
                          radius='1609',
                          category='bbq',
                          search=True)
    resp = client.post(url_for('main.yelpBus'),
                       follow_redirects=True, data=form.data)
    assert "data" in resp.json
    assert "error" not in resp.json['data'][0]


# Ensure POST with invalid data redirects and shows error message
def test_ID_post_fail(client):
    form = businessIDForm(business_id="fake-id",
                          viewBusiness=True)
    resp = client.post(url_for('main.businessDetails'),
                       follow_redirects=True, data=form.data)
    # Search for message bytes in HTML dump
    # If error, check first you didn't  change the message in routes
    assert b'Sorry there was an error' in resp.data


# Same as above but with business details form
def test_search_post_fail(client):
    form = searchYelpForm(latitude='300.2672',
                          longitude='-999.7431',
                          radius='1609',
                          category='bbq',
                          search=True)
    resp = client.post(url_for('main.yelpBus'),
                       follow_redirects=True, data=form.data)
    assert b'Sorry there was an error' in resp.data


# Ensure categories route returns JSON dump with expected results
def test_category_JSON(client):
    resp = client.get(url_for('main.yelpCat'))
    assert "data" in resp.json
