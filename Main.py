import subprocess
import sys
import argparse
# ANSI color codes
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
RESET = "\033[0m"

# List of required packages
required_packages = ["requests", "python-dotenv, dotenv"]

def install_package(package):
    """Install a package using pip, optionally with --break-system-packages."""
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

Title_color = os.getenv("Title_color", "\033[33m")  # Yellow
Username_color = os.getenv("Username_color", "\033[32m")  # Green
time_color = os.getenv("time_color", "\033[37m")  # White

base_url = "https://crafters.one/api/v1/stats/world"
online_timers = {}

response = requests.get(url="http://Stats.galaticadam.com:8000")
if response.status_code == 200:
    data = response.json()
    for player, time_online in data.items():
        hours, minutes, seconds = map(int, time_online.split(":"))
        time_duration = timedelta(hours=hours, minutes=minutes, seconds=seconds)
        online_timers[player] = time_duration
else:
    print(f"\033[31mError: Received status code {response.status_code} From the Crafters.one.Player.Statistics bot: waiting 5 seconds before continuing\033[0m")
    time.sleep(5)


def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")


while True:
    try:
        headers = {'X-API-KEY': API_KEY}
        response = requests.get(url=base_url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            current_players = data.get("online_players", [])

            clear_terminal()
            print(f"🌍 {Title_color}\033[1mOnline Players:\033[0m")

            if not current_players:
                print(f"{time_color}No players online\033[0m")
            else:
                for player in current_players:
                    if player not in online_timers:
                        online_timers[player] = datetime.now()

                    login_time = online_timers[player]
                    if isinstance(login_time, datetime):
                        time_online = datetime.now() - login_time
                    else:
                        time_online = login_time + timedelta(seconds=1)
                        online_timers[player] = time_online

                    formatted_time = str(timedelta(seconds=int(time_online.total_seconds())))
                    print(f" - {Username_color}{player}\033[0m | Online for: {time_color}{formatted_time}\033[0m")

            # Remove players who went offline
            for player in list(online_timers.keys()):
                if player not in current_players:
                    del online_timers[player]

        else:
            print(f"\033[31mError: Received status code {response.status_code}\033[0m Is there no API key? or is the API down?")

    except Exception as e:
        print(f"\033[31mAn error occurred: {e}\033[0m")

    time.sleep(int(os.getenv("update_delay")))
