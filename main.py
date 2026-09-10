from pathlib import Path
from config import *

def main():
    print("Valheim Server Monitor")

    config = load_config()

    print(f"log file located at: {config["log_path"]}")

if __name__ == "__main__":
    main()
