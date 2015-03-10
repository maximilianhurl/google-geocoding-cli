import unittest
from scripts.search import Geocode


class SearchTestCase(unittest.TestCase):

    def test_key(self):
        geocode = Geocode()
        geocode.set_key("12345")
        self.assertEqual(geocode.current_key, "12345")
