import os
from twilio.rest import Client

from flight_data import FlightData


def send_sms(flight_data: FlightData):
    body = f'''
        You have a new lowest price flight from {flight_data.origin_city} to {flight_data.destination_city}.
        Price: {flight_data.price}
    '''

    account_sid = os.environ['twilio_sid']
    auth_token = os.environ['twilio_api_key']
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=body,
        from_="+18149628062",
        to=os.environ["phone_number"]
    )

    print(message.status)

    print(body + "\n\n")
