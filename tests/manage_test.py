import unittest
from mock import patch
from scripts.manager import GeocodingManager
from scripts.search import ReverseGeocode
from scripts.exceptions import (
    GeocoderException, GeocoderSetupException, GeocoderOverLimitException
)


class ManagerTestCase(unittest.TestCase):

    @patch('scripts.files.os.path.exists')
    def test_keys(self, path_exists):
        path_exists.return_value = True
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

    @patch('scripts.files.os.path.exists')
    def test_geocode_reverse_switch(self, path_exists):
        path_exists.return_value = True
        manager = GeocodingManager(
            keys=u'1235',
            input_file_path="test.csv",
            query_type=GeocodingManager.REVERSE_GEOCODE_TYPE
        )
        self.assertEqual(type(manager.search_handler), ReverseGeocode)

    @patch('scripts.manager.CSVFileHandler')
    @patch('scripts.manager.Geocode')
    def test_search(self, geocode_mock, csvfile_mock):
        manager = GeocodingManager(keys=u"12345", input_file_path="test.csv")
        csvfile_mock.assert_called_once_with('test.csv')
        geocode_mock.assert_called_once_with()

        geocode_instance = geocode_mock.return_value
        self.assertEqual(geocode_instance.search.call_count, 0)

        csvfile_instance = csvfile_mock.return_value
        self.assertEqual(csvfile_instance.setup_files.call_count, 0)
        self.assertEqual(csvfile_instance.get_rows.call_count, 0)
        self.assertEqual(csvfile_instance.write_result.call_count, 0)
        self.assertEqual(csvfile_instance.close_files.call_count, 0)

        csvfile_instance.get_rows.return_value = ['test_row']
        geocode_instance.search.return_value = 'test_resut'

        manager.search()

        self.assertEqual(csvfile_instance.setup_files.call_count, 1)
        self.assertEqual(csvfile_instance.get_rows.call_count, 1)
        csvfile_instance.write_result.assert_called_with('test_resut')
        self.assertEqual(csvfile_instance.close_files.call_count, 1)
        geocode_instance.search.assert_called_with('test_row')

    @patch('scripts.manager.CSVFileHandler')
    @patch('scripts.manager.Geocode')
    def test_search_over_limit(self, geocode_mock, csvfile_mock):
        manager = GeocodingManager(keys=u"12345", input_file_path="test.csv")
        manager.overAPILimit = True
        csvfile_mock.assert_called_once_with('test.csv')
        geocode_mock.assert_called_once_with()

        geocode_instance = geocode_mock.return_value
        geocode_instance.search.return_value = 'test_resut'
        self.assertEqual(geocode_instance.search.call_count, 0)

        csvfile_instance = csvfile_mock.return_value
        csvfile_instance.get_rows.return_value = ['test_row']

        manager.search()

        self.assertEqual(geocode_instance.search.call_count, 0)

    @patch('scripts.files.os.path.exists')
    @patch('scripts.manager.Geocode')
    def test_search_row_errors(self, geocode_mock, path_exists):
        path_exists.return_value = True
        search_row = ['test']
        manager = GeocodingManager(keys=u"12345,12345", input_file_path="test.csv")
        self.assertEqual(manager.current_key_index, 0)
        self.assertFalse(manager.overAPILimit)
        geocode_mock.assert_called_once_with()

        geocode_instance = geocode_mock.return_value
        geocode_instance.search.side_effect = GeocoderException()

        result = manager.search_row(search_row)
        self.assertEqual(result, search_row)

        geocode_instance.search.side_effect = GeocoderOverLimitException()
        result = manager.search_row(search_row)
        self.assertEqual(result, search_row)
        self.assertEqual(manager.current_key_index, 1)
        self.assertTrue(manager.overAPILimit)
