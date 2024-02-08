#!/bin/bash
#SBATCH --job-name=jk-try
#SBATCH --time=00:05:00
#SBATCH --output=/u/area/jenkins_onpexp/jenkins_logs/tmp/%x-%j.out  
#SBATCH --error=/u/area/jenkins_onpexp/jenkins_logs/tmp/%x-%j.err   
#SBATCH -p DGX --nodes=1 --ntasks-per-node=1 --cpus-per-task=1 --gpus=1
#SBATCH hetjob
#SBATCH -p GPU --nodes=1 --ntasks-per-node=1 --cpus-per-task=24

json_file=$1

model=$(jq -r '.Basecalling.model' "$json_file")
logs_dir=$(jq -r '.Basecalling.logs_dir' "$json_file")

echo "Model: $model"
echo "Logs Directory: $logs_dir"


srun --het-group=0 ~/BC-pipelines/basecalling-pipeline/BC_scripts/host/instructions.sh $model $logs_dir &
sleep 10
srun --het-group=1 ~/BC-pipelines/basecalling-pipeline/BC_scripts/client/instructions.sh $model $logs_dir &
wait
