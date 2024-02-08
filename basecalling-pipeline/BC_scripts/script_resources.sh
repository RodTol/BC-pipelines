#!/bin/bash
#SBATCH --job-name=jk-try
#SBATCH --time=00:05:00
#SBATCH --output=/u/area/jenkins_onpexp/jenkins_logs/tmp/%x-%j.out  # Use %x for job name and %j for job ID
#SBATCH --error=/u/area/jenkins_onpexp/jenkins_logs/tmp/%x-%j.err   # Use %x for job name and %j for job ID
#SBATCH -p DGX --nodes=1 --ntasks-per-node=1 --cpus-per-task=1 --gpus=1
#SBATCH hetjob
#SBATCH -p GPU --nodes=1 --ntasks-per-node=1 --cpus-per-task=24

echo "id"
cd ~
pwd

srun --het-group=0 ~/BC-pipelines/basecalling-pipeline/BC_scripts/host/instructions.sh &
sleep 10
srun --het-group=1 ~/BC-pipelines/basecalling-pipeline/BC_scripts/client/instructions.sh &
wait
