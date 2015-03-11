import unittest
from mock import patch, Mock
from scripts.files import CSVFileHandler
from scripts.exceptions import GeocoderSetupException


class CSVFileTestCase(unittest.TestCase):

    def setUp(self):
        super(CSVFileTestCase, self).setUp()

    @patch('scripts.files.os.path.exists')
    def test_init(self, path_exists):

        path_exists.return_value = False
        with self.assertRaisesRegexp(GeocoderSetupException, "Unable to find file: /cat/test.csv"):
            CSVFileHandler(input_file_path="/cat/test.csv")

        path_exists.return_value = True
        csvhandler = CSVFileHandler(input_file_path="/cat/test.csv")
        self.assertEqual(csvhandler.input_file_path, "/cat/test.csv")
        self.assertEqual(csvhandler.temp_file_path, "/cat/geocode-result-temp.csv")

        csvhandler = CSVFileHandler(input_file_path="test.csv")
        self.assertEqual(csvhandler.temp_file_path, "geocode-result-temp.csv")

    @patch('scripts.files.os.rename')
    def test_replace_original(self, os_rename):
        csvhandler = CSVFileHandler(input_file_path="test.csv")
        csvhandler.replace_original()
        os_rename.assert_called_with('geocode-result-temp.csv', 'test.csv')

    def test_write_row(self):
        csvhandler = CSVFileHandler(input_file_path="test.csv")
        csvhandler.writer = Mock()
        csvhandler.write_result("test")
        csvhandler.writer.writerow.assert_called_with('test')

    def test_get_output_cols(self):
        csvhandler = CSVFileHandler(input_file_path="test.csv")
        input_file = Mock()
        input_file.fieldnames = ['test']
        cols = csvhandler.get_output_cols(input_file)
        self.assertEqual(cols, ['test', 'address', 'latitude', 'longitude'])
