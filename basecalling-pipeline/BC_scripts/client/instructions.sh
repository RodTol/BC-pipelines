#!/bin/bash
current_time=$(date +"%Y-%m-%d %H:%M:%S")
echo "Current time: $current_time"
echo "hello from ${SLURM_JOB_NODELIST}"

model=$1
logs_dir=$2

echo "Launching the server"
~/BC-pipelines/basecalling-pipeline/BC_scripts/client/server.sh $model $logs_dir


