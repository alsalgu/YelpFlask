from app import create_app as ca
from flask_testing import TestCase
import unittest
import urllib


# Unit Testing Main Routes
# Tests Needed
# 200 checks for routes
# Form validation checks
# Correct data checks
# Redirect checks?

class Test(TestCase):
    def create_app(self):
        app = ca()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        return app

    def test_routes(self):
        # List of paths defined as 200 routes
        written_routes = ['/', '/yelp/categories', '/yelp/businesses/search', '/yelp/businesses/details/', '/yelp/businesses/details/LFVtF9FeWZ3mavVPk0j1Gw']
        # Lists of 404 paths, which should redirect.
        redirect_routes = ['/not-real', '/yelp/businesses/details/fake-business' ]
        for route in written_routes:
            response = self.client.get(route)
            self.assertEqual(response.status_code, 200, route + ' failed.')
        for route in redirect_routes:
            response = self.client.get(route)
            self.assertEqual(response.status_code, 302, route + ' failed.')

    def test_JSON(self):
        # Paths that list JSON
        json_routes = ['/yelp/categories']
        for route in json_routes:
            response = self.client.get(route)
            assert "data" in response.json
    
    def test_POST(self):
        routes_with_POST = ['/yelp/businesses/search', '/yelp/businesses/details/']
        for route in routes_with_POST:
            response = self.client.post(route)
            self.assertEqual(response.status_code, 200, route + ' failed.')

if __name__ == '__main__':
    unittest.main()