import re
shutdown_pattern: re.Pattern = re.compile(r"Game - OnApplicationQuit")
server_info_pattern: re.Pattern = re.compile(r'Session "([^"]+)" with join code (\d+) and IP (\S+)')
playfab_error_pattern: re.Pattern = re.compile(r"with type '([^']+)' and code '(\d+)'")
server_crash_pattern: re.Pattern = re.compile(r"Crash!!!")
player_zdoID_created_pattern: re.Pattern = re.compile(r"Got character ZDOID from (.*) : (\S+)")
player_zdoID_destroyed_pattern: re.Pattern = re.compile(r"Destroying abandoned non persistent zdo (\S+)")
server_status_pattern: re.Pattern = re.compile(r"Game server (.*)")
event_patterns: list[tuple[re.Pattern, str]] = [
    (
        re.compile(r'Register PlayFab server "([^"]+)" with IP (\S+)'),
        "Registering PlayFab server {} with IP {}..."
    ),
    (
        re.compile(r'Session "([^"]+)" with join code (\d+) and IP (\S+)'),
        "Session {} active! Join code: {} IP: {}"
    )
]
