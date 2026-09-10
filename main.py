import time
from pathlib import Path
from config import *
from read_log import *

def main():
    print("Valheim Server Monitor")

    # load config, set path to server log, and verify that log exists
    config = load_config()
    log_path = Path(config["log_path"])

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
            print(line)

if __name__ == "__main__":
    main()
