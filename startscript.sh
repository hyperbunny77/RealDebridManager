#!/bin/bash
export dbinfo=/config/main.db
export watchpath=/watch
exec python3 FileWatch.py &
exec gunicorn --bind 0.0.0.0:$rdmport mainwebui:app