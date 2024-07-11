# RAIN SAFE v1 By Shaluka Manodya
# 2024-July-07

import os
import time
import requests
import schedule
from dotenv import load_dotenv
from urllib.parse import quote


load_dotenv()


# Assigning credentials to call openweather and textit.biz API's

# textit.biz

user = os.getenv('USER')
pw = os.getenv('PW')

# Open weather api

api = os.getenv('APIKEY')
url = f"https://api.openweathermap.org/data/2.5/weather?q=Nugegoda,LK&appid={api}&units=metric"

# Status Values
send_code = False
send_code2 = False

def main_app():

    global send_code, send_code2

    # Retrieving data from open weather api
    def current_weather(url):
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            # Storing the values from the response
            current_status = data['weather'][0]['main']
            weather_desc = data['weather'][0]['description']
            humidity = data['main']['humidity']
            temp = data['main']['temp']

            return current_status, humidity, weather_desc, temp
        
        else:
            print("Data retrieval unsuccessful")  

    

    #getting the returned values
    status = current_weather(url)     

    # Checking conditions whether its raining or not
    if status[0] == "Rain":
        
        while not send_code:
            # sms alert is sent 3 times
            times = 0
            while times < 3:
                print("Its raining...")
                # Sending the sms alert using the gateway
                url_alert=quote(f"!!!!RAIN SAFE ALERT!!!! Please take your clothes, It's RAINING outside. Current Weather: {status[0]}, Description: {status[2]}, Humidity: {status[1]}, Tempreture: {status[3]}")

                sms_gateway = f"https://www.textit.biz/sendmsg?id={user}&pw={pw}&to=0787785324&text={url_alert}"

                requests.post(sms_gateway)
                times += 1
                time.sleep(10)

                # Trigger is Set to send sms only once    
            send_code = True
        print(f"Trigger Running, Current Weather: {status[0]}, Description: {status[2]}, Humidity: {status[1]}, Tempreture: {status[3]}") 

    elif status[1] > 80:
        
        while not send_code2:
                times2 = 0
                while times2 < 2:
                    url_alert=quote(f"!!!!RAIN SAFE ALERT!!!! Please be in alert, It may rain in the following hours. Current Weather: {status[0]}, Description: {status[2]}, Humidity: {status[1]}, Tempreture: {status[3]}")

                    sms_gateway = f"https://www.textit.biz/sendmsg?id={user}&pw={pw}&to=0787785324&text={url_alert}"

                    requests.post(sms_gateway)

                    times2 += 1
                    time.sleep(10)

                send_code2 = True
        print(f"Trigger Running, Current Weather: {status[0]}, Description: {status[2]}, Humidity: {status[1]}, Tempreture: {status[3]}")

    else:
        # if no rain is detected the trigger will stay doment
        print(f"Trigger Running, Current Weather: {status[0]}, Description: {status[2]}, Humidity: {status[1]}, Tempreture: {status[3]}") 
        if send_code == True:
            send_code = not send_code 
        elif send_code2 == True:
            send_code2 = not send_code2 
# Application is running every minute
main_app()
schedule.every(1).minutes.do(main_app)

while True:
        schedule.run_pending()
        time.sleep(1)



    


   
