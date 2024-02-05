#!/bin/bash
#SBATCH --job-name=jk-try
#SBATCH --time=00:10:00
#SBATCH -p DGX --ntasks-per-node=1 --nodes=1 --cpus-per-task=1 --gpus=0 --nodelist=dgx002
#SBATCH hetjob
#SBATCH -p GPU --nodes=1 --ntasks-per-node=1 --cpus-per-task=1 --nodelist=gpu004

##SBATCH hetjob
##SBATCH -p DGX --ntasks-per-node=1 --nodes=1 --cpus-per-task=256 --gpus=8 --nodelist=dgx001
##SBATCH hetjob
##SBATCH -p GPU --nodes=1 --ntasks-per-node=1 --cpus-per-task=48 --nodelist=gpu003
##SBATCH hetjob
##SBATCH -p GPU --nodes=1 --ntasks-per-node=1 --cpus-per-task=48 --nodelist=gpu002
##SBATCH hetjob
##SBATCH -p GPU --nodes=1 --ntasks-per-node=1 --cpus-per-task=48 --nodelist=gpu001


srun --het-group=0 ~/BC-pipelines/utility/prova_job.sh &
sleep 10
srun --het-group=1 ~/BC-pipelines/utility/prova_job.sh &
wait
