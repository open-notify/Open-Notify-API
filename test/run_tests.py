#!/usr/bin/env python
import unittest
import urllib2
import json

class TestISSNow(unittest.TestCase):

    def setUp(self):
        self.response = urllib2.urlopen("http://localhost:5000/iss-now.json")


    def test_header(self):
        self.assertEqual(self.response.headers['Content-Type'], 'application/json')

    def test_data(self):
        data = None
        try:
            data = json.loads(self.response.read())
        except TypeError:
            self.fail("ISS Now didn't return valid JSON" )

        if data:
            self.assertEqual(data.get("message", None), "success")
            ts = data.get("timestamp", None)
            if not ts:
                self.fail("No timestamp returned")
            iss = data.get("iss_position", None)
            if not ts:
                self.fail("No iss_position returned")



if __name__ == '__main__':
    unittest.main()
