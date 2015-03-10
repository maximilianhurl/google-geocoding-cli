import unittest
import requests_mock
from scripts.search import Geocode
from scripts.exceptions import GeocoderException


class SearchTestCase(unittest.TestCase):

    def setUp(self):
        super(SearchTestCase, self).setUp()

        self.key = "12345"

        self.geocode = Geocode()
        self.geocode.set_key(self.key)

    def test_key(self):
        self.assertEqual(self.geocode.current_key, self.key)

    def test_missing_data(self):

        data = {
            "latitude": "",
            "longitude": ""
        }
        self.assertEqual(self.geocode.search(data), data)

        with self.assertRaises(GeocoderException):
            self.geocode.search({})

    @requests_mock.Mocker()
    def test_search_query(self, requests_mock):
        data = {
            "address": "cat st,seagulltown, uk"
        }

        json = {
            "results": [
                {
                    "geometry": {
                        "location": {
                            "lat": "0.0111",
                            "lng": "0.0222",
                        }
                    }
                }
            ],
            "status": "OK"
        }

        requests_mock.register_uri('GET', self.geocode.URL, json=json)

        response = self.geocode.search(data)
        self.assertEqual(response, {
            'latitude': '0.0111', 'longitude': '0.0222', 'address': 'cat st,seagulltown, uk'
        })

        history = requests_mock.request_history
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0].qs, {'key': [self.key], 'address': ['cat st,seagulltown, uk']})

    def test_search_query_validation(self):
        pass
