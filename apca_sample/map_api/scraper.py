import pandas as pd
from sodapy import Socrata
from pathlib import Path
import json
import geopandas as gpd
import os
import dotenv

# Import geojson file with california counties
ca_counties = json.load(open('./data/ca-county-boundaries.geojson', 'r'))

for feature in ca_counties['features']:
    feature['id'] = feature['properties']['geoid']

geo_df = gpd.GeoDataFrame.from_features(
    ca_counties["features"])

print("geo_df: ", geo_df.head())

# Use geo_df to create a dictionary of geoids and county names
geoid_dict = {}

for index, row in geo_df.iterrows():
    if row['namelsad'] not in geoid_dict:
        geoid_dict[row['namelsad']] = row['geoid']

print("geoid_dict: ", geoid_dict)
print("length of geoid_dict: ", len(geoid_dict))

# Make API call to collect unemployment data
BASE_DIR = Path(__file__).resolve().parent.parent
dotenv_file = os.path.join(BASE_DIR, ".env")

if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

APP_TOKEN = os.environ['APP_TOKEN']
APP_USERNAME = os.environ['APP_USERNAME']
APP_PASSWORD = os.environ['APP_PASSWORD']

# client = Socrata("data.edd.ca.gov", None)
client = Socrata("data.edd.ca.gov",
                 APP_TOKEN,
                 username=APP_USERNAME,
                 password=APP_PASSWORD)

# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
results = client.get("r8rw-9pxx", where="status_preliminary_final='Final' AND month='December'", order="year desc", limit=2000)

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)


print("results_df: ", results_df.head())
print("results_df shape: ", results_df.shape)

# Use geoid_dict to create a geoid column in results_df
results_df['geoid'] = results_df['area_name'].map(geoid_dict)
print("results_df with geoid: ", results_df.head())
print("results_df shape with geoid: ", results_df.shape)

# Iterate through the completed results_df and add to database table
