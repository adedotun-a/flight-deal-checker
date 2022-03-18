import requests
import os
from flight_data import FlightData

LOCATION_ENDPOINT = os.environ['TEQUILA_LOCATION_ENDPOINT']
SEARCH_ENDPOINT = os.environ['TEQUILA_SEARCH_ENDPOINT']

API_KEY = os.environ['TEQUILA_API_KEY']

'TEQUILA_LOCATION_ENDPOINT=https://tequila-api.kiwi.com/locations/query'

HEADER = {"apikey": API_KEY}

NIGHTS_IN_DST_FROM = 7
NIGHTS_IN_DST_TO = 28
FLIGHT_TYPE = "round"

CURR = "GBP"


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    # pass

    def __init__(self):
        self.code = "TESTING"

    def get_iata(self, city_name):
        query = {
            "term": city_name,
            "location_types": "city",
            "limit": 1,
        }
        response = requests.get(url=LOCATION_ENDPOINT, headers=HEADER, params=query)
        response.raise_for_status()
        self.code = response.json()["locations"][0]["code"]
        # pprint(self.code)
        return self.code

    def get_flights(self, fly_from, fly_to, date_from, date_to):
        query = {
            "fly_from": fly_from,
            "fly_to": fly_to,
            "date_from": date_from,
            "date_to": date_to,
            "nights_in_dst_from": NIGHTS_IN_DST_FROM,
            "nights_in_dst_to": NIGHTS_IN_DST_TO,
            "flight_type": FLIGHT_TYPE,
            "curr": CURR,
            "vehicle_type": "aircraft",
            "sort": "price",
            "limit": 2,
        }
        response = requests.get(url=SEARCH_ENDPOINT, headers=HEADER, params=query)
        response.raise_for_status()
        result = response.json()["data"]
        if result:
            flight_data = FlightData(price=result[0]["price"],
                                     origin_city=result[0]["route"][0]["cityFrom"],
                                     origin_airport=result[0]["route"][0]["flyFrom"],
                                     destination_city=result[0]["route"][0]["cityTo"],
                                     destination_airport=result[0]["route"][0]["flyTo"],
                                     out_date=result[0]["route"][0]["local_departure"].split("T")[0],
                                     return_date=result[0]["route"][1]["local_departure"].split("T")[0]
                                     )
            print(f"{flight_data.destination_city}: £{flight_data.price}")
            return flight_data
        else:
            print(f"No flight found for {fly_from} to {fly_to}.")
            return None
        # print(self.code)

