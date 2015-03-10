[![Build Status](https://travis-ci.org/maximilianhurl/google-geocoding-cli.svg)](https://travis-ci.org/maximilianhurl/google-geocoding-cli)

[![Coverage Status](https://coveralls.io/repos/maximilianhurl/google-geocoding-cli/badge.svg)](https://coveralls.io/r/maximilianhurl/google-geocoding-cli)

## TO DO

- improve custom exceptions
- improve logging of exceptons - how to use with click?
- add reverse geocode
- add tests
- add support for JSON


## Features

- Will add columns files to data file
- When completed will replace the original file
- Can use multiple API keys and will switch when it reaches the API quota

##Installation

    pip install googlegeocodingcli
    geocode --keys xxxxxxxxx --file test.csv
    reverse_geocode --keys xxxxxx,xxxxxx,xxxxxx --file path/test.csv


###Installing manually
   
- Clone the repo

Now run the following inside the  directory

	$ virtualenv env
    $ source env/bin/activate
    $ pip install --editable .