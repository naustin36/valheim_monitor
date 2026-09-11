from pathlib import Path

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
