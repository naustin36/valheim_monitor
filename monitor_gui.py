from tkinter import *
from tkinter import ttk
from config import *
import patterns

class ValheimServerMonitor:
    def __init__(self, root: Tk):
        self.root = root
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.title("Valheim Server Monitor")
        self.wrong_password_flag = False

        main_frame = ttk.Frame(self.root, padding=5)
        main_frame.grid(sticky=(N, W, E, S))

        server_frame = ttk.Labelframe(main_frame, text="Server Information", padding=5, borderwidth=1, relief="ridge")
        server_frame.grid(column=0, row=0, sticky=(N, W, E, S))

        log_frame = ttk.Frame(main_frame, padding=5)
        log_frame.grid(column=0, row=1, sticky=(N, W, E, S))

        # Server Information
        self.server_name = StringVar()
        ttk.Label(server_frame, text="Server Name:").grid(column=1, row=1, sticky=E)
        ttk.Label(server_frame, textvariable=self.server_name).grid(column=2, row=1, padx=5, sticky=W)

        self.server_join_code = StringVar()
        ttk.Label(server_frame, text="Join Code:").grid(column=3, row=1, sticky=E)
        ttk.Label(server_frame, textvariable=self.server_join_code).grid(column=4, row=1, padx=5, sticky=W)

        self.server_ip = StringVar()
        ttk.Label(server_frame, text="Server IP:").grid(column=5, row=1, sticky=E)
        ttk.Label(server_frame, textvariable=self.server_ip).grid(column=6, row=1, padx=5, sticky=W)

        self.server_status = StringVar()
        ttk.Label(server_frame, text="Server Status:").grid(column=1, row=2, sticky=E)
        ttk.Label(server_frame, textvariable=self.server_status).grid(column=2, row=2, padx=5, sticky=W)

        self.player_count = IntVar()
        ttk.Label(server_frame, text="Players Online:").grid(column=3, row=2, sticky=E)
        ttk.Label(server_frame, textvariable=self.player_count).grid(column=4, row=2, padx=5, sticky=W)

        # Log Data
        self.log_file_path = StringVar()
        self.log_file_path.set(load_config()["log_path"])
        ttk.Label(log_frame, text="Log File Location:").grid(column=1, row=1, sticky=E)
        ttk.Label(log_frame, textvariable=self.log_file_path).grid(column=2, row=1, padx=5, sticky=W)

        # Event log will take work. Probably try a tk.Text() widget with a scrollbar. For now, print event log to console.
        self.event_log = StringVar()
        #ttk.Label(log_frame, text="Event Log:").grid(column=1, row=2, sticky=(N, E))
        #ttk.Label(log_frame, textvariable=self.event_log, relief="sunken").grid(column=2, row=2, padx=5, pady=5, sticky=W)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        log_frame.columnconfigure(2, weight=1)

        try:
            self.log_file = open(self.log_file_path.get(), "r")
            print(self.log_file_path.get(), "opened")
        except OSError as e:
            print(e)
            self.log_file_path.set(f"{e.strerror}: Please set log file location in config.json")

        self.read_log()

    def read_log(self) -> None:
        while True:
            # Read next line until all lines are read. Once caught up, return to root.mainloop
            line = self.log_file.readline()
            if not line:
                break
            timestamp = " ".join(line.split()[0:2])
            # Pull server information from the log
            match = patterns.server_info_pattern.search(line)
            if match:
                self.server_name.set(match.group(1))
                self.server_join_code.set(match.group(2))
                self.server_ip.set(match.group(3))
                self.server_status.set("Online")

            # Check for wrong passwords, then check for connection events
            if "has wrong password" in line:
                self.wrong_password_flag = True
                self.event_log.set(self.event_log.get() + "Failed to join: wrong password\n")
            match = patterns.connection_pattern.search(line)
            if match:
                self.player_count.set(match.group(2))
                # In case of wrong password, manually reduce the player count. Valheim does not log this properly.
                if self.wrong_password_flag:
                    self.player_count.set(int(match.group(2))-1)
                    self.wrong_password_flag = False
                log_string = f"{timestamp} {match.group(1)}! Current player count: {match.group(2)}"
                print(log_string)
                self.event_log.set(self.event_log.get() + log_string + "\n")

            # Check for server heartbeat, and adjust active players if necessary
            match = patterns.connection_check_pattern.search(line)
            if match and int(match.group(1)) != self.player_count.get():
                self.player_count.set(int(match.group(1)))
                log_string = f"{timestamp} Server Heartbeat: Player count mismatch detected. Corrected player count to {match.group(1)}"
                print(log_string)
                self.event_log.set(self.event_log.get() + log_string + "\n")

            # Check for server shutdown
            match = patterns.shutdown_pattern.search(line)
            if match:
                print(timestamp, "Server Shutdown")
                self.server_status.set("Offline")

            # Check for server connections issues
            match = patterns.playfab_error_pattern.search(line)
            if match:
                log_string = f"{timestamp} PlayFab network {match.group(1)}: {match.group(2)}"
                # If error 4098 when player disconnects, server doesn't properly log the disconnect. Manually reduce player count.
                if int(match.group(2)) == 4098:
                    self.player_count.set(self.player_count.get() - 1)
                    log_string += f": Disconnect not properly logged. Player count corrected to {self.player_count.get()}"
                print(log_string)
            match = patterns.playfab_connection_pattern.search(line)
            if match:
                print(timestamp, "Joined PlayFab Party network")
                self.server_status.set("Online")

            # Check for information-only event logs
            for pattern, message in patterns.event_patterns:
                match = pattern.search(line)
                if match:
                    log_string = f"{timestamp} {message.format(*match.groups())}"
                    print(log_string)
                    self.event_log.set(self.event_log.get() + log_string + "\n")

        # Call read_log again after 1000ms to check for new lines
        self.root.after(1000, self.read_log)

    # Handles closing the log file when the GUI window is closed
    def on_close(self) -> None:
        if self.log_file and not self.log_file.closed:
            self.log_file.close()
            print("log file closed")

        self.root.destroy()

root = Tk()
app = ValheimServerMonitor(root)
root.mainloop()
