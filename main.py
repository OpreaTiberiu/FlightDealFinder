from data_manager import DataManager
from dotenv import load_dotenv
from flight_search import *
from notification_manager import send_sms

load_dotenv()

data_manager = DataManager()
data = data_manager.get_data()
data_manager.set_iata_codes(get_iata_codes())
cities = [x["city"] for x in data_manager.get_data()]
flights = get_flights(cities)

for flight in flights:
    for d in data:
        if d["city"] == flight.destination_city:
            if flight.price < d["lowestPrice"]:
                send_sms(flight)
                data_manager.update_price({flight.destination_city: flight.price})





