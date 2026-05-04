#!/bin/bash
python run.py &
SERVER_PID=$!
sleep 2
python -m pytest
kill $SERVER_PID
