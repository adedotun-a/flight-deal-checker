import requests
import os

API_KEY = f"Bearer {os.environ['SHEETY_API_KEY']}"
ENDPOINT = os.environ['SHEETY_ENDPOINT']
HEADERS = {
    "Authorization": API_KEY,
    "Content-Type": "application/json"
}


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.response = requests.get(url=ENDPOINT, headers=HEADERS)
        self.response.raise_for_status()
        self.result = self.response.json()
        # self.result = {'prices': [{'city': 'Paris', 'iataCode': 'PAR', 'id': 2, 'lowestPrice': 54},
        #                           {'city': 'Berlin', 'iataCode': 'BER', 'id': 3, 'lowestPrice': 42},
        #                           {'city': 'Tokyo', 'iataCode': 'TYO', 'id': 4, 'lowestPrice': 485},
        #                           {'city': 'Sydney', 'iataCode': 'SYD', 'id': 5, 'lowestPrice': 551},
        #                           {'city': 'Istanbul', 'iataCode': 'IST', 'id': 6, 'lowestPrice': 95},
        #                           {'city': 'Kuala Lumpur', 'iataCode': 'KUL', 'id': 7, 'lowestPrice': 414},
        #                           {'city': 'New York', 'iataCode': 'NYC', 'id': 8, 'lowestPrice': 240},
        #                           {'city': 'San Francisco', 'iataCode': 'SFO', 'id': 9, 'lowestPrice': 260},
        #                           {'city': 'Cape Town', 'iataCode': 'CPT', 'id': 10, 'lowestPrice': 378}]}

        self.sheet_data = self.result['prices']

        # print(self.sheet_data)

    def get_sheet_data(self):
        return self.sheet_data

    def update_sheets(self, sheet_data):
        self.sheet_data = sheet_data
        for data in sheet_data:
            sheet_params = {"price": {key: val for (key, val) in data.items() if key == 'iataCode'}}
            response = requests.put(url=f"{ENDPOINT}/{data['id']}", json=sheet_params, headers=HEADERS)
            response.raise_for_status()
