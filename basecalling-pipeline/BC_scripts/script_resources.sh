#!/bin/bash
#SBATCH --job-name=jk-try
#SBATCH --time=00:10:00
#SBATCH --output=/orfeo/LTS/LADE/LT_storage/tolloi
#SBATCH -p DGX --ntasks-per-node=1 --nodes=1 --cpus-per-task=1 --gpus=0
#SBATCH hetjob
#SBATCH -p GPU --nodes=1 --ntasks-per-node=1 --cpus-per-task=1


srun --het-group=0 ~/BC-pipelines/basecalling-pipeline/BC_scripts/host/prova.sh &
sleep 10
srun --het-group=1 ~/BC-pipelines/basecalling-pipeline/BC_scripts/client/prova.sh &
wait
