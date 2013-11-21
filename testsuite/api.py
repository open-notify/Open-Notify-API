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
        
        self.assertEqual(data['message'], "success", "ISS API Did not return 'sucess' message")

