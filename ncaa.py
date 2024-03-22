import requests
import json
from datetime import datetime
import pytz


def get_games():
    # Get the current time in UTC
    utc_now = datetime.utcnow()

    # Define the time zone for Central Time
    central_tz = pytz.timezone('America/Chicago')

    # Convert UTC time to Central Time
    central_now = utc_now.replace(tzinfo=pytz.utc).astimezone(central_tz)

    # Extract only the date
    central_today = central_now.date()

    today = central_today.strftime('%A, %b %d')

    url = f"https://data.ncaa.com/casablanca/scoreboard/basketball-men/d1/2024/{today}/scoreboard.json"

    try:
        # Send GET request to the API
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Extract JSON data from the response
            data = response.json()
            games = data['games']

            # Now you can work with the JSON data as needed
            return games
        else:
            print("Failed to retrieve data. Status code:", response.status_code)
            return {}

    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
        return {}