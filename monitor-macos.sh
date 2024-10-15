#!/bin/bash

FOLDER_TO_RUN="./site"
FOLDER_TO_MONITOR="./template"
PORT=8001 

# Function to start the live HTTP server
start_server() {
    echo "Starting HTTP server on port $PORT in $FOLDER_TO_RUN..."
    (cd "$FOLDER_TO_RUN" && python3 -m http.server $PORT) &
    SERVER_PID=$!  # Capture the server process ID
}

# Function to stop the HTTP server
stop_server() {
    if [[ ! -z "$SERVER_PID" ]]; then
        echo "Stopping HTTP server (PID: $SERVER_PID)..."
        kill $SERVER_PID
        wait $SERVER_PID 2>/dev/null
    fi
}

run_command() {
	python3 ssg/generate.py
}

start_server

fswatch -o "$FOLDER_TO_MONITOR" | while read; do
    run_command
done

trap stop_server EXIT

