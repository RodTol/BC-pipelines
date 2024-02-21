#!/bin/bash

#Color for bash echo
RED="\033[0;31m"
GREEN="\033[0;32m"
RESET="\033[0m"  

input_dir=$1
echo -e "${RED}Input directory${RESET}"
echo $input_dir

output_dir=$2
echo -e "${RED}Output path${RESET}"
echo $output_dir

model=$3
echo -e "${RED}Model${RESET}"
echo $model

port=42837
echo -e "${RED}Port${RESET}"
echo $port

#Added to PATH
#dorado_server_path=/u/dssc/tolloi/ont-dorado-server/bin/

num_clients=5

ont_basecaller_supervisor --num_clients $num_clients \
--input_path $input_dir \
--save_path $output_dir \
--config $model \
--port $port 