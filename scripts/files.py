import csv
import os
from scripts.exceptions import GeocoderException, GeocoderSetupException


class FileHanlderBase(object):

    def __init__(self, input_file_path):

        if not os.path.exists(input_file_path):
            raise GeocoderSetupException("Unable to find file: %s" % input_file_path)

        self.input_file_path = input_file_path
        self.temp_file_path = "%s%s.%s" % (
            os.path.dirname(input_file_path),
            "geocode-result-temp",
            self.FILE_EXT
        )

    def replace_original(self):
        # replace oringal file with resulting file
        os.rename(self.temp_file_path, self.input_file_path)


class CSVFileHandler(FileHanlderBase):

    REQUIRED_COLS = ['address', 'latitude', 'longitude']
    FILE_EXT = "csv"

    def setup_files(self):
        # open and setup temp file with correct columns
        self.input_file = open(self.input_file_path, 'rb')
        self.temp_csvfile = open(self.temp_file_path, 'wb')

        self.reader = csv.DictReader(self.input_file, delimiter=',')

        self.writer = csv.DictWriter(
            self.temp_csvfile,
            delimiter=',',
            fieldnames=self.get_output_cols(self.reader)
        )
        self.writer.writeheader()

    def get_output_cols(self, input_file):
        # gets the coloumns of the input file to be added to the output
        fieldnames = input_file.fieldnames
        for col in (col for col in self.REQUIRED_COLS if col not in fieldnames):
            fieldnames.append(col)
        return fieldnames

    def close_files(self):
        if not self.input_file or not self.temp_csvfile:
            raise GeocoderException("Files not open")

        self.replace_original()

        self.input_file.close()
        self.temp_csvfile.close()
        self.writer = None
        self.reader = None

    def get_rows(self):
        # returns each column (cloned)
        if not self.reader:
            raise GeocoderException("File reader not yet setup")

        for row in self.reader:
            result_row = row.copy()
            yield result_row

    def write_result(self, result_row):
        self.writer.writerow(result_row)
