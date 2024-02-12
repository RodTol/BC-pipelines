#!/bin/bash
#SBATCH --job-name=het-dorado
#SBATCH --time=04:00:00
#SBATCH -p DGX --ntasks-per-node=1 --nodes=1 --cpus-per-task=256 --gpus=8 --nodelist=dgx002
#SBATCH hetjob
#SBATCH -p GPU --nodes=1 --ntasks-per-node=1 --cpus-per-task=48 --nodelist=gpu004
#SBATCH hetjob
#SBATCH -p GPU --nodes=1 --ntasks-per-node=1 --cpus-per-task=48 --nodelist=gpu003
#SBATCH hetjob
#SBATCH -p GPU --nodes=1 --ntasks-per-node=1 --cpus-per-task=48 --nodelist=gpu002
#SBATCH hetjob
#SBATCH -p GPU --nodes=1 --ntasks-per-node=1 --cpus-per-task=48 --nodelist=gpu001

##SBATCH hetjob
##SBATCH -p DGX --ntasks-per-node=1 --nodes=1 --cpus-per-task=256 --gpus=8 --nodelist=dgx001


echo "1_dgx-4_gpu SUP"
srun --het-group=0 script_dgx2.sh &
sleep 3
#srun --het-group=1 script_dgx1.sh &
srun --het-group=1 script_gpu4.sh &
srun --het-group=2 script_gpu3.sh &
srun --het-group=3 script_gpu2.sh &
srun --het-group=4 script_gpu1.sh &
wait
