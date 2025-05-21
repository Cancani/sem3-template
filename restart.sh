#!/bin/bash
cd ~/sem3-template || exit
source venv/bin/activate || python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
pkill gunicorn || true
gunicorn -w 4 -b 0.0.0.0:8000 run:app &
