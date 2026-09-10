from pathlib import Path
from config import *
from read_log import *

def main():
    print("Valheim Server Monitor")

    # load config, set path to server log, and verify that log exists
    config = load_config()
    log_path = Path(config["log_path"])

    print(f"Loading log at {log_path}...")
    try:
        log = read_log(log_path)
        print("".join(log[-5:]))
    except OSError as e:
        print(e)
        print("Please verify that the log path is correctly set in config.json")

if __name__ == "__main__":
    main()
