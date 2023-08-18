import os
import requests
from datetime import datetime, timedelta
from flight_data import FlightData

def get_iata_codes():
    uri = "https://api.tequila.kiwi.com/locations/dump"
    params = {
        "locale": "en-US",
        "location_types": "city",
        "active_only": "true",
        "limit": "500"
    }
    header = {
        "accept": "application/json",
        "apikey": os.environ["kiwi_api_key"]
    }
    r = requests.get(url=uri, params=params, headers=header)
    iata_codes_data = r.json().get("locations")
    iata_codes_dict = {e["name"]: e["code"] for e in iata_codes_data}
    return iata_codes_dict



def get_flights(cities: list):
    uri = "https://api.tequila.kiwi.com"
    headers = {"apikey": os.environ["kiwi_api_key"]}

    today_string = datetime.now().strftime("%d/%m/%Y")
    max_search_string = (datetime.now() + timedelta(weeks=24)).strftime("%d/%m/%Y")

    query = {
        "fly_from": "BUH",
        "date_from": today_string,
        "date_to": max_search_string,
        "nights_in_dst_from": 7,
        "nights_in_dst_to": 9,
        "flight_type": "round",
        "one_for_city": 1,
        "max_stopovers": 3,
        "curr": "RON"
    }

    response = requests.get(
        url=f"{uri}/v2/search",
        headers=headers,
        params=query,
    )

    response.raise_for_status()

    data = response.json()["data"]

    if len(data) > 0:
        result = []
        for flight in data:
            if flight["cityTo"] in cities:
                flight_data = FlightData(
                    price=flight["price"],
                    origin_city=flight["cityFrom"],
                    origin_airport=flight["flyFrom"],
                    destination_city=flight["cityTo"],
                    destination_airport=flight["flyTo"],
                    out_date=flight["local_departure"].split("T")[0],
                    return_date=flight["local_departure"].split("T")[0]
                )
                result.append(flight_data)
                print(f"{flight_data.destination_city}: RON{flight_data.price}")
        return result
    return None
