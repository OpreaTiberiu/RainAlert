import requests
from dotenv import load_dotenv
from twilio.rest import Client
from datetime import datetime
import os

load_dotenv()
MY_LAT = 6.524379  # 44.426765  # Your latitude
MY_LONG = 3.379206  # 26.102537  # Your longitude


def send_sms():
    account_sid = os.environ['twilio_sid']
    auth_token = os.environ['twilio_api_key']
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body="It is going to rain. Bring an umbrella ☂️!",
        from_="+18149628062",
        to=os.environ["phone_number"]
    )

    print(message.sid)


uri = "https://api.openweathermap.org/data/2.5/forecast"
params = {
    "lat": MY_LAT,
    "lon": MY_LONG,
    "appid": os.environ['key'],
    "units": "metric"

}
weather_list = requests.get(uri, params=params).json()["list"]

for w in weather_list:
    code = int(w['weather'][0]['id'])

    date_string = w['dt_txt']
    format = "%Y-%m-%d %H:%M:%S"
    date = datetime.strptime(date_string, format)

    if code < 600 and datetime.now().day + 1 == date.day:
        print(f"Bring umbrella for {w['dt_txt']}")
        send_sms()
        break
