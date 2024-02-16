#!/bin/bash
#SBATCH --job-name=jk-try
#SBATCH --time=00:20:00
#SBATCH --output=/u/area/jenkins_onpexp/scratch/jenkins_logs/tmp/%x-%j.out  
#SBATCH --error=/u/area/jenkins_onpexp/scratch/jenkins_logs/tmp/%x-%j.err   
#SBATCH -A lage -p DGX --nodes=1 --ntasks-per-node=1 --cpus-per-task=24 --gpus=2
#SBATCH hetjob
#SBATCH -A lage -p DGX --nodes=1 --ntasks-per-node=1 --cpus-per-task=24 --gpus=1

json_file=$1
index_host=$(jq -r '.Resources.index_host' "$json_file")

#Only one node, launched with index for host node
#srun ~/BC-pipelines/BC_scripts/instructions.sh $json_file $index_host

srun --het-group=0 ~/BC-pipelines/BC_scripts/instructions.sh $json_file $index_host &   
sleep 10
srun --het-group=1 ~/BC-pipelines/BC_scripts/instructions.sh $json_file $((index_host + 1)) &
wait 