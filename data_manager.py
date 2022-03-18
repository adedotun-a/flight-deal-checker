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

        self.sheet_data = self.result['prices']

    def get_sheet_data(self):
        return self.sheet_data

    def update_sheets(self, sheet_data):
        self.sheet_data = sheet_data
        for data in sheet_data:
            sheet_params = {"price": {key: val for (key, val) in data.items() if key == 'iataCode'}}
            response = requests.put(url=f"{ENDPOINT}/{data['id']}", json=sheet_params, headers=HEADERS)
            response.raise_for_status()
