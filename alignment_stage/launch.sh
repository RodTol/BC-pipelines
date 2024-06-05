#!/bin/bash
config_file_path=$1
cores=$(jq -r '.Alignment.Resources.Cores' "$config_file_path")
mem=$(jq -r '.Alignment.Resources.Mem' "$config_file_path")
time=$(jq -r '.Alignment.Resources.time' "$config_file_path")

srun -p EPYC -N 1 -c $cores --mem=$mem --time=$time python3 main.py $config_file_path



