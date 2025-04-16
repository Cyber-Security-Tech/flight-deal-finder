class FlightData:
    """
    Represents the essential data for a roundtrip flight deal.
    Used to pass structured flight info between modules.
    """

    def __init__(self, price, origin_city, origin_airport,
                 destination_city, destination_airport,
                 departure_date, return_date):
        """
        Initializes a FlightData object.

        Args:
            price (float): Total price of the flight
            origin_city (str): City of origin
            origin_airport (str): IATA airport code of origin
            destination_city (str): Destination city
            destination_airport (str): IATA airport code of destination
            departure_date (str): Departure date (YYYY-MM-DD)
            return_date (str): Return date (YYYY-MM-DD)
        """
        self.price = price
        self.origin_city = origin_city
        self.origin_airport = origin_airport
        self.destination_city = destination_city
        self.destination_airport = destination_airport
        self.departure_date = departure_date
        self.return_date = return_date

    def __str__(self):
        """
        Returns a readable summary of the flight deal.
        """
        return (
            f"💸 ${self.price} | "
            f"{self.origin_city} ({self.origin_airport}) → "
            f"{self.destination_city} ({self.destination_airport})\n"
            f"📅 {self.departure_date} → {self.return_date}"
        )
