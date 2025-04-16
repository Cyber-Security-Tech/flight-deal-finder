import smtplib
import os
from dotenv import load_dotenv

# 🔐 Load email credentials from .env file
load_dotenv()

EMAIL = os.getenv("MY_EMAIL")
PASSWORD = os.getenv("MY_EMAIL_PASSWORD")


class NotificationManager:
    """
    Responsible for sending flight deal alerts via email using SMTP.
    """

    def send_email(self, flight_data, to_email=EMAIL):
        """
        Sends an email notification with flight deal info.

        Args:
            flight_data (FlightData): A FlightData object containing deal details.
            to_email (str): Email address to send the alert to (defaults to sender).
        """
        try:
            with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
                connection.starttls()  # Encrypt the connection
                connection.login(user=EMAIL, password=PASSWORD)

                subject = f"✈️ Low price alert: ${flight_data.price} to {flight_data.destination_city}"
                body = (
                    f"Cheap flight found!\n\n"
                    f"{flight_data.origin_city} ({flight_data.origin_airport}) → "
                    f"{flight_data.destination_city} ({flight_data.destination_airport})\n"
                    f"Price: ${flight_data.price}\n"
                    f"Departure: {flight_data.departure_date} | Return: {flight_data.return_date}"
                )

                message = f"Subject: {subject}\n\n{body}"

                connection.sendmail(
                    from_addr=EMAIL,
                    to_addrs=to_email,
                    msg=message
                )

                print(f"📧 Email sent to {to_email}")

        except Exception as e:
            print(f"❌ Failed to send email: {e}")
