
#TO DO

# === improve custom exceptions
# === improve logging of exceptons - how to use with click?
# === add reverse geocode
# === add tests
# === add support for JSON

- Will add columns files to data file
- When completed will replace the original file
- Can use multiple API keys and will switch when it reaches the API quota

##Installation

    pip install googlegeocodingcli
    geocode --keys xxxxxxxxx --file test.csv
    reverse_geocode --keys xxxxxx,xxxxxx,xxxxxx --file path/test.csv


###Installing manually
    
- Clone the repo    

    $ virtualenv env
    $ source env/bin/activate
    $ pip install --editable .