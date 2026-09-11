import time
from pathlib import Path
from config import *
from parse_log import *

def main():
    print("Valheim Server Monitor")

    # load config, set path to server log, and verify that log exists
    config = load_config()
    log_path = Path(config["log_path"])
    if not log_path.exists():
        print("Log file not found, please configure in config.json")
        return

    print(f"Loading log at {log_path}...")

    num_connections = 0
    server_name = ""

    with open(log_path, "r") as f:
        while True:
            # Read each line in log file, from the top
            line = f.readline()

            # If there are no more lines, wait for a new one
            if not line:
                time.sleep(1)
                continue

            # Process the line
            if "Register PlayFab server" in line:
                server_timestamp, server_name, server_ip = get_server_info(line)
                print(f"{server_timestamp} Server Online with Name {server_name} with IP {server_ip}")
            if f"Session {server_name} registered" in line:
                timestamp, join_code = get_join_code(line)
                print(f"{timestamp} PlayFab join code: {join_code}")

            if "Player joined server" in line:
                num_connections += 1
                print(f"Player Joined! Total connected: {num_connections}")

            if "Player connection lost" in line:
                num_connections -= 1
                print(f"Player left! Total connected: {num_connections}")

if __name__ == "__main__":
    main()
