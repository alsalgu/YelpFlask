from flask import url_for

def test_routes(client):
    routes = {"GET":['main.index',
                     'main.yelpCat',
                     'main.yelpBus',
                     'main.yelpSingBus',
                     'main.businessDetails'], 
              "POST":['main.yelpBus',
                      'main.businessDetails']}
    valid_ID = "LFVtF9FeWZ3mavVPk0j1Gw"
    
    for route in routes["GET"]:
        if route == 'main.yelpSingBus':
            assert client.get(url_for(route, id=valid_ID)).status_code == 200
        else: 
            assert client.get(url_for(route)).status_code == 200
    for route in routes["POST"]:
        assert client.post(url_for(route)).status_code == 200