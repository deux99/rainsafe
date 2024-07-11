# RAIN SAFE v1

**By Shaluka Manodya**

**Date: 2024-July-07**

RAIN SAFE is a Python application that monitors weather conditions in Nugegoda, Sri Lanka, using the OpenWeatherMap API. It sends SMS alerts via the Textit.biz SMS gateway when it detects rain or high humidity, ensuring that users can take action, such as bringing clothes inside before it rains.

## Features

- Fetches current weather data from OpenWeatherMap.
- Sends SMS alerts for rain and high humidity.
- Uses environment variables for API credentials.
- Runs continuously, checking the weather every minute.
- Limits SMS alerts to avoid repeated messages.

## Prerequisites

- Python 3.6+
- Requests library
- Dotenv library
- Schedule library
- An account with OpenWeatherMap for API access.
- An account with Textit.biz for SMS sending.

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/deux99/rainsafe.git
    cd rainsafe
    ```

2. Install the required Python libraries:

    ```sh
    pip install requests python-dotenv schedule
    ```

3. Create a `.env` file in the project directory with your API credentials:

    ```env
    APIKEY=your_openweather_api_key
    USER=your_textit_user_id
    PW=your_textit_password
    ```

## Usage

1. Open `rain_safe.py` in a text editor and modify the phone number in the `sms_gateway` URL to your desired recipient.

2. Run the application:

    ```sh
    python rain_safe.py
    ```

## Code Overview

### Importing Required Libraries

```python
import os
import time
import requests
import schedule
from dotenv import load_dotenv
from urllib.parse import quote
```

### Loading Environment Variables

```python
load_dotenv()
```

### Assigning Credentials

```python
user = os.getenv('USER')
pw = os.getenv('PW')
api = os.getenv('APIKEY')
url = f"https://api.openweathermap.org/data/2.5/weather?q=Nugegoda,LK&appid={api}&units=metric"
```

### Main Application Function

```python
def main_app():
    send_code = False
    send_code2 = False

    def current_weather(url):
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            current_status = data['weather'][0]['main']
            weather_desc = data['weather'][0]['description']
            humidity = data['main']['humidity']
            temp = data['main']['temp']
            return current_status, humidity, weather_desc, temp
        else:
            print("Data retrieval unsuccessful")

    status = current_weather(url)

    if status[0] == "Rain":
        times = 0
        while send_code == False:
            while times <= 3:
                print("Its raining...")
                url_alert=quote(f"!!!!RAIN SAFE ALERT!!!! Please take your clothes, It's RAINING outside. Current Weather: {status[0]}, Description: {status[2]}, Humidity: {status[1]}, Temperature: {status[3]}")
                sms_gateway = f"https://www.textit.biz/sendmsg?id={user}&pw={pw}&to=0787785324&text={url_alert}"
                requests.post(sms_gateway)
                times = times + 1
                time.sleep(60)
            send_code = True

    elif status[1] > 80:
        times2 = 0
        while send_code2 == False:
            while times2 <= 2:
                url_alert=quote(f"!!!!RAIN SAFE ALERT!!!! Please be in alert, It may rain in the following hours. Current Weather: {status[0]}, Description: {status[2]}, Humidity: {status[1]}, Temperature: {status[3]}")
                sms_gateway = f"https://www.textit.biz/sendmsg?id={user}&pw={pw}&to=0787785324&text={url_alert}"
                requests.post(sms_gateway)
                times2 = times2 + 1
                time.sleep(60)
            send_code2 = True

    else:
        print(f"Trigger Running, Current Weather: {status[0]}, Description: {status[2]}, Humidity: {status[1]}, Temperature: {status[3]}")
        if send_code == True:
            send_code = not send_code 
        elif send_code2 == True:
            send_code2 = not send_code2 
```

### Scheduling the Application

```python
main_app()
schedule.every(1).minutes.do(main_app)

while True:
    schedule.run_pending()
    time.sleep(1)
```

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## License

This project is licensed under the [MIT License](./license.md) - see the license file for details.

## Contact

For any inquiries, please contact Shaluka Manodya at Shalukamahagamage@gmail.com