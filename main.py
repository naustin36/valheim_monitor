import time
from pathlib import Path
from config import *
import re

def main():
    print("Valheim Crossplay Server Monitor")

    # load config, set path to server log, and verify that log exists
    config: dict = load_config()
    log_path = Path(config["log_path"])
    if not log_path.exists():
        print("Log file not found, please configure in config.json")
        return

    # set global variables and regex patterns
    player_count: int = 0
    wrong_password_flag: bool = False
    shutdown_pattern: re.Pattern = re.compile(r"Game - OnApplicationQuit")
    # Grab the first three words after the timestamp that describe a connection event, and the updated number of players
    connection_pattern: re.Pattern = re.compile(r"^\S+\s+\S+\s+(\w+\s+\w+\s+\w+) .*, now (\d+) player\(s\)")
    connection_check_pattern: re.Pattern = re.compile(r"Connections (\d+) ZDOS:\d+\s+sent:\d+ recv:\d+")
    event_patterns: list[tuple[re.Pattern, str]] = [
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
            re.compile(r"Game server (.*)"),
            "Game server {}"
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
            timestamp = " ".join(line.split()[0:2])
            # Check for server related events
            for pattern, message in event_patterns:
                match = pattern.search(line)
                if match:
                    print(timestamp, message.format(*match.groups()))

            # Check for connection events
            # If a wrong password event is detected, set flag and decrement player count manually. Valheim does not log this correctly.
            if "has wrong password" in line:
                print(f"{timestamp} Failed to join: Wrong password")
                wrong_password_flag = True
            match =  connection_pattern.search(line)
            if match:
                player_count = int(match.group(2))
                if wrong_password_flag == True:
                    player_count = max(0, player_count - 1)
                    wrong_password_flag = False
                print(f"{timestamp} {match.group(1)}! Current player count: {player_count}")

            # Check current players against server heartbeat report and update if needed
            match = connection_check_pattern.search(line)
            if match and int(match.group(1)) != player_count:
                print(f"{timestamp} Player count mismatch: Corrected current player count from {player_count} to {int(match.group(1))}")
                player_count = int(match.group(1))

            match = shutdown_pattern.search(line)
            if match:
                print("Server Shutdown")
                return

if __name__ == "__main__":
    main()
