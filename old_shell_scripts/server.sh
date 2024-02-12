#!/bin/bash

log_path="/AB_20T_output/nanopore_output/server_logs/"
echo "Log files path"
echo $log_path
#read log_path

dorado_server_path=/u/dssc/tolloi/ont-dorado-server/bin/

$dorado_server_path/dorado_basecall_server \
--config dna_r10.4.1_e8.2_400bps_hac.cfg \
--log_path $log_path \
--device cuda:0,1,2,3,4,5,6,7 \
--port 42837 \