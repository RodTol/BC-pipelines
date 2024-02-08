#!/bin/bash
#SBATCH --job-name=jk-try
#SBATCH --time=00:05:00
#SBATCH --output=/u/area/jenkins_onpexp/jenkins_logs
#SBATCH -p DGX --nodes=1 --ntasks-per-node=1 --cpus-per-task=1 --gpus=1
#SBATCH hetjob
#SBATCH -p GPU --nodes=1 --ntasks-per-node=1 --cpus-per-task=24


srun --het-group=0 ~/BC-pipelines/basecalling-pipeline/BC_scripts/host/prova.sh &
sleep 10
srun --het-group=1 ~/BC-pipelines/basecalling-pipeline/BC_scripts/client/prova.sh &
wait
