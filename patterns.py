import re
shutdown_pattern: re.Pattern = re.compile(r"Game - OnApplicationQuit")
# Grab the first three words after the timestamp that describe a connection event, and the updated number of players
connection_pattern: re.Pattern = re.compile(r"^\S+\s+\S+\s+(\w+\s+\w+\s+\w+) .*, now (\d+) player\(s\)")
connection_check_pattern: re.Pattern = re.compile(r"Connections (\d+) ZDOS:\d+\s+sent:\d+ recv:\d+")
server_info_pattern: re.Pattern = re.compile(r'Session "([^"]+)" with join code (\d+) and IP (\S+)')
playfab_error_pattern: re.Pattern = re.compile(r"with type '([^']+)' and code '(\d+)'")
playfab_socket_timeout_pattern: re.Pattern = re.compile(r"ZRpc timeout detected")
playfab_connection_pattern: re.Pattern = re.compile(r"Joined PlayFab Party network")
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
        re.compile(r"Game server (.*)"),
        "Game server {}"
    )
]
