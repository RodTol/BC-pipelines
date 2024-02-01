#!/bin/bash

env_file=".env"

if [ -e "$env_file" ]; then
    # Load environment variables from .env
    set -o allexport
    source "$env_file"
    set +o allexport

    if [ -n "$TELEGRAM_BOT_TOKEN" ]; then
        echo "Token read from $env_file"

        echo "Sending a message to bot"
        curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" -d "chat_id=-4074077922" -d "text=Hello World"
    	curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" -d "chat_id=-4074077922" -d text="from build #${BUILD_NUMBER}"
    else
        echo "TELEGRAM_BOT_TOKEN not found in $env_file."
    fi
else
    echo "File $env_file not found."
fi

