from tkinter import *
from tkinter import ttk

class ValheimServerMonitor:
    def __init__(self, root: Tk):
        root.title("Valheim Server Monitor")

        server_frame = ttk.Frame(root, padding=10)
        server_frame.grid(column=0, row=0, sticky=(N, W, E, S))

        log_frame = ttk.Frame(root, padding=10)
        log_frame.grid(column=0, row=1, sticky=(N, W, E, S))

        # Server Information
        self.server_name = StringVar()
        ttk.Label(server_frame, text="Server Name:").grid(column=1, row=1, sticky=E)
        ttk.Label(server_frame, textvariable=self.server_name).grid(column=2, row=1, sticky=W)

        self.server_join_code = StringVar()
        ttk.Label(server_frame, text="Join Code:").grid(column=3, row=1, sticky=E)
        ttk.Label(server_frame, textvariable=self.server_join_code).grid(column=4, row=1, sticky=W)

        self.server_status = StringVar()
        ttk.Label(server_frame, text="Server Status:").grid(column=1, row=2, sticky=E)
        ttk.Label(server_frame, textvariable=self.server_status).grid(column=2, row=2, sticky=W)

        self.player_count = StringVar()
        ttk.Label(server_frame, text="Players Online:").grid(column=3, row=2, sticky=E)
        ttk.Label(server_frame, textvariable=self.player_count).grid(column=4, row=2, sticky=W)

        # Log Data
        self.log_file_path = StringVar()
        ttk.Label(log_frame, text="Log File Location:").grid(column=1, row=1, sticky=E)
        ttk.Label(log_frame, textvariable=self.log_file_path).grid(column=2, row=1, sticky=W)

        self.event_log = StringVar()
        ttk.Label(log_frame, text="Event Log:").grid(column=1, row=2, sticky=E)
        ttk.Label(log_frame, textvariable=self.event_log).grid(column=2, row=2, sticky=W)

root = Tk()
ValheimServerMonitor(root)
root.mainloop()
