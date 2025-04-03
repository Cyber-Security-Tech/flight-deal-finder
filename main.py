from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()

sheet_data = data_manager.get_destination_data()

for destination in sheet_data:
    
    origin = "IAD"  
    dest_code = destination["iataCode"]
    max_price = destination["lowestPrice"]
    city_name = destination["city"]

    print(f"\n🔍 Searching for flights: {origin} → {dest_code} (Max: ${max_price})")

    flight = flight_search.search_flights(
        origin_city=origin,
        destination_city=dest_code,
        max_price=max_price
    )

    if flight:
        # Console output
        print("✅ CHEAP FLIGHT FOUND!")
        print(f"{flight.origin_city} ({flight.origin_airport}) → {flight.destination_city} ({flight.destination_airport})")
        print(f"Price: ${flight.price}")
        print(f"Departure: {flight.departure_date} | Return: {flight.return_date}")

        # Send email alert
        notification_manager.send_email(flight)
    else:
        print("❌ No deals found within budget.")
