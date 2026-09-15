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

    player_count: int = 0
    wrong_password_flag = False
    #count_pattern = re.compile(r"now (\d+) player\(s\)")
    shutdown_pattern = re.compile(r"Game - OnApplicationQuit")
    connection_pattern = re.compile(r"^\S+\s+\S+\s+(\w+\s+\w+\s+\w+) .*, now (\d+) player\(s\)")
    connection_check_pattern = re.compile(r"Connections (\d+) ZDOS:\d+\s+sent:\d+ recv:\d+")
    event_patterns = [
        (
            re.compile(r'Register PlayFab server "([^"]+)" with IP (\S+)'),
            "Registering PlayFab server {} with IP {}..."
        ),
        (
            re.compile(r'Session "([^"]+)" with join code (\d+) and IP (\S+)'),
            "Session {} active! Join code: {} IP: {}"
        ),
        (
            re.compile(r'PlayFab network error in session'),
            "PlayFab network error!"
        ),
        (
            re.compile(r"with type '([^']+)' and code '(\d+)'"),
            "{} code: {}"
        ),
        (
            re.compile(r"Joined PlayFab Party network"),
            "Joined PlayFab Party network"
        ),
        (
            re.compile(r"Game server connected"),
            "Game server connected"
        ),
    ]

    print(f"Loading log at {log_path}...")
    with open(log_path, "r") as f:
        while True:
            # Read each line in log file, from the top
            line = f.readline()

            # If there are no more lines, wait for a new one
            if not line:
                time.sleep(1)
                continue

            # Process the line
            # Check for server related events
            for pattern, message in event_patterns:
                match = pattern.search(line)
                if match:
                    print(" ".join(line.split()[0:2]), message.format(*match.groups()))

            # Check for connection events
            # If a wrong password event is detected, set flag and decrement player count manually. Valheim does not log this correctly.
            if "has wrong password" in line:
                print(f"{" ".join(line.split()[0:2])} Failed to join: Wrong password")
                wrong_password_flag = True
            match =  connection_pattern.search(line)
            if match:
                player_count = int(match.group(2))
                if wrong_password_flag == True:
                    player_count = max(0, player_count - 1)
                    wrong_password_flag = False
                print(f"{" ".join(line.split()[0:2])} {match.group(1)}! Current player count: {player_count}")

            match = connection_check_pattern.search(line)
            if match and int(match.group(1)) != player_count:
                player_count = int(match.group(1))
                print(f"Connection count mismatch: Corrected current player count to {player_count}")


            match = shutdown_pattern.search(line)
            if match:
                print("Server Shutdown")
                return
            #player_count_updated = count_pattern.search(line)
            #if player_count_updated:
            #    timestamp, update_event, player_count = update_player_count(line, player_count_updated)
            #    print(f"{timestamp} {update_event}! Current player count: {player_count}")

            #if "Game - OnApplicationQuit" in line:
            #    print(f"{" ".join(line.split()[0:2])} Server Offline")
            #    return

if __name__ == "__main__":
    main()
