from pathlib import Path
import json
CONFIG_FILE = Path("config.json")
CONFIG_DEFAULT = {
    "log_path":""
}

def load_config() -> dict[str,str]:
    if not CONFIG_FILE.exists():
        print("No config file found. Creating config.json...")
        save_config(CONFIG_DEFAULT)
        return CONFIG_DEFAULT
    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)
    return config

def save_config(config) -> None:
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)
