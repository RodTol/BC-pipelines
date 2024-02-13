#!/bin/bash
current_time=$(date +"%Y-%m-%d %H:%M:%S")
echo "Current time: $current_time"
echo "Hello from ${SLURM_JOB_NODELIST}"

#Input parameters are the json and what node I am on the list 
json_file=$1
my_index=$2

#Read from config.json file
model=$(jq -r '.Basecalling.model' "$json_file")
logs_dir=$(jq -r '.Basecalling.logs_dir' "$json_file")
input_dir=$(jq -r '.Basecalling.input_dir' "$json_file")
output_dir=$(jq -r '.Basecalling.output_dir' "$json_file")

node=$(jq -r --argjson my_index "$my_index" '.Resources.nodes_list[$my_index]' "$json_file")
gpus_settings=$(jq -r --argjson my_index "$my_index" '.Resources.gpus[$my_index]' "$json_file")


echo "Model: $model"
echo "Logs Directory: $logs_dir"
echo "Input Directory: $input_dir"
echo "Output Directory: $output_dir"

echo "I am this node: $node"
echo "GPUs selected: $gpus_settings"

echo "Launching the server"
~/BC-pipelines/basecalling-pipeline/BC_scripts/server.sh $model $logs_dir $gpus_settings &
sleep 10

echo ""

#Load virtualenv for python
source /u/area/jenkins_onpexp/python_venvs/DGX_dorado_venv/bin/activate

cd ~/BC-pipelines/BC_software

#Start BCM on host node
if [ "$my_index" -eq 0 ]; then
  BC_manager_log_path=/u/area/jenkins_onpexp/scratch/jenkins_logs/tmp/BCManager_log.txt
  python3 BCManagement.py $json_file $my_index >> "$BC_manager_log_path" 2>&1 &
fi

#Start BCP
BC_processor_log_path="/u/area/jenkins_onpexp/scratch/jenkins_logs/tmp/BCProcessor_log_$node.txt"
python3 BCProcessors.py $json_file $my_index >> $BC_processor_log_path 2>&1 

wait