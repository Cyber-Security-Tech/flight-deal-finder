import requests
import os
from dotenv import load_dotenv

# 🔐 Load environment variables from .env file
load_dotenv()
SHEET_ENDPOINT = os.getenv("SHEET_ENDPOINT")


class DataManager:
    """
    Handles interaction with the Google Sheet via the Sheety API.
    Gets destination data and updates IATA codes.
    """

    def __init__(self):
        self.destination_data = []

    def get_destination_data(self):
        """
        Retrieves destination data from Google Sheets.
        Returns:
            list[dict]: A list of dictionaries containing city, IATA code, and price.
        """
        response = requests.get(url=SHEET_ENDPOINT)
        response.raise_for_status()
        self.destination_data = response.json()["sheet1"]
        return self.destination_data

    def update_iata_code(self, city_id, iata_code):
        """
        Updates the IATA code for a specific city in the Google Sheet.

        Args:
            city_id (int): The row ID of the city in the sheet.
            iata_code (str): The IATA airport code to update.
        """
        update_endpoint = f"{SHEET_ENDPOINT}/{city_id}"
        body = {
            "sheet1": {
                "iataCode": iata_code
            }
        }

        response = requests.put(url=update_endpoint, json=body)
        response.raise_for_status()

        # Optional debug logging
        print(f"\n📤 Updating city ID {city_id} with IATA code '{iata_code}'")
        print("Request body:", body)
        print("Response status code:", response.status_code)
        print("Response text:", response.text)
