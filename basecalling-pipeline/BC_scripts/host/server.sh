#!/bin/bash

# Check if at least one argument is provided
if [ "$#" -eq 0 ]; then
    echo "SERVER SCRIPT: Missing at least one argument"
    exit 1
fi

echo "HOST SCRIPT"

model="$1"
echo "model"
echo $model

log_path="$2"
echo "Log files path"
echo $log_path

#Already added to path
#dorado_server_path=

dorado_basecall_server \
--config dna_r10.4.1_e8.2_400bps_sup.cfg \
--log_path $log_path \
--device cuda:0,1 \
--port 41757 \