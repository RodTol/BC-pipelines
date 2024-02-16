#!/bin/bash
#Input parameters are the json and what node I am on the list 
json_file=$1
my_index=$2

#Read from config.json file
model=$(jq -r '.Basecalling.model' "$json_file")
logs_dir=$(jq -r '.Basecalling.logs_dir' "$json_file")
input_dir=$(jq -r '.Basecalling.input_dir' "$json_file")
output_dir=$(jq -r '.Basecalling.output_dir' "$json_file")


host_index=$(jq -r '.Resources.index_host' "$json_file")
node_name=$(jq -r --argjson my_index "$my_index" '.Resources.nodes_list[$my_index]' "$json_file")
gpus_settings=$(jq -r --argjson my_index "$my_index" '.Resources.gpus[$my_index]' "$json_file")

echo "Model: $model"gu
echo "Logs Directory: $logs_dir"
echo "Input Directory: $input_dir"
echo "Output Directory: $output_dir"

echo "I am this node_name: $node_name"
echo "GPUs selected: $gpus_settings"

#I need launch the server, BCM and BCP on the same dir in order to have
#the supervisor being able to find the connection file 
cd ~/BC-pipelines/BC_software

echo "Launching the server"
~/BC-pipelines/BC_scripts/server.sh $model $logs_dir $gpus_settings &
sleep 5

echo ""

#Load virtualenv for python
source /u/area/jenkins_onpexp/python_venvs/DGX_dorado_venv/bin/activate

#Start BCM and BCC on host node
if ((my_index == host_index)); then
  BC_manager_log_path=/u/area/jenkins_onpexp/scratch/jenkins_logs/tmp/BCManager_log.txt
  python3 BCManagement.py $json_file $my_index >> "$BC_manager_log_path" 2>&1 &

  sleep 5
fi

BC_controller_log_path=/u/area/jenkins_onpexp/scratch/jenkins_logs/tmp/BCController_log_$node_name.txt
python3 BCController.py $json_file $my_index >> "$BC_controller_log_path" 2>&1 &

sleep 5

#Start BCP
BC_processor_log_path="/u/area/jenkins_onpexp/scratch/jenkins_logs/tmp/BCProcessor_log_$node_name.txt"
python3 BCProcessors.py $json_file $my_index >> $BC_processor_log_path 2>&1 

wait