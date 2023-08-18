import requests
import os


class DataManager:
    def __init__(self):
        self.uri = f"https://api.sheety.co/{os.environ['sheety_id']}/flights/flights"
        self.header = {
            "Authorization": f"Bearer {os.environ['sheety_api_key']}"
        }
        self.data = []
        self.get_data()

    def get_data(self):
        if not len(self.data) > 0:
            r = requests.get(url=self.uri, headers=self.header)
            r.raise_for_status()
            self.data = r.json().get("flights")
        return self.data

    def update_data(self, element: dict):
        update_uri = f"{self.uri}/{element['id']}"
        body = {"flight": element}
        r = requests.put(url=update_uri, json=body, headers=self.header)
        r.raise_for_status()
        print(r.text)

    def set_iata_codes(self, codes):
        for index in range(len(self.data)):
            if not self.data[index]["iataCode"] and self.data[index]["city"] in codes.keys():
                self.data[index]["iataCode"] = codes[self.data[index]["city"]]
                self.update_data(self.data[index])

    def update_price(self, value: dict):
        for index in range(len(self.data)):
            if self.data[index]["city"] in value.keys():
                self.data[index]["lowestPrice"] = value[self.data[index]["city"]]
                self.update_data(self.data[index])
