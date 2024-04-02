import requests
import os.path

CRIME_DATA_FILENAME = "crime_data.csv"
CRIME_DATA_URL = "https://data.lacity.org/api/views/2nrs-mtv8/rows.csv?accessType=DOWNLOAD"


def download_crime_data():
    if not os.path.exists(CRIME_DATA_FILENAME):
        print("Downloading ...")
        response = requests.get(CRIME_DATA_URL)
        with open(CRIME_DATA_FILENAME, 'w') as file:
            file.write(response.text)
