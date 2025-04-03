import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
SHEET_ENDPOINT = os.getenv("SHEET_ENDPOINT")

class DataManager:
    def __init__(self):
        self.destination_data = []

    def get_destination_data(self):
        response = requests.get(url=SHEET_ENDPOINT)
        response.raise_for_status()
        self.destination_data = response.json()["sheet1"]  
        return self.destination_data

    def update_iata_code(self, city_id, iata_code):
        update_endpoint = f"{SHEET_ENDPOINT}/{city_id}"
        body = {
            "sheet1": {  
                "iataCode": iata_code
            }
        }
        response = requests.put(url=update_endpoint, json=body)

        # Debug print to help confirm it's working
        print(f"\nUpdating city ID {city_id} with IATA code '{iata_code}'")
        print("Request body:", body)
        print("Response status code:", response.status_code)
        print("Response text:", response.text)

        response.raise_for_status()
