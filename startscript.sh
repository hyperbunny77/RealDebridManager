#!/bin/bash
exec python3 FileWatch.py &
exec gunicorn --bind 0.0.0.0:$rdmport mainwebui:app