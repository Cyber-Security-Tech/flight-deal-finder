from amadeus import Client, ResponseError
from flight_data import FlightData
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# 🔐 Load Amadeus API credentials from .env
load_dotenv()

amadeus = Client(
    client_id=os.getenv("AMADEUS_CLIENT_ID"),
    client_secret=os.getenv("AMADEUS_CLIENT_SECRET")
)


class FlightSearch:
    """
    Handles flight-related API calls using the Amadeus SDK.
    - Gets IATA codes for cities
    - Searches for cheap flights
    """

    def get_iata_code(self, city_name):
        """
        Queries Amadeus to retrieve the IATA code for a given city name.

        Args:
            city_name (str): City name to look up (e.g., "Paris")

        Returns:
            str | None: IATA code if found, otherwise None
        """
        try:
            response = amadeus.reference_data.locations.get(
                keyword=city_name,
                subType='CITY'
            )
            if response.data:
                return response.data[0]["iataCode"]
            else:
                print(f"❌ No IATA code found for city: {city_name}")
                return None
        except ResponseError as error:
            print(f"🛑 Amadeus API error (IATA lookup): {error}")
            return None

    def search_flights(self, origin_city, destination_city, max_price):
        """
        Searches for the cheapest flight between two cities using Amadeus.

        Args:
            origin_city (str): IATA code of the origin (e.g., "IAD")
            destination_city (str): IATA code of the destination (e.g., "CDG")
            max_price (float): Maximum budget threshold

        Returns:
            FlightData | None: Flight info object if a deal is found, else None
        """
        # Set date range: from tomorrow to 6 months ahead
        date_from = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        date_to = (datetime.now() + timedelta(days=180)).strftime('%Y-%m-%d')
        return_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')  # Default return: 1 week later

        try:
            response = amadeus.shopping.flight_offers_search.get(
                originLocationCode=origin_city,
                destinationLocationCode=destination_city,
                departureDate=date_from,
                returnDate=return_date,
                adults=1,
                max=1  # Only get the cheapest one
            )

            if not response.data:
                print(f"❌ No flight deals found for {origin_city} → {destination_city}")
                return None

            offer = response.data[0]
            price = float(offer["price"]["total"])

            if price <= max_price:
                # Extract flight segment info
                outbound = offer["itineraries"][0]["segments"][0]
                inbound = offer["itineraries"][1]["segments"][0]

                return FlightData(
                    price=price,
                    origin_city=origin_city,
                    origin_airport=outbound["departure"]["iataCode"],
                    destination_city=destination_city,
                    destination_airport=outbound["arrival"]["iataCode"],
                    departure_date=outbound["departure"]["at"].split("T")[0],
                    return_date=inbound["arrival"]["at"].split("T")[0]
                )

        except ResponseError as error:
            print(f"🛑 Amadeus flight search error: {error}")

        return None
