#!/bin/bash
#SBATCH --job-name=jk-try
#SBATCH --time=00:10:00
#SBATCH --output=/u/dssc/tolloi/LTS/jenkins-jobs-logs
#SBATCH -p DGX --ntasks-per-node=1 --nodes=1 --cpus-per-task=1 --gpus=0
#SBATCH hetjob
#SBATCH -p GPU --nodes=1 --ntasks-per-node=1 --cpus-per-task=1


srun --het-group=0 ~/BC-pipelines/utility/prova_job.sh &
sleep 10
srun --het-group=1 ~/BC-pipelines/utility/prova_job.sh &
wait
