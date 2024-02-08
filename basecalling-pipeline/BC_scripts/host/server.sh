#!/bin/bash

# Check if at least one argument is provided
if [ "$#" -eq 0 ]; then
    echo "Missing at least one argument"
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
--config $model \
--log_path $log_path \
--device cuda:0,1,2,3,4,5,6,7 \
--port 42837 \