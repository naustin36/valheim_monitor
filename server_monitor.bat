@echo off

rem echo "Starting Valheim Crossplay Server Monitor"
rem echo "This console provides a log of important and useful events"
rem echo "To quit, close the monitor GUI window. This ensures proper closing of log file handle"


start "" pythonw "%~dp0monitor_gui.py"
