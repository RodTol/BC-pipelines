#!/bin/bash

# Function to send a message to Telegram
send_message() {
 local message="$1"
 local background_color="$2"
 local formatted_message="<b>${message}</b>"
 
 curl -s -X POST "https://api.telegram.org/bot$BOT_TOKEN/sendMessage" \
 -d "chat_id=$CHAT_ID" \
 -d "text=$formatted_message" \
 -d "parse_mode=HTML" \
 -d "disable_web_page_preview=true" \
 -d "caption=$formatted_message" \
 -d "reply_markup={\"inline_keyboard\":[[{\"text\":\"Click me\",\"url\":\"https://example.com\"}]]}"
}

BOT_TOKEN="$BC_TOKEN_BOT"
CHAT_ID="-4074077922"

json_file=$1
run_name=$(jq -r '.General.run_name' "$json_file")
model=$(jq -r '.Basecalling.model' "$json_file")
nodes_list=$(jq -r '.Resources.nodes_list' "$json_file")

send_message "The $run_name is started at $(date +"%H:%M:%S")." "#BB8FCE"
send_message "The basecalling will be executed on $nodes_list with model $model" "#BB8FCE" > /dev/null