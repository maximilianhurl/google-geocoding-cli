import click
import time
from scripts.files import CSVFileHandler
from scripts.search import Geocode
from scripts.exceptions import (
    GeocoderException, GeocoderSetupException, GeocoderOverLimitException
)


class GeocodingManager():

    GEOCODE_TYPE = 'geocode'

    def __init__(self, keys, input_file_path, query_type=GEOCODE_TYPE):

        self.overAPILimit = False

        self.file_handler = CSVFileHandler(input_file_path)
        self.search_handler = self.get_search_object(query_type)

        self.keys = self.validate_keys(keys)
        self.current_key_index = -1
        self.switch_key()

    def get_search_object(self, query_type):
        if query_type == self.GEOCODE_TYPE:
            return Geocode()
        else:
            pass

    def search(self):
        # loop over data and conduct search query

        self.file_handler.setup_files()

        for row in self.file_handler.get_rows():

            if not self.overAPILimit:
                row = self.search_row(row)
            else:
                click.echo("Over query limit for all keys - try again tomorrow!")

            self.file_handler.write_result(row)

        self.file_handler.close_files()

    def search_row(self, row):
        time.sleep(0.1)  # make sure we dont do too many requests
        if not self.overAPILimit:
            try:
                row = self.search_handler.search(row)
            except GeocoderException:
                pass
            except GeocoderOverLimitException:
                click.echo("Over query limit exception")
                self.switch_key()
                self.search_row(row)  # retry with new key

        return row

    def validate_keys(self, keys):
        # make sure keys are in correct format and return list
        if type(keys) is unicode:
            return keys.split(",")
        else:
            raise GeocoderSetupException("Unable to load keys")

    def switch_key(self):
        # switch to next key if there are anymore
        if (len(self.keys) - 1 > self.current_key_index):
            self.current_key_index += 1
            if self.search_handler:
                self.search_handler.set_key(self.keys[self.current_key_index])
        else:
            self.overAPILimit = True
