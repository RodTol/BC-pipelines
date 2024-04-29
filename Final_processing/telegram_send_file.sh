#!/bin/bash
# SOURCE: https://medium.com/@IamCOD3X/how-to-make-a-bashscript-to-send-file-over-telegram-c827011c880e

# Get date and time
DATE=$(date +"%m-%d-%y")
######################### Colours ############################
ON_BLUE=$(echo -e "\033[44m")
RED=$(echo -e "\033[1;31m")
BLUE=$(echo -e "\033[1;34m")
GREEN=$(echo -e "\033[1;32m")
STD=$(echo -e "\033[0m") # Clear colour
##############################################################

######################## BOT INFO ############################
BOT_TOKEN="$BC_TOKEN_BOT"
CHAT_ID="-4074077922"

echo "_____________________________________"
echo " "
echo " ${RED} Message Sent ${STD}"
echo "_____________________________________"
 
# Function to send a file to Telegram
send_file() {
 local file_path="$1"
 local caption="$2"
 curl -s -X POST "https://api.telegram.org/bot$BOT_TOKEN/sendDocument" \
 -F "chat_id=$CHAT_ID" \
 -F "document=@$file_path" \
 -F "caption=$caption"
}

send_file "$1" "Speed plot ." > /dev/null
echo " ${ON_BLUE} File Upload Complete ${STD}"

send_file "$2" "File distribution plot." > /dev/null
echo " ${ON_BLUE} File2 Upload Complete ${STD}"