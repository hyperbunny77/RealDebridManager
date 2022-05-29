#!/bin/bash
exec python3 FileWatch.py &
exec gunicorn --bind 0.0.0.0:5000 mainwebui:app