import subprocess
import sys
import argparse
import threading

# ANSI color codes
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
RESET = "\033[0m"

required_packages = ["requests", "python-dotenv"]

def install_package(package):
    try:
        command = [sys.executable, "-m", "pip", "install", package]
        command.append("--break-system-packages")
        
        subprocess.check_call(command)
        print(f"{GREEN}Successfully installed: {package}{RESET}")
    except subprocess.CalledProcessError:
        print(f"{RED}Failed to install: {package}{RESET}")


try:
    import os
    import time
    import requests
    from dotenv import load_dotenv
    from datetime import datetime, timedelta
except:
    for package in required_packages:
        try:
            __import__(package)
            print(f"{GREEN}{package} is already installed.{RESET}")
        except ImportError:
            print(f"{YELLOW}Installing {package}...{RESET}")
            install_package(package)
    import os
    import time
    import requests
    from dotenv import load_dotenv
    from datetime import datetime, timedelta


load_dotenv("Settings.env")
API_KEY = os.getenv("API_KEY")
try:
    sleep_delay = int(os.getenv("update_delay", 5))
except:
    sleep_delay = None
api_update_interval = int(os.getenv("api_update_interval", 10))  # New variable

Title_color = os.getenv("Title_color", "\033[33m")  # Yellow
Username_color = os.getenv("Username_color", "\033[32m")  # Green
time_color = os.getenv("time_color", "\033[37m")  # White

base_url = "https://crafters.one/api/v1/stats/world"
online_timers = {}
latest_data = {
    "online_players": [],
    "time_of_day": "",
    "weather_overworld": "",
}

def fetch_api_data():
    """Fetch data from the API at a fixed interval."""
    global latest_data
    while True:
        try:
            headers = {'X-API-KEY': API_KEY}
            response = requests.get(url=base_url, headers=headers)

            if response.status_code == 200:
                latest_data = response.json()
            else:
                print(f"\033[31mError: Received status code {response.status_code} from the API.\033[0m")
        except Exception as e:
            print(f"\033[31mAn error occurred while fetching API data: {e}\033[0m")

        time.sleep(api_update_interval)  # Update interval from settings.env


# Initial API Call to Fetch Player Uptime
current_players_timp = []

try:
    response = requests.get(url="http://Stats.galaticadam.com:8000", timeout=3)
    if response.status_code == 200:
        data = response.json()
        for player, time_online in data.items():
            hours, minutes, seconds = map(int, time_online.split(":"))
            time_duration = timedelta(hours=hours, minutes=minutes, seconds=seconds)
            online_timers[player] = time_duration
            current_players_timp.append(player)
    else:
        print(f"{RED}Error: Status {response.status_code} from Crafters.one Player Statistics bot. Waiting 5 seconds...{RESET}\nContinuing in 5 seconds")
except Exception as e:
    print(f"{RED}Failed to fetch initial player uptime: {e}{RESET}\nContinuing in 5 seconds")
finally:
    time.sleep(5)  # Either way, pause a bit before continuing


# Start the API fetcher thread
api_thread = threading.Thread(target=fetch_api_data, daemon=True)
api_thread.start()


def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")


while True:
    try:
        if current_players_timp != None:
            current_players = current_players_timp
            current_players_timp = None
        else:
            current_players = latest_data.get("online_players", [])
        time_of_day = latest_data.get("time_of_day", "")
        weather = latest_data.get("weather_overworld", "")

        clear_terminal()
        print(f"🌍 {Title_color}\033[1mOnline Players:\033[0m")

        if not current_players:
            print(f"{time_color}No players online\033[0m")
        else:
            for player in current_players:
                if player not in online_timers:
                    # Convert timedelta to datetime
                    online_timers[player] = datetime.now() - online_timers.get(player, timedelta(0))

                login_time = online_timers[player]

                if isinstance(login_time, datetime):
                    time_online = datetime.now() - login_time
                else:
                    time_online = timedelta(seconds=int(login_time.total_seconds()) + 1)
                    online_timers[player] = time_online

                formatted_time = str(timedelta(seconds=int(time_online.total_seconds())))
                print(f" - {Username_color}{player}\033[0m | Online for: {time_color}{formatted_time}\033[0m")

        # Remove players who went offline
        for player in list(online_timers.keys()):
            if player not in current_players:
                del online_timers[player]

        print(f"\n\n🌍 {Title_color}\033[1mWorld State\033[0m")
        print(f" - {Username_color}Time of day\033[0m | {time_of_day}")
        print(f" - {Username_color}Current Weather\033[0m | {weather}")

    except Exception as e:
        print(f"\033[31mAn error occurred: {e}\033[0m")

    if sleep_delay != None:
        time.sleep(sleep_delay)  # Main loop delay
