import unittest
import requests_mock
from scripts.search import Geocode, ReverseGeocode
from scripts.exceptions import GeocoderException, GeocoderOverLimitException


class SearchTestBase(unittest.TestCase):

    address_data = {
        "latitude": "1234",
        "longitude": "1234",
        "address": "123 cat street"
    }

    def setUp(self):
        super(SearchTestBase, self).setUp()
        self.key = "12345"
        self.geocode.set_key(self.key)


class GeocodeSearchTestCase(SearchTestBase):

    def setUp(self):
        self.geocode = Geocode()
        super(GeocodeSearchTestCase, self).setUp()
        self.data = {"address": "cat st,seagulltown, uk"}

    def test_key(self):
        self.assertEqual(self.geocode.current_key, self.key)

    def test_missing_data_address(self):
        data = {
            "latitude": "",
            "longitude": "",
        }
        with self.assertRaisesRegexp(GeocoderException, "Missing data: address"):
            self.geocode.search(data)

    def test_contains_lat_long(self):
        self.assertEqual(self.geocode.search(self.address_data), self.address_data)

    @requests_mock.Mocker()
    def test_search_query(self, requests_mock):

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

        response = self.geocode.search(self.data)
        self.assertEqual(response, {
            'latitude': '0.0111', 'longitude': '0.0222', 'address': 'cat st,seagulltown, uk'
        })

        history = requests_mock.request_history
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0].qs, {'key': [self.key], 'address': ['cat st,seagulltown, uk']})

    @requests_mock.Mocker()
    def test_search_query_status_error(self, requests_mock):

        requests_mock.register_uri('GET', self.geocode.URL, status_code=400)

        with self.assertRaisesRegexp(GeocoderException, "Status Error: 400"):
            self.geocode.search(self.data)

    @requests_mock.Mocker()
    def test_search_query_over_limit(self, requests_mock):

        json = {"status": "OVER_QUERY_LIMIT"}

        requests_mock.register_uri('GET', self.geocode.URL, json=json)

        with self.assertRaises(GeocoderOverLimitException):
            self.geocode.search(self.data)

    @requests_mock.Mocker()
    def test_search_query_google_status_error(self, requests_mock):

        json = {"status": "AUTH ERROR"}

        requests_mock.register_uri('GET', self.geocode.URL, json=json)

        with self.assertRaisesRegexp(GeocoderException, "Results Error: AUTH ERROR"):
            self.geocode.search(self.data)


class ReverseGeocodeSearchTestCase(SearchTestBase):

    def setUp(self):
        self.geocode = ReverseGeocode()
        super(ReverseGeocodeSearchTestCase, self).setUp()
        self.data = {"latitude": "0.0111", "longitude": "0.0222"}

    def test_key(self):
        self.assertEqual(self.geocode.current_key, self.key)

    def test_missing_data_lat_long(self):
        data = {"address": ""}
        with self.assertRaisesRegexp(GeocoderException, "Missing data: lat/long"):
            self.geocode.search(data)

    def test_contains_address(self):
        self.assertEqual(self.geocode.search(self.address_data), self.address_data)

    @requests_mock.Mocker()
    def test_reverse_search_query(self, requests_mock):

        json = {
            "results": [
                {
                    "formatted_address": "cat st,seagulltown, uk"
                }
            ],
            "status": "OK"
        }

        requests_mock.register_uri('GET', self.geocode.URL, json=json)

        response = self.geocode.search(self.data)
        self.assertEqual(response, {
            'latitude': '0.0111',
            'longitude': '0.0222',
            'address': 'cat st,seagulltown, uk'
        })

        history = requests_mock.request_history
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0].qs, {'key': [self.key], 'latlng': ['0.0111,0.0222']})
