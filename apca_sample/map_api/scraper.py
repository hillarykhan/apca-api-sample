import pandas as pd
from sodapy import Socrata
from pathlib import Path
import os
import dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
dotenv_file = os.path.join(BASE_DIR, ".env")

if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

APP_TOKEN = os.environ['APP_TOKEN']
APP_USERNAME = os.environ['APP_USERNAME']
APP_PASSWORD = os.environ['APP_PASSWORD']

client = Socrata("data.edd.ca.gov", None)
# client = Socrata("data.edd.ca.gov",
#                  APP_TOKEN)
                #  USERNAME=APP_USERNAME,
                #  PASSWORD=APP_PASSWORD)

# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
results = client.get("r8rw-9pxx", where="status_preliminary_final='Final' AND month='December'", order="year desc", limit=2000)

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)

print(results_df.head())
print(results_df.shape)
