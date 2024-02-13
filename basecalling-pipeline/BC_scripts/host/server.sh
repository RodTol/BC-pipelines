#!/bin/bash

RED="\033[0;31m"
GREEN="\033[0;32m"
RESET="\033[0m"  # Reset color to default

# Check if at least one argument is provided
if [ "$#" -eq 0 ]; then
    echo "SERVER SCRIPT: Missing at least one argument"
    exit 1
fi

echo -e "${GREEN}HOST SERVER SCRIPT${RESET}"

model="$1"
echo -e "${GREEN}model $model${RESET}"

log_path="$2"
echo -ez "${GREEN}Log files path: ${log_path} ${RESET}"

port=42837
echo -e "${GREEN}Port${RESET} $port "

#Already added to path
#dorado_server_path=

dorado_basecall_server \
--config $model \
--log_path $log_path \
--device cuda:0,1 \
--port $port \