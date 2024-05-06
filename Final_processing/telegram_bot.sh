#!/bin/bash

######################## BOT INFO ############################
BOT_TOKEN="$BC_TOKEN_BOT"
CHAT_ID="-4270864261"

# Function to send a message to Telegram
send_message() {
 local message="$1"
 curl -s -X POST "https://api.telegram.org/bot$BOT_TOKEN/sendMessage" \
 -d "chat_id=$CHAT_ID" \
 -d "text=$message"
}

export TEMP_RUN_NAME=$(jq -r '.General.run_name' < $1)

# Check if BC_TOKEN_BOT is defined
if [ -n "$BC_TOKEN_BOT" ]; then
    # Send a "Hello World" message to the Telegram bot
    send_message "Jenkins performed build $TEMP_RUN_NAME succesfully. These are the results of this batch:" > /dev/null
else
    # Print an error message if BC_TOKEN_BOT is not found
    echo "BC_TOKEN_BOT not found "
fi


