#!/bin/bash

RED="\033[0;31m"
GREEN="\033[0;32m"
RESET="\033[0m"  # Reset color to default

# Check if at least one argument is provided
if [ "$#" -eq 0 ]; then
    echo "SERVER SCRIPT: Missing at least one argument"
    exit 1
fi

echo "${GREEN}HOST SCRIPT${GREEN}"

model="$1"
echo "${GREEN}model $model${RESET}"

log_path="$2"
echo -e "${GREEN}Log files path: ${log_path} ${RESET}"

port=42837
echo -e "${GREEN}Port${RESET}"
echo $port

#Already added to path
#dorado_server_path=

dorado_basecall_server \
--config dna_r10.4.1_e8.2_400bps_hac.cfg \
--log_path $log_path \
--device cuda:0,1 \
--port $port \