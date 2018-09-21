from flask import url_for
from app.main.forms import businessIDForm
from app.main.forms import searchYelpForm

def test_routes(client):
    routes = {"GET":['main.index',
                     'main.yelpCat',
                     'main.yelpBus',
                     'main.yelpSingBus',
                     'main.businessDetails'], 
              "POST":['main.yelpBus',
                      'main.businessDetails'],
              "404":['/fake-path',
                     '/yelp/businesses/details/fake-id']}
    valid_ID = "LFVtF9FeWZ3mavVPk0j1Gw"

    for route in routes["GET"]:
        if route == 'main.yelpSingBus':
            assert client.get(url_for(route, id=valid_ID)).status_code == 200
        else: 
            assert client.get(url_for(route)).status_code == 200
    for route in routes["POST"]:
        assert client.post(url_for(route)).status_code == 200
    for route in routes["404"]:
        assert client.get(route).status_code == 302

def test_ID_post(client):
    form = businessIDForm(business_id="LFVtF9FeWZ3mavVPk0j1Gw",
                          viewBusiness=True)
    resp = client.post(url_for('main.businessDetails'), follow_redirects=True, data=form.data)
    assert "data" in resp.json

def test_search_post(client):
    form = searchYelpForm(latitude='30.2672',
                          longitude='-97.7431',
                          radius='1609',
                          category='bbq',
                          search=True)
    resp = client.post(url_for('main.yelpBus'), follow_redirects=True, data=form.data)
    assert "data" in resp.json

def test_ID_post_fail(client):
    form = businessIDForm(business_id="fake-id",
                          viewBusiness=True)
    resp = client.post(url_for('main.businessDetails'), follow_redirects=True, data=form.data)
    assert b'Sorry there was an error' in resp.data

def test_search_post_fail(client):
    form = searchYelpForm(latitude='300.2672',
                          longitude='-999.7431',
                          radius='1609',
                          category='bbq',
                          search=True)
    resp = client.post(url_for('main.yelpBus'), follow_redirects=True, data=form.data)
    assert b'Sorry there was an error' in resp.data

def test_category_JSON(client):
    resp = client.get(url_for('main.yelpCat'))
    assert "data" in resp.json