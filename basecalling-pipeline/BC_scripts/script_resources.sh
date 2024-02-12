#!/bin/bash
#SBATCH --job-name=jk-try
#SBATCH --time=00:20:00
#SBATCH --output=/u/area/jenkins_onpexp/scratch/jenkins_logs/tmp/%x-%j.out  
#SBATCH --error=/u/area/jenkins_onpexp/scratch/jenkins_logs/tmp/%x-%j.err   
#SBATCH -A lage -p DGX --nodes=1 --ntasks-per-node=1 --cpus-per-task=24 --gpus=2

##SBATCH hetjob
##SBATCH -A lage -p DGX --nodes=1 --ntasks-per-node=1 --cpus-per-task=24

json_file=$1

#only one node
srun ~/BC-pipelines/basecalling-pipeline/BC_scripts/host/instructions.sh $json_file &

#srun --het-group=0 ~/BC-pipelines/basecalling-pipeline/BC_scripts/host/instructions.sh $json_file &
sleep 10
#run --het-group=1 ~/BC-pipelines/basecalling-pipeline/BC_scripts/client/instructions.sh $model $logs_dir &
wait
