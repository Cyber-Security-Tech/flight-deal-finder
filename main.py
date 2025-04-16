from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
from flight_data import FlightData

# 🔧 Toggle this to True to enable recruiter-friendly demo output
DEMO_MODE = True

if DEMO_MODE:
    print("\n🎓 DEMO MODE ENABLED – Running with mock data only\n")

    # 🧪 Mocked example flight (replace with real search in production)
    mock_flight = FlightData(
        price=199,
        origin_city="IAD",
        origin_airport="IAD",
        destination_city="Paris",
        destination_airport="CDG",
        departure_date="2025-06-01",
        return_date="2025-06-08"
    )

    # 🖨️ Pretty-print mock result
    print("✅ CHEAP FLIGHT FOUND!")
    print(f"{mock_flight.origin_city} ({mock_flight.origin_airport}) → {mock_flight.destination_city} ({mock_flight.destination_airport})")
    print(f"Price: ${mock_flight.price}")
    print(f"Departure: {mock_flight.departure_date} | Return: {mock_flight.return_date}")

else:
    # 🛠 Initialize project components
    data_manager = DataManager()
    flight_search = FlightSearch()
    notification_manager = NotificationManager()

    # 📄 Fetch destination data from Google Sheets via Sheety API
    sheet_data = data_manager.get_destination_data()

    for destination in sheet_data:
        origin = "IAD"  # Default origin airport (Washington D.C.)
        dest_code = destination["iataCode"]
        max_price = destination["lowestPrice"]
        city_name = destination["city"]

        print(f"\n🔍 Searching for flights: {origin} → {dest_code} (Max: ${max_price})")

        # 🛫 Search for flights using Tequila API
        flight = flight_search.search_flights(
            origin_city=origin,
            destination_city=dest_code,
            max_price=max_price
        )

        if flight:
            # ✅ Found deal under budget
            print("✅ CHEAP FLIGHT FOUND!")
            print(f"{flight.origin_city} ({flight.origin_airport}) → {flight.destination_city} ({flight.destination_airport})")
            print(f"Price: ${flight.price}")
            print(f"Departure: {flight.departure_date} | Return: {flight.return_date}")

            # ✉️ Send email notification to users
            notification_manager.send_email(flight)
        else:
            print("❌ No deals found within budget.")
