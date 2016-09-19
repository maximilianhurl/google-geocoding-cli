import unittest
from click.testing import CliRunner
from mock import patch
from scripts.googlegeocodingcli import geocode, reverse_geocode
from tests.common import PathExistsMockMixin


class GeocodingCLITestCase(PathExistsMockMixin, unittest.TestCase):

    @patch('scripts.googlegeocodingcli.GeocodingManager')
    def test_geocode(self, geocoding_mock):
        self.path_exists.return_value = True
        geocoding_mock.return_value.search.return_value = None
        runner = CliRunner()

        with runner.isolated_filesystem():
            with open('test.csv', 'wb') as f:
                f.write(b'test')

            result = runner.invoke(geocode, ['--keys', 'xxxx', '--file', 'test.csv'])
            geocoding_mock.assert_called_with(keys='xxxx', input_file_path='test.csv')
            geocoding_mock.return_value.search.assert_called_with()
            self.assertEqual(result.output, "Gecoding complete!\n")

    def test_geocode_error(self):
        runner = CliRunner()
        result = runner.invoke(geocode, [])
        self.assertEqual(result.output, "Missing keys. Add with --keys \n")

    @patch('scripts.googlegeocodingcli.GeocodingManager')
    def test_reverse_geocode(self, geocoding_mock):
        geocoding_mock.return_value.search.return_value = None
        geocoding_mock.REVERSE_GEOCODE_TYPE = "reverse"
        runner = CliRunner()

        with runner.isolated_filesystem():
            with open('test.csv', 'wb') as f:
                f.write(b'test')

            result = runner.invoke(reverse_geocode, ['--keys', 'xxxx', '--file', 'test.csv'])
            self.assertEqual(result.output, "Reverse Gecoding complete!\n")
            geocoding_mock.assert_called_with(
                keys='xxxx', input_file_path='test.csv', query_type="reverse"
            )

    def test_reverse_geocode_error(self):
        runner = CliRunner()
        result = runner.invoke(reverse_geocode, ['--keys', 'xxxx'])
        self.assertEqual(result.output, "Missing input file. Add with --file \n")
