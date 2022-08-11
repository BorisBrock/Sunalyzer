#!/bin/bash

exec python grabber/grabber.py &
exec python webserver/server.py