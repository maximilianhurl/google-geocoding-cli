[![Build Status](https://travis-ci.org/maximilianhurl/google-geocoding-cli.svg)](https://travis-ci.org/maximilianhurl/google-geocoding-cli)

[![Coverage Status](https://coveralls.io/repos/maximilianhurl/google-geocoding-cli/badge.svg?branch=master)](https://coveralls.io/r/maximilianhurl/google-geocoding-cli?branch=master)


## Google Geocoding CLI

Takes a CSV containing location data and will carry out geocoding or reverse geocoding using the [Google Geocoding API](https://developers.google.com/maps/documentation/geocoding/).



##Installation

    pip install googlegeocodingcli


## Usage


#### geocoding (address -> lat,long)

When geocoding the CSV file requires a column containing the address.

    geocode --keys xxxxxxxxx --file path/test.csv
    
This will create a temporary file that will store the results of the geocoding and when completed will replace the original file.


#### Reverse geocoding (lat,long -> address)

When reverse geocoding the CSV file requires two columns called 'latitude' and 'longitude'.

    reverse_geocode --keys xxxxxxxx --file path/test.csv

#### Using multiple GoogleAPI keys

To increase the number of searches you can conduct per day you can use multiple Google API keys. The keys will be automatically switch through once they reach their daily quota.

    reverse_geocode --keys xxxxxx,xxxxxx,xxxxxx --file path/test.csv

If you reach you daily quota you for all your keys you can run the CLI again the next day and it will start from where it left (when using the resulting file).


####Running the tests
   
- Clone the repo

Now run the following inside the project's directory

	virtualenv env
    source env/bin/activate
    pip install --editable .
    ./runtests