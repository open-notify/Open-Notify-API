from unittest import main, TestCase
from flask.ext.webtest import TestApp
from app import app


class FrontPageTest(TestCase):
    """Test that the front page is rendering"""

    def setUp(self):
        self.app = app
        self.w = TestApp(self.app)

    def test(self):
        r = self.w.get('/')

        # Assert there was no messages flashed
        self.assertFalse(r.flashes)

        # Assert that we got an index template
        self.assertEqual(r.template, 'index.html')
