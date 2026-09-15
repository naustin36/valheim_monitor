import time
from pathlib import Path
from config import *
from parse_log import *
import re

def main():
    print("Valheim Crossplay Server Monitor")

    # load config, set path to server log, and verify that log exists
    config = load_config()
    log_path = Path(config["log_path"])
    if not log_path.exists():
        print("Log file not found, please configure in config.json")
        return

    print(f"Loading log at {log_path}...")

    player_count: int = 0
    count_pattern = re.compile(r"now (\d+) player\(s\)")
    event_patterns = [
        (
            re.compile(r'Register PlayFab server "([^"]+)"'),
            "Register PlayFab server {}"
        ),
        (
            re.compile(r'Session "([^"]+)" registered with join code (\d+)'),
            "Session {} registered with join code {}"
        ),
        (
            re.compile(r'PlayFab network error in session'),
            "PlayFab network error in session!"
        ),
        (
            re.compile(r"with type '([^']+)' and code '(\d+)'"),
            "{} code: {}"
        ),
        (
            re.compile(r"Joined PlayFab Party network"),
            "Joined PlayFab Party network"
        )
    ]

    with open(log_path, "r") as f:
        while True:
            # Read each line in log file, from the top
            line = f.readline()

            # If there are no more lines, wait for a new one
            if not line:
                time.sleep(1)
                continue

            # Process the line
            if "Game server connected" in line:
               print(f"{" ".join(line.split()[0:2])} Game server connected")

            for pattern, message in event_patterns:
                match = pattern.search(line)
                if match:
                    print(" ".join(line.split()[0:2]), message.format(*match.groups()))

            player_count_updated = count_pattern.search(line)
            if player_count_updated:
                timestamp, update_event, player_count = update_player_count(line, player_count_updated)
                print(f"{timestamp} {update_event}! Current player count: {player_count}")

            if "Game - OnApplicationQuit" in line:
                print(f"{" ".join(line.split()[0:2])} Server Offline")
                return

if __name__ == "__main__":
    main()
