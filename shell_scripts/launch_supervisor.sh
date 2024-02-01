#!/bin/bash

cd /u/dssc/tolloi/Cluster_Basecalling_Manager/BC_software/orfeo_executable/file_performance_test/executables/

timestamp=$(date +"%H:%M:%S")

counter=1

while true; do
    # Construct the output log file name with the counter
    output_log_path="/u/dssc/tolloi/Cluster_Basecalling_Manager/BC_software/orfeo_executable/file_performance_test/bc_logs"
    output_log_file="${output_log_path}/dgx002_${counter}_hac.txt"

    # Check if the file already exists, if not, break the loop
    if [ ! -e "$output_log_file" ]; then
        break
    fi

    # Increment the counter
    ((counter++))
done

./supervisor.sh $1 $2 > $output_log_file 2>&1 