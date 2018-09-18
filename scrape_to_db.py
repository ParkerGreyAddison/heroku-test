import os
import psycopg2
import requests
import json

### Scraping from Vons ###

# Vons
url = 'https://shop.vons.com/bin/safeway/login'
base = 'https://shop.vons.com/bin/safeway/product/results'

# Scrape terms
ZIP = 92092
KEY = 'promo'
VALUE = 'popular-items-1750'

data = {'zipcode':ZIP}
payload = {'key':KEY, 'value':VALUE}

# Session start
s = requests.Session()

s.post(url, data=data)
r = s.get(base, params=payload)

results = r.json()['products']

# Index by id
data = {}
for item in results:
    data[item.pop('id')] = item

# Convert to json string
data_json = json.dumps(data)



### Adding to table ###

# Initializing connection and cursor
DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode="require")
cur = conn.cursor()

# Finally insert zipcode into column 'zipcode' and json into column 'json'
cur.execute("INSERT INTO scrapes VALUES (%s, %s);", (ZIP, data_json))
    # This worked practically line for line when testing locally.

#! For the project, the relevant keys of the json will receive their own columns,
    # this is just for testing purposes... not a good practice in this case!

# Commit and close connection
conn.commit()
cur.close()
conn.close()