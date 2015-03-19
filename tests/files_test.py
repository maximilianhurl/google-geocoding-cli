import unittest
from mock import patch, Mock
from scripts.files import CSVFileHandler
from scripts.exceptions import GeocoderSetupException, GeocoderException


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

    def test_get_rows(self):
        csvhandler = CSVFileHandler(input_file_path="test.csv")
        csvhandler.reader = [
            {"test1": "value1"},
            {"test2": "value2"},
        ]
        count = 0
        for row in csvhandler.get_rows():
            self.assertEqual(csvhandler.reader[count], row)
            count += 1
        self.assertEqual(count, 2)

        # test will error if missing
        csvhandler = CSVFileHandler(input_file_path="test.csv")
        csvhandler.reader = False
        with self.assertRaisesRegexp(GeocoderException, "File reader not yet setup"):
            for row in csvhandler.get_rows():
                pass

    def test_close_files(self):
        csvhandler = CSVFileHandler(input_file_path="test.csv")
        csvhandler.replace_original = Mock()
        csvhandler.input_file = Mock()
        csvhandler.temp_csvfile = Mock()
        csvhandler.writer = True
        csvhandler.reader = True

        csvhandler.close_files()

        csvhandler.replace_original.assert_called_with()
        assert csvhandler.input_file.close.called
        assert csvhandler.temp_csvfile.close.called

        # now test the error
        csvhandler = CSVFileHandler(input_file_path="test.csv")
        with self.assertRaisesRegexp(GeocoderException, "Files not open"):
            csvhandler.close_files()

    @patch('__builtin__.open')
    @patch('scripts.files.csv')
    def test_setup_files(self, csv_mock, open_mock):
        open_mock.return_value = "cats"

        csvhandler = CSVFileHandler(input_file_path="test.csv")
        csvhandler.get_output_cols = lambda x: "cols"
        csvhandler.setup_files()

        open_mock.assert_any_call('test.csv', 'rb')
        open_mock.assert_any_call('geocode-result-temp.csv', 'wb')

        csv_mock.DictReader.assert_called_with('cats', delimiter=',')
        csv_mock.DictWriter.assert_called_with('cats', delimiter=',', fieldnames='cols')
        assert csv_mock.DictWriter.return_value.writeheader.called
