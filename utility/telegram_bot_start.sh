#!/bin/bash

######################## BOT INFO ############################
BOT_TOKEN="$BC_TOKEN_BOT"
CHAT_ID="-4074077922"

# Function to send a message to Telegram
send_message() {
 local message="$1"
 curl -s -X POST "https://api.telegram.org/bot$BOT_TOKEN/sendMessage" \
 -d "chat_id=$CHAT_ID" \
 -d "text=$message"
}

# Function to send a file to Telegram
send_file() {
 local file_path="$1"
 local caption="$2"
 curl -s -X POST "https://api.telegram.org/bot$BOT_TOKEN/sendDocument" \
 -F "chat_id=$CHAT_ID" \
 -F "document=@$file_path" \
 -F "caption=$caption"
}

BC_MODEL=$(jq -r '.Basecalling.model' < $1)
INPUT_DIR="/u/area/jenkins_onpexp/scratch/test_10G_dataset_POD5"
message="**I am watching directory $INPUT_DIR **\nWith Basecalling model $BC_MODEL\nand the following computing resources:"

python3 /u/area/jenkins_onpexp/BC-pipelines/utility/resources_recap.py $1

# Check if BC_TOKEN_BOT is defined
if [ -n "$BC_TOKEN_BOT" ]; then
    # Send a "Hello World" message to the Telegram bot
    echo "Sending message to bot"
    send_message "$message" > /dev/null
    send_file "/u/area/jenkins_onpexp/BC-pipelines/utility/resource_table.png" "First plot." > /dev/null
else
    # Print an error message if BC_TOKEN_BOT is not found
    echo "BC_TOKEN_BOT not found "
fi


