import requests
import json
from datetime import datetime


def get_games():
    today = datetime.today().date()
    today = today.strftime("%m/%d")

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