from pathlib import Path
import json
CONFIG_FILE = Path("config.json")
CONFIG_DEFAULT = {
    "log_path":None
}

def load_config():
    if not CONFIG_FILE.exists():
        print("No config file found. Creating config.json...")
        save_config(CONFIG_DEFAULT)
        return CONFIG_DEFAULT
    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)
    return config

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)
