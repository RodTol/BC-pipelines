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
echo "_____________________________________"
echo " "
echo "${GREEN} Title ${STD}"
echo " "
echo " ${RED} Message${STD}"
echo " "
echo "${GREEN} DATE:$DATE ${STD}"
echo "_____________________________________"
echo " "
######################## BOT INFO ############################
BOT_TOKEN="$BC_TOKEN_BOT"
CHAT_ID="-4074077922"
file_path="$1"
# Function to send a message to Telegram
send_message() {
 local message="$1"
 curl -s -X POST "https://api.telegram.org/bot$BOT_TOKEN/sendMessage" \
 -d "chat_id=$CHAT_ID" \
 -d "text=$message"
}
send_message "Hi I'm your bot to send files.. UPLOADING here…"
echo " "
echo "_____________________________________"
echo " "
echo " ${RED} Message Sent ${STD}"
echo "_____________________________________"
echo " "
echo " ${ON_BLUE} Uploading to Telegram${STD}"
echo " "
echo " "
 
# Function to send a file to Telegram
send_file() {
 local file_path="$1"
 local caption="$2"
 curl -s -X POST "https://api.telegram.org/bot$BOT_TOKEN/sendDocument" \
 -F "chat_id=$CHAT_ID" \
 -F "document=@$file_path" \
 -F "caption=$caption"
}
send_file "$1" "Your file is here." > /dev/null
echo " ${ON_BLUE} File Upload Complete ${STD}"
send_file "$1" "Your file2 is here." > /dev/null
echo " ${ON_BLUE} File2 Upload Complete ${STD}"