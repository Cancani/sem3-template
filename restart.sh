#!/bin/bash
cd /home/ubuntu/ma-room-template
source venv/bin/activate
pkill gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 run:app
