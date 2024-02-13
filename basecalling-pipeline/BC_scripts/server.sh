#!/bin/bash

RED="\033[0;31m"
GREEN="\033[0;32m"
RESET="\033[0m"  # Reset color to default

echo -e "${GREEN}HOST SERVER SCRIPT${RESET}"

model="$1"
echo -e "${GREEN}model $model${RESET}"

log_path="$2"
echo -e "${GREEN}Log files path: ${log_path} ${RESET}"

gpus_settings="$3"
echo -e "${GREEN}GPUs selected: ${gpus_settings} ${RESET}"

port=42837
echo -e "${GREEN}Port${RESET} $port "

#Already added to path
#dorado_server_path=

dorado_basecall_server \
--config $model \
--log_path $log_path \
--device $gpus_settings \
--port $port \