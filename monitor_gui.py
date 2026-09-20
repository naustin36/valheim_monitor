from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from config import *
import patterns

ERROR_CODES = {
    "4098":"Player socket timeout"
}
class ValheimServerMonitor:
    def __init__(self, root: Tk):
        self.root = root
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.title_name = "Valheim Crossplay Server Monitor"
        self.log_file = None
        self.config = load_config()

        main_frame = ttk.Frame(self.root, padding=5)
        main_frame.grid(sticky=(N, W, E, S))

        server_frame = ttk.Labelframe(main_frame, text="Server Information", padding=5, borderwidth=1, relief="ridge")
        server_frame.grid(column=0, row=0, sticky=(N, W, E, S), columnspan=2)

        log_frame = ttk.Frame(main_frame, padding=5)
        log_frame.grid(column=0, row=1, sticky=(N, W, E, S), columnspan=2)

        player_frame = ttk.Labelframe(main_frame, text="Player Info", padding=5, borderwidth=1, relief="ridge")
        player_frame.grid(column=0, row=2, sticky=(N, W, E, S))

        event_frame  = ttk.Labelframe(main_frame, text="Event Log", padding=5, borderwidth=1, relief="ridge")
        event_frame.grid(column=1, row=2, sticky=(N, W, E, S))

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
        ttk.Label(player_frame, text="Players Online:").grid(column=1, row=1, sticky=(N, E))
        ttk.Label(player_frame, textvariable=self.player_count).grid(column=2, row=1, sticky=(N, W))

        self.player_dict: dict[str, str] = {}
        self.player_list: list[str] = []
        self.player_list_Var = StringVar()
        self.player_listbox = Listbox(player_frame, listvariable=self.player_list_Var).grid(column=1, row=2, columnspan=2, sticky=(N, W, E, S))

        # Log and Player Data
        self.log_file_path = StringVar()
        self.log_file_path.set(self.config["log_path"])
        ttk.Label(log_frame, text="Log File Location:").grid(column=1, row=1, sticky=E)
        log_file_entry = ttk.Entry(log_frame, textvariable=self.log_file_path, width=50)
        log_file_entry.grid(column=2, row=1, padx=5, sticky=(W,E))
        log_file_entry.focus()
        self.root.bind("<Return>", self.open_log)

        ttk.Button(log_frame, text="Read Log", command=self.open_log).grid(column=3, row=1, sticky=W)

        self.log_file_status = StringVar()
        ttk.Label(log_frame, textvariable=self.log_file_status).grid(column=1, row=2, sticky=(N, W), columnspan=2, pady=5)

        self.event_log_display = ScrolledText(event_frame, width=105, height=10, state="disabled", wrap="word")
        self.event_log_display.grid(column=3, row=2, sticky=(N, E, W, S))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        log_frame.columnconfigure(2, weight=1)
        event_frame.columnconfigure(3, weight=1)
        event_frame.rowconfigure(2, weight=1)

        self.open_log()

    def open_log(self, *args):
        try:
            # Clear any existing server information; it will be repopulated by the log
            self.server_name.set("")
            self.root.title(self.title_name)
            self.server_ip.set("")
            self.server_join_code.set("")
            self.event_log_display.config(state="normal")
            self.event_log_display.delete("1.0", END)
            self.event_log_display.config(state="disabled")
            # If a log file is already open, close it
            if self.log_file:
                self.log_file.close()
                print("Log file handle closed")
            # Open the new log file specified in the entry field
            self.log_file = open(self.log_file_path.get(), "r")
            print(self.log_file_path.get(), "handle opened")

            # Clear any log status errors
            self.log_file_status.set("Log loaded successfully, monitoring:")

            # Update config.json with new log file path
            if self.log_file_path.get() != self.config["log_path"]:
                self.config["log_path"] = self.log_file_path.get()
                save_config(self.config)
                print("config.json updated with new log file")

            # Read the new log
            self.read_log()
        except OSError as e:
            print(e)
            self.log_file_status.set(f"{e.strerror}: Please verify log path is correct and log exists")

    def read_log(self) -> None:
        if not self.log_file or self.log_file.closed:
            return
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
                self.root.title(f"{self.title_name} - {self.server_name.get()}")
                self.server_join_code.set(match.group(2))
                self.server_ip.set(match.group(3))
                self.server_status.set("Online")

            # Check for player logon
            match = patterns.player_zdoID_created_pattern.search(line)
            if match:
                print(f"{timestamp} Player zdoID created/updated: Name: {match.group(1)} zdoID: {match.group(2)}")

                if match.group(1) not in self.player_dict:
                    self.player_logon(match.group(1))
                    self.log_event(f"{timestamp} Player Joined: {match.group(1)}")
                self.player_dict[match.group(1)] = match.group(2)
                self.player_count.set(len(self.player_dict))
            # Check for player logoff
            match = patterns.player_zdoID_destroyed_pattern.search(line)
            if match:
                for player_name in self.player_dict.copy():
                    if match.group(1) == self.player_dict[player_name]:
                        print(f"{timestamp} Player logged off. Name: {player_name} zdoID: {self.player_dict.copy()[player_name]}")
                        self.player_logoff(player_name)
                        self.log_event(f"{timestamp} Player Left: {player_name}")
                        self.player_count.set(len(self.player_dict))

            # Check for server shutdown
            match = patterns.shutdown_pattern.search(line)
            if match:
                print(timestamp, "Server Shutdown")
                log_string = f"{timestamp} Server Shutdown. Log file closed."
                self.server_status.set("Offline")
                self.log_file.close()
                self.log_file_status.set("Server shutdown. Log file closed")
                print(f"log file closed: {self.log_file.closed}")
                self.log_event(log_string)
                break

            # Check for server errors
            match = patterns.playfab_error_pattern.search(line)
            if match:
                log_string = f"{timestamp} PlayFab network {match.group(1)} {match.group(2)}"
                if match.group(2) in ERROR_CODES:
                    log_string += f": {ERROR_CODES[match.group(2)]}"
                print(log_string)
                self.log_event(log_string)

            # Check for information-only event logs
            for pattern, message in patterns.event_patterns:
                match = pattern.search(line)
                if match:
                    log_string = f"{timestamp} {message.format(*match.groups())}"
                    print(log_string)
                    self.log_event(log_string)

        # Call read_log again after 1000ms to check for new lines
        self.root.after(1000, self.read_log)

    def log_event(self, event_message):
        self.event_log_display.config(state="normal")
        self.event_log_display.insert(END, event_message + "\n")
        self.event_log_display.see(END)
        self.event_log_display.config(state="disabled")

    def player_logon(self, player_name: str):
        self.player_list.append(player_name)
        self.player_list_Var.set(self.player_list)

    def player_logoff(self, player_name: str):
        self.player_list.remove(player_name)
        self.player_list_Var.set(self.player_list)
        del self.player_dict[player_name]

    # Handles closing the log file when the GUI window is closed
    def on_close(self) -> None:
        if self.log_file and not self.log_file.closed:
            self.log_file.close()
            print("log file closed")

        self.root.destroy()

root = Tk()
app = ValheimServerMonitor(root)
root.mainloop()
