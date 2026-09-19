### VALHEIM CROSSPLAY SERVER MONITOR
Because there isn't a good way to communicate directly with PlayFab's servers, this server monitor simply parses the valheim server log.

To start the server monitor, run server_monitor.bat.

To create the server log file, edit the start_headless_server.bat in the server directory to include -logfile "[desired location]" in the launch options.
e.g. "valheim_server -nographics -batchmode -name "[server name] -port 2456 -world "[your world file name]" -password "[password]" -logfile "[C:/some_folder/log.txt]" -crossplay [etc, etc]

This results in the server console no longer showing the log output, as it is instead written directly to the log file in the location you specified. You must still use CTRL+C in the server's console to close the server. The log file is created when the server runs for the first time, and is overwritten if the server is restarted.

In the server monitor GUI, you can type the absolute path to the log file (e.g. C:/some_folder/log.txt) and click the "Read Log" button to begin monitoring. If the server is shut down and restarted while the monitor is still running, you must click "Read Log" again to begin monitoring the new log.

Once a log file has been successfully loaded, it is saved to config.json and will be loaded by default whenever the server monitor is run. To change it, just enter a new file path in the monitor window and click "Load Log". Alternatively, you can edit config.json and replace the previously saved path.
