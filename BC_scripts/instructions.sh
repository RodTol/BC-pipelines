#!/bin/bash

# Color for bash echo
RED="\033[0;31m"
GREEN="\033[0;32m"
CYAN="\033[0;36m"
RESET="\033[0m"

# Input parameters are the json and what node I am on the list 
json_file=$1
my_index=$2

# Read from config.json file (necessary)
host_index=$(jq -r '.Resources.index_host' "$json_file")
node_name=$(jq -r --argjson my_index "$my_index" '.Resources.nodes_list[$my_index]' "$json_file")
model=$(jq -r '.Basecalling.model' "$json_file")
logs_dir=$(jq -r '.Basecalling.logs_dir' "$json_file")
node_queue=$(jq -r --argjson my_index "$my_index" '.Resources.nodes_queue[$my_index]' "$json_file")

input_dir=$(jq -r '.Basecalling.input_dir' "$json_file") #debug
output_dir=$(jq -r '.Basecalling.output_dir' "$json_file") #debug
gpus_settings=$(jq -r --argjson my_index "$my_index" '.Resources.gpus[$my_index]' "$json_file") #debug

echo -e "${RED}I am this node_name: $node_name${RESET}, and for Slurm: $SLURM_NODELIST"

# Update config.json file
if  [ "$node_name" == "" ]; then
  echo -e "${RED}|||Update node_name from $node_name to $SLURM_NODELIST|||${RESET}"
  node_name=$SLURM_NODELIST
fi
# Brief output for checking everything it's correct
echo $CUDA_VISIBLE_DEVICES
echo -e "${RED}GPUs selected: $gpus_settings${RESET}"
echo -e "${RED}-----------------------${RESET}"
echo "Model: $model"
echo "Node queue: $node_queue"
echo "Logs Directory: $logs_dir"
echo "Input Directory: $input_dir"
echo "Output Directory: $output_dir"
echo -e "${RED}-----------------------${RESET}"

# Each node has its own dir with the port file for the connection
mkdir ~/BC-pipelines/BC_software/server_node_$node_name
cd ~/BC-pipelines/BC_software/server_node_$node_name

sleep 5 # Maybe I need this pause to be able to create the TCP file correctly

# Starting the dorado_basecall_server, using the script
echo "Launching the server"
~/BC-pipelines/BC_scripts/server.sh $model $logs_dir $gpus_settings &
sleep 20 # Maybe I need this pause to be able to create the TCP file correctly

# Load virtualenv for Python, necessary for BC Software
# Note that each node needs its own virtualenv since they 
# do not share python
if [ "$node_queue" == "DGX" ]; then
  source /u/area/jenkins_onpexp/python_venvs/DGX_dorado_venv/bin/activate
  echo -e "${CYAN}$node_name is loading DGX venv, given ${node_queue}${RESET}"
elif [ "$node_queue" == "GPU" ]; then
  source /u/area/jenkins_onpexp/python_venvs/GPU_dorado_venv/bin/activate
  echo -e "${CYAN}$node_name is loading GPU venv, given ${node_queue}${RESET}"
else
  echo -e "${RED}SOMETHING WRONG IN THE VIRTUALENV FOR BC SOFTWARE${RESET}"
fi

# Start BCManager and BCController on host node
if ((my_index == host_index)); then
  BC_manager_log_path=${logs_dir}/BCManager_log.txt
  python3 ~/BC-pipelines/BC_software/BCManagement.py $json_file $my_index >> "$BC_manager_log_path" 2>&1 &

  sleep 5
  
  BC_controller_log_path=${logs_dir}/BCController_log_$node_name.txt
  python3 ~/BC-pipelines/BC_software/BCController.py $json_file $my_index >> "$BC_controller_log_path" 2>&1 &
  
  sleep 5
fi

# Start BCProcessor
BC_processor_log_path="${logs_dir}/BCProcessor_log_$node_name.txt"
python3 ~/BC-pipelines/BC_software/BCProcessors.py $json_file $my_index >> $BC_processor_log_path 2>&1 

wait