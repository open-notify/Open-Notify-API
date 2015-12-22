from unittest import main, TestCase
from flask.ext.webtest import TestApp
import json
from app import app

class IssPassTest(TestCase):
    """Test ISS-pass API"""
    def setUp(self):
        self.app = app
        self.w = TestApp(self.app)
        self.endpoint = '/iss-pass.json'

    def format_uri(self, lat, lon):
        return self.endpoint + '?lat={0}&lon={1}'.format(lat, lon) 
    
    def test_berkeley(self):
        berkeley = self.format_uri(37.8715926, -122.27274699999998)
        r = self.w.get(berkeley)
        r.charset = 'utf8'
        data = json.loads(r.text)
        self.assertEqual(r.status_code, 200)

    def test_no_passes_found(self):
        mcmurdo_station = self.format_uri(-77.8418779, 166.6863449)
        r = self.w.get(mcmurdo_station)
        self.assertEqual(r.status_code, 200)
        data = r.json
        self.assertEqual(len(data['response']), 0)

    def test_bad_lat(self):
        bad_lat = self.format_uri(-91, 50)
        r = self.w.get(bad_lat, expect_errors=True)
        self.assertEqual(r.status_code, 400)
        

class IssNowTest(TestCase):
    """Test the ISS-now API"""

    def setUp(self):
        self.app = app
        self.w = TestApp(self.app)

    def test_load(self):
        # Test the endpoints
        r = self.w.get('/iss-now.json')
        self.assertFalse(r.flashes)
        r = self.w.get('/iss-now/')
        self.assertFalse(r.flashes)
        r = self.w.get('/iss-now/v1')
        self.assertFalse(r.flashes)

    def test_data(self):
        r = self.w.get('/iss-now.json')
        r.charset = 'utf8'
        try:
            data = json.loads(r.text)
        except:
            self.fail("ISS API not a valid JSON response")

        # Success message
        self.assertEqual(data['message'], "success", "ISS API Did not return 'sucess' message")

        # timestamp exists
        self.assertTrue('timestamp' in data)

        # position data
        self.assertTrue('iss_position' in data)
        self.assertTrue('latitude' in data['iss_position'])
        self.assertTrue('longitude' in data['iss_position'])


class AstrosTest(TestCase):
    """Test the number of astros API"""

    def setUp(self):
        self.app = app
        self.w = TestApp(self.app)

    def test_load_astros(self):
        r = self.w.get('/astros.json')
        self.assertFalse(r.flashes)
        r = self.w.get('/astros/')
        self.assertFalse(r.flashes)
        r = self.w.get('/astros/v1')
        self.assertFalse(r.flashes)

    def test_data(self):
        r = self.w.get('/astros.json')
        r.charset = 'utf8'
        try:
            data = json.loads(r.text)
        except:
            self.fail("ISS API not a valid JSON responce")

        # Success message
        self.assertEqual(data['message'], "success", "ISS API Did not return 'sucess' message")

        # data exists
        self.assertTrue('number' in data)
        self.assertEqual(type(data['number']), int)
        self.assertTrue('people' in data)
