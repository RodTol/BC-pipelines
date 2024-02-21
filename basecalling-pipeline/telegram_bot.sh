#!/bin/bash

# Set the filename for the environment variables
env_file=".env"

# Check if the environment file exists
if [ -e "$env_file" ]; then
    # Load environment variables from .env
    set -o allexport
    source "$env_file"
    set +o allexport

    # Check if TELEGRAM_BOT_TOKEN is defined
    if [ -n "$TELEGRAM_BOT_TOKEN" ]; then
        # Print a message indicating that the token is read from the environment file
        echo "Token read from $env_file"

        # Send a "Hello World" message to the Telegram bot
        echo "Sending a message to bot"
        curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" -d "chat_id=-4074077922" -d "text=Hello World"
        
        # Send a message containing the build number to the Telegram bot
        curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" -d "chat_id=-4074077922" -d text="from build #${BUILD_NUMBER}"
    else
        # Print an error message if TELEGRAM_BOT_TOKEN is not found
        echo "TELEGRAM_BOT_TOKEN not found in $env_file."
    fi
else
    # Print an error message if the environment file is not found
    echo "File $env_file not found."
fi
