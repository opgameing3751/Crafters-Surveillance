import os
import time
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta


load_dotenv("Settings.env")
API_KEY = os.getenv("API_KEY")


Title_color = os.getenv("Title_color", "\033[33m")  # Yellow
Username_color = os.getenv("Username_color", "\033[32m")  # Green
time_color = os.getenv("time_color", "\033[37m")  # White


base_url = "https://crafters.one/api/v1/stats/world"


online_timers = {}

def clear_terminal():
    """Clears the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")

while True:
    try:
        headers = {'X-API-KEY': API_KEY}
        response = requests.get(url=base_url, headers=headers)

        if response.status_code == 200:
            data = response.json()  # Convert response to JSON
            current_players = data.get("online_players", [])

            # Clear the terminal before printing the latest info
            clear_terminal()

            # Check each online player
            for player in current_players:
                if player not in online_timers:
                    # New player detected, store login time
                    online_timers[player] = datetime.now()

            # Display online players and their duration
            print(f"🌍 {Title_color}\033[1mOnline Players:\033[0m")
            for player in current_players:
                login_time = online_timers[player]
                time_online = datetime.now() - login_time
                formatted_time = str(timedelta(seconds=int(time_online.total_seconds())))
                print(f" - {Username_color}{player}\033[0m | Online for: {time_color}{formatted_time}\033[0m")

            # Remove players who have logged off
            for player in list(online_timers.keys()):
                if player not in current_players:
                    del online_timers[player]

        else:
            print(f"\033[31mError: Received status code {response.status_code}\033[0m Is there no API key? or is the API down?")  # Red Error Message

    except Exception as e:
        print(f"\033[31mAn error occurred: {e}\033[0m")  # Red Error Message

    time.sleep(1)