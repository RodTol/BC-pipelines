#!/bin/bash

# Function to send a message to Telegram
send_message() {
 local message="$1"
  
 curl -s -X POST "https://api.telegram.org/bot$BOT_TOKEN/sendMessage" \
 -d "chat_id=$CHAT_ID" \
 -d "parse_mode=HTML" \
 -d "text=$message"
}

BOT_TOKEN="$BC_TOKEN_BOT"
CHAT_ID="-4074077922"

json_file=$1
run_name=$(jq -r '.General.run_name' "$json_file")
model=$(jq -r '.Basecalling.model' "$json_file")
nodes_list=$(jq -r '.Resources.nodes_list' "$json_file")

message="<b> Jenkins is building for $run_name is at $(date +"%H:%M:%S")."

send_message $message > /dev/null