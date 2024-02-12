#!/bin/bash
RED="\033[0;31m"
GREEN="\033[0;32m"
RESET="\033[0m"  # Reset color to default

current_time=$(date "+%Y-%m-%d %H:%M:%S")
message="$SLURM_JOB_NODELIST"
# Echo the time and message
echo -e "${RED}[$current_time] $message${RESET}"

# venv activation
cd /u/dssc/tolloi/Cluster_Basecalling_Manager/BC_software/orfeo_executable/
source BC_venv/bin/activate

cd /u/dssc/tolloi/Cluster_Basecalling_Manager/BC_software/orfeo_executable/file_performance_test/executables

./server.sh &
server_pid=$!

number_of_splits=$1
total_file=584
batch_size=$((total_file / number_of_splits))

echo "------------------------------------"
echo "Number of Splits: $number_of_splits"
echo "Total Files: $total_file"
echo "Batch Size: $batch_size"
echo "------------------------------------"

python_file="/u/dssc/tolloi/Cluster_Basecalling_Manager/BC_software/orfeo_executable/file_performance_test/executables/BCConfiguration.py"
run_name="run_${number_of_splits}_splits"

output_dir="/AB_20T_output/nanopore_output/run_files_test/outputs/${run_name}"
bc_logs_path=/u/dssc/tolloi/Cluster_Basecalling_Manager/BC_software/orfeo_executable/file_performance_test/bc_logs/$run_name

# Use sed to replace the value of engine_optimal_request_size with the new value
if [$number_of_splits == 1]; then
    #Should already be 584
    echo "Batch size modified. New value: $batch_size"
else
    previous_value=$((total_file / (number_of_splits-1)))
    sed -i "s/engine_optimal_request_size = $previous_value/engine_optimal_request_size = $batch_size/" "$python_file"
    echo "Batch size modified. New value: $batch_size"
fi

sed -i "s|mngt_outputdir = '/AB_20T_output/nanopore_output/run_files_test/outputs/run_name'|mngt_outputdir = '$output_dir'|" "$python_file"
sed -i "s|engine_outputdir = '/AB_20T_output/nanopore_output/run_files_test/outputs/run_name'|engine_outputdir = '$output_dir'|" "$python_file"

python3 BCManagement.py > $bc_logs_path/BC_manager_log.txt 2>&1  &
current_time=$(date "+%Y-%m-%d %H:%M:%S")
message="BC_manager is running"
echo -e "${RED}[$current_time] $message${RESET}"


sleep 10
python3 BCProcessors.py

current_time=$(date "+%Y-%m-%d %H:%M:%S")
message="Processors has finished on dgx002"
# Echo the time and message
echo -e "${GREEN}[$current_time] $message${RESET}"

