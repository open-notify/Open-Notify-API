from unittest import main, TestCase
from flask.ext.webtest import TestApp
import json
from app import app


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
            self.fail("ISS API not a valid JSON responce")

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

class IssPathTest(TestCase):
    """Test the ISS-path API"""

    def setUp(self):
        self.app = app
        self.w = TestApp(self.app)

    def test_load(self):
        # Test the endpoints
        r = self.w.get('/iss-path.json')
        self.assertFalse(r.flashes)
        r = self.w.get('/iss-path/')
        self.assertFalse(r.flashes)
        r = self.w.get('/iss-path/v1')
        self.assertFalse(r.flashes)

    def test_data(self):
        r = self.w.get('/iss-path.json')
        r.charset = 'utf8'
        try:
            data = json.loads(r.text)
        except:
            self.fail("ISS API not a valid JSON responce")

        # Success message
        self.assertEqual(data['message'], "success", "ISS API Did not return 'sucess' message")

        # timestamp exists
        self.assertTrue('timestamp' in data)

        # position data
        self.assertTrue('path' in data)
        self.assertEqual(len(data['path']), 45*2+1)
        self.assertTrue('iss_position' in data['path'][0])
        self.assertTrue('delta_minute' in data['path'][0])
        self.assertTrue('longitude' in data['path'][0]['iss_position'])
        self.assertTrue('latitude' in data['path'][0]['iss_position'])