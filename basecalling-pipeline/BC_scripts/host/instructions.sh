#!/bin/bash
current_time=$(date +"%Y-%m-%d %H:%M:%S")
echo "Current time: $current_time"
echo "hello from ${SLURM_JOB_NODELIST}"

#Input parameters are the json and what node I am on the list 
json_file=$1
my_index=$2

#Read from config.json file
model=$(jq -r '.Basecalling.model' "$json_file")
logs_dir=$(jq -r '.Basecalling.logs_dir' "$json_file")
input_dir=$(jq -r '.Basecalling.input_dir' "$json_file")
output_dir=$(jq -r '.Basecalling.output_dir' "$json_file")
gpus_settings=$(jq -r '.Resources.gpus[0]' "$json_file")


echo "Model: $model"
echo "Logs Directory: $logs_dir"
echo "Input Directory: $input_dir"
echo "Output Directory: $output_dir"

echo "Launching the server"
~/BC-pipelines/basecalling-pipeline/BC_scripts/host/server.sh $model $logs_dir $gpus_settings &
sleep 10

echo ""

#echo "Launching the supervisor"
#~/BC-pipelines/basecalling-pipeline/BC_scripts/host/supervisor.sh $input_dir $output_dir $model

#Load virtualenv for python
source /u/area/jenkins_onpexp/python_venvs/DGX_dorado_venv/bin/activate

#Start BCM on host node
BC_manager_log_path=/u/area/jenkins_onpexp/scratch/jenkins_logs/tmp/BCManager_log.txt
python3 ~/BC-pipelines/BC_software/BCManagement.py $json_file 0 >> $BC_manager_log_path 2>&1 &

#Start BCP
BC_processor_log_path=/u/area/jenkins_onpexp/scratch/jenkins_logs/tmp/BCProcessor_log.txt
python3 ~/BC-pipelines/BC_software/BCProcessors.py $json_file 0 >> $BC_processor_log_path 2>&1 

wait