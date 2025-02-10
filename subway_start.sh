#!/bin/bash

# Maximum log file size in bytes
MAX_LOG_SIZE=1000000  # 1MB

cd ~/Pi_Subway_Ticker/

board_command () {
    echo "Starting LED Board"
    screen -dmS board python3 backend/pi_subway_ticker.py
}

api_command () {
    echo "Starting API"
    cd backend
    screen -dmS api python3 app.py
}

website_command () {
    echo "Starting Local Server"
    cd frontend
    screen -dmS website npm run dev
}

log_size_check () {
    while true; do
        sleep 3600  # Sleep for 1 hour (3600 seconds)
        check_log_size "logs/board_logs.log"
        check_log_size "logs/api_logs.log"
        check_log_size "logs/website_logs.log"
        echo "Log sizes checked."
    done
}

check_log_size() {
    log_file=$1
    if [ -f "$log_file" ]; then
        log_size=$(stat -c %s "$log_file")
        if [ $log_size -gt $MAX_LOG_SIZE ]; then
            echo "Log file $log_file exceeds maximum size, clearing..."
            echo "" > "$log_file"
        fi
    fi
}

cleanup() {
    echo "Cleaning up..."
    pkill screen
    exit 0
}

# Trap Ctrl+C to perform cleanup
trap cleanup SIGINT

# Create logs directory if it doesn't exist
mkdir -p logs

# Run log size check concurrently
log_size_check &

# Run other commands concurrently
board_command &
api_command &
website_command &

echo "All commands started."

# Wait for all background processes to finish
wait
