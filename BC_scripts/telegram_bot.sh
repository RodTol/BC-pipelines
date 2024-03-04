#!/bin/bash
export TEMP_RUN_NAME=$(jq -r '.General.run_name' < $1)

# Check if BC_TOKEN_BOT is defined
if [ -n "$BC_TOKEN_BOT" ]; then
    # Send a "Hello World" message to the Telegram bot
    echo "Sending a message to bot"
    curl -s -X POST "https://api.telegram.org/bot$BC_TOKEN_BOT/sendMessage" -d "chat_id=-4074077922" -d "text=Hello World"
    
    # Send a message containing the build number to the Telegram bot
    curl -s -X POST "https://api.telegram.org/bot$BC_TOKEN_BOT/sendMessage" -d "chat_id=-4074077922" -d text="from build #${BUILD_NUMBER}"
else
    # Print an error message if BC_TOKEN_BOT is not found
    echo "BC_TOKEN_BOT not found "
fi


