#!/bin/bash
current_time=$(date +"%Y-%m-%d %H:%M:%S")
echo "Current time: $current_time"
echo "hello from ${SLURM_JOB_NODELIST}"

json_file=$1

#Read from config.json file
model=$(jq -r '.Basecalling.model' "$json_file")
logs_dir=$(jq -r '.Basecalling.logs_dir' "$json_file")
input_dir=$(jq -r '.Basecalling.input_dir' "$json_file")
output_dir=$(jq -r '.Basecalling.output_dir' "$json_file")

index_host=$(jq -r '.Resources.index_host' "$json_file")

echo "Model: $model"
echo "Logs Directory: $logs_dir"
echo "Input Directory: $input_dir"
echo "Output Directory: $output_dir"

echo "Launching the server"
~/BC-pipelines/basecalling-pipeline/BC_scripts/host/server.sh $model $logs_dir &
sleep 10

echo ""

#echo "Launching the supervisor"
#~/BC-pipelines/basecalling-pipeline/BC_scripts/host/supervisor.sh $input_dir $output_dir $model

#Start BCM on host node
BC_manager_log_path=/u/area/jenkins_onpexp/scratch/jenkins_logs/tmp/BCManager_log.txt
python3 ~/BC-pipelines/BC_software/BCManagement.py $json_file 0 > $BC_manager_log_path 2>&1

#Start BCP
