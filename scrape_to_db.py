import os
import psycopg2
import requests
import json

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode="require")

cur = conn.cursor()

### Scrape from a zipcode and add to existing table ###

# Vons
url = 'https://shop.vons.com/bin/safeway/login'
base = 'https://shop.vons.com/bin/safeway/product/results'


# Scrape terms
ZIP = 92092
KEY = 'promo'
VALUE = 'popular-items-1750'

# data = {'resourcePath': '/content/shop/vons/en/welcome/jcr:content/root/responsivegrid/column_control/par_0/two_column_zip_code_', 'zipcode': 92092}
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


# Add to table as json dumps
to_add = json.dumps(data)

#! Not quite ready yet!!!
    # Need to wrap this string with single quotes, and replace all double quotes with two single quotes
to_add.replace('"', "''")
    # Wow that's a line of code I never want to see again
final_json = "'" + to_add + "'"

# Finally insert zipcode into column 'zipcode' and json into column 'json'
cur.execute("INSERT INTO scrapes (zipcode, json) VALUES (%s, %s)" % (ZIP, to_add))

# Close connection
conn.commit()
cur.close()
conn.close()