#!/bin/bash
exec python backend/grabber.py &
exec python backend/server.py