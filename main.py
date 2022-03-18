# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the
# program requirements.
from pprint import pprint
from data_manager import DataManager
from flight_search import FlightSearch
import datetime as dt

from notification_manager import NotificationManager

DEPARTURE = "LON"

today = dt.datetime.today()
today_date = today.strftime("%d/%m/%Y")
month_6 = today + dt.timedelta(days=6*30)
return_date = month_6.strftime("%d/%m/%Y")

data_manager = DataManager()

sheet_data = data_manager.get_sheet_data()
flight_search = FlightSearch()

notification_manager = NotificationManager()


def check_codes():
    for data in sheet_data:
        if data['iataCode'] == "":
            # return False
            data['iataCode'] = flight_search.get_iata(data['city'])


def search_flights():
    for data in sheet_data:
        flight = flight_search.get_flights(DEPARTURE, data['iataCode'], today_date, return_date)
        if flight and flight.price < data["lowestPrice"]:
            msg = f"Low price alert! Only £{flight.price} to fly from " \
                  f"{flight.origin_city}-{flight.origin_airport} to " \
                  f"{flight.destination_city}-{flight.destination_airport}, " \
                  f"from {flight.out_date} to {flight.return_date} "
            notification_manager.send_sms(msg)


search_flights()
