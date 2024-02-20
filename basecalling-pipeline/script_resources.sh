#!/bin/bash
#SBATCH --job-name=ExampleRun_1_Dgx
#SBATCH --time=00:20:00
#SBATCH --output=/u/area/jenkins_onpexp/scratch/jenkins_logs/tmp/%x-%j.out
#SBATCH --error=/u/area/jenkins_onpexp/scratch/jenkins_logs/tmp/%x-%j.err

#SBATCH -A lage -p DGX --nodelist=dgx001 --nodes=1 --ntasks-per-node=1 --cpus-per-task=64 --gpus 8


json_file=$1
index_host=$(jq -r '.Resources.index_host' '$json_file')

srun /u/area/jenkins_onpexp/BC-pipelines/BC_scripts/instructions.sh  $json_file $((index_host + 0)) &
wait
#**********WRITTEN BY CONFIGURATION.PY**********
