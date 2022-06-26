#!/bin/bash
export dbinfo=/config/main.db # Change to where your DB should be stored
export watchpath=/watchpath # Change to your watch path where torrents are placed
exec python3 FileWatch.py & # Runs background watch service
exec gunicorn --bind 0.0.0.0:8003 mainwebui:app #Runs Web UI, Change Port as needed

