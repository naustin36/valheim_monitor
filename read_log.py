from pathlib import Path

def read_log(log_path: Path) -> list[str]:
    with open(log_path, "r") as f:
        return f.readlines()
