import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Assigning credentials to call openweather and textit.biz API's

# Open weather api

api = os.getenv('APIKEY')
url = f"https://api.openweathermap.org/data/2.5/weather?q=Nugegoda,LK&appid={api}&units=metric"

# textit.biz

user = os.getenv('USER')
pw = os.getenv('PW')

# Retrieving data from open weather api

def current_weather(url):
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        current_status = data['weather'][0]['main']
        humidity = data['main']['humidity']

        print(current_status, humidity)
        

current_weather(url)        
