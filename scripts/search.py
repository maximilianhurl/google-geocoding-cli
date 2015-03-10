import requests
import click
from scripts.exceptions import GeocoderException, GeocoderOverLimitException


class SearchBase(object):

    def set_key(self, key):
        self.current_key = key

    def validate_response(self, response):
        # validate a response from Google API
        if response.status_code != 200:
            click.echo("Search Status Error: %s" % response.status_code)
            raise GeocoderException("Status Error: %s" % response.status_code)

        data = response.json()

        if data['status'] == "OVER_QUERY_LIMIT":
            raise GeocoderOverLimitException("Over Limit Error: %s" % data['status'])

        if data['status'] != "OK":
            click.echo("Search Status Error: %s" % data['status'])
            raise GeocoderException("Results Error: %s" % data['status'])

        return data


class Geocode(SearchBase):

    """
    example query:
    https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&key=API_KEY
    """

    URL = "https://maps.googleapis.com/maps/api/geocode/json"

    def search(self, row):

        if 'latitude' not in row.keys() or 'longitude' not in row.keys():

            if 'address' not in row.keys():
                raise GeocoderException("Missing data: address")

            payload = {'key': self.current_key, 'address': row['address']}
            response = requests.get(self.URL, params=payload)

            data = self.validate_response(response)

            # now return the results
            latlong = data['results'][0]['geometry']['location']

            row['latitude'] = latlong['lat']
            row['longitude'] = latlong['lng']

        return row
