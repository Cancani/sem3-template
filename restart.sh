#!/bin/bash
cd /home/ubuntu/sem3-template || exit
docker compose down
docker compose up --build -d