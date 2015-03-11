import unittest
from scripts.manager import GeocodingManager
from scripts.exceptions import GeocoderSetupException


class ManagerTestCase(unittest.TestCase):

    def setUp(self):
        super(ManagerTestCase, self).setUp()

    def test_keys(self):
        keys = u"12345,65432"
        manager = GeocodingManager(keys=keys, input_file_path="test.csv")
        self.assertEqual(manager.keys, ['12345', '65432'])
        self.assertEqual(manager.current_key_index, 0)

        keys = u"12345"
        manager = GeocodingManager(keys=keys, input_file_path="test.csv")
        self.assertEqual(manager.keys, ['12345'])
        self.assertEqual(manager.current_key_index, 0)

        with self.assertRaisesRegexp(GeocoderSetupException, "Unable to load keys"):
            GeocodingManager(keys=None, input_file_path="test.csv")
