#!/bin/bash

# Copy config if it doesn't exist already
cp -n config.yml data/config.yml

exec python backend/grabber.py &
exec python backend/server.py