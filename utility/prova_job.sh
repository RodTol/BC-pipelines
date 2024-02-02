#!/bin/bash
#SBATCH --job-name=prova-job
#SBATCH --time=00:02:00
#SBATCH -o /orfeo/cephfs/home/area/jenkins_lage_test/BC-pipeline_orfeo/slurm.out
#SBATCH -p THIN --ntasks-per-node=1 --nodes=1

current_time=$(date +"%Y-%m-%d %H:%M:%S")
echo "Current time: $current_time"
echo "hello from ${SLURM_JOB_NODELIST}"


