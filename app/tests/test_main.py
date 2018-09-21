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
            result = self.client.get(route)
            self.assertEqual(result.status_code, 200, route + ' failed.')
        for route in redirect_routes:
            result = self.client.get(route)
            self.assertEqual(result.status_code, 302, route + ' failed.')

    def test_2(self):
        self.assertTrue(True)
 
    def test_3(self):
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()