#!/bin/bash

RED="\033[0;31m"
GREEN="\033[0;32m"
RESET="\033[0m"  # Reset color to default

echo -e "${RED}Input directory${RESET}"
echo $1

save_path=$2
echo -e "${RED}Save path${RESET}"
echo $save_path

dorado_server_path=/u/dssc/tolloi/ont-dorado-server/bin/

$dorado_server_path/ont_basecaller_supervisor --num_clients $num_clients \
--input_path $1 \
--save_path $save_path \
--config dna_r10.4.1_e8.2_400bps_hac.cfg \
--port 40765 