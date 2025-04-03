import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("MY_EMAIL")
PASSWORD = os.getenv("MY_EMAIL_PASSWORD")

class NotificationManager:
    def send_email(self, flight_data):
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=EMAIL, password=PASSWORD)
            
            subject = f"Low price alert! Only ${flight_data.price} to {flight_data.destination_city}"
            body = (
                f"Cheap flight found!\n\n"
                f"{flight_data.origin_city} ({flight_data.origin_airport}) -> "
                f"{flight_data.destination_city} ({flight_data.destination_airport})\n"
                f"Price: ${flight_data.price}\n"
                f"From {flight_data.departure_date} to {flight_data.return_date}"
            )
            message = f"Subject: {subject}\n\n{body}"
            connection.sendmail(from_addr=EMAIL, to_addrs=EMAIL, msg=message)
