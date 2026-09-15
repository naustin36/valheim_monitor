from pathlib import Path
import re

def monitor_log(log_path: Path) -> None:
    pass

def get_server_info(line: str) -> tuple[str, str, str]:
    # return timestamp, name of server, and server IP
    line_sections = line.split()
    server_timestamp = " ".join(line_sections[0:2])
    server_name = " ".join(line_sections[line_sections.index("server")+1:line_sections.index("with")])
    server_ip = line_sections[-1]
    return server_timestamp, server_name, server_ip

def get_join_code(line: str) -> tuple[str, str]:
    # return timestamp and PlayFab join code
    line_sections = line.split()
    return " ".join(line_sections[0:2]), line_sections[-1]

def update_player_count(line: str, regex_match) -> tuple[str, str, int]:
    split_line = line.split()
    timestamp = " ".join(split_line[0:2])
    update_event = " ".join(split_line[2:5])
    player_count = int(regex_match.group(1))
    return timestamp, update_event, player_count
