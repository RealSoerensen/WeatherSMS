import time
import schedule
from schedule import repeat
from main import app, db
from models import User
import requests
from inspect import cleandoc
import os
from twilio.rest import Client

BASE = "http://api.openweathermap.org/data/2.5/weather?"
client = Client(os.environ['SID'], os.environ['TOKEN'])


def get_weather(city: str):
    complete_url = f"{BASE}appid={os.environ['WEATHER_TOKEN']}&q={city}&units=metric"
    response = requests.get(complete_url)
    r = response.json()
    if r["cod"] == "404":
        return "The city registered with this number is invalid.\nPlease opt-out on https://WeatherSMS.soerensen.repl.co and re-register with the correct information."

    main = r["main"]

    # print following values
    return cleandoc(f"""
\nGood morning! Here are todays weather forcast for {city}:
There is {r["weather"][0]["description"]} today!
The temperature is between {str(round(int(main["temp_min"])))} and {str(round(int(main["temp_max"])))} degrees Celsius.
The pressure is {main["pressure"]} hPa.
The humidity is {main["humidity"]}%.
The wind speed is {r["wind"]["speed"]} m/s.

Opt-out here: https://WeatherSMS.soerensen.repl.co""")


@repeat(schedule.every().day.at("06:00:00"))
def send_sms():
    with app.app_context():
        for user in db.session.query(User).all():
            try:
                body = get_weather(user.city)
            except Exception:
                body = "Good morning! Unfortunately, I was unable to fetch todays weather. I will try again tomorrow!"

            try:
                client.messages \
                    .create(
                         body=body,
                         from_=os.environ["SENDING_NUM"],
                         to=user.number
                     )
            except Exception:
              pass


def scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)
