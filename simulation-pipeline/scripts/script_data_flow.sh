#!/bin/bash
#SBATCH --job-name=data_flow
#SBATCH --time=06:00:00
#SBATCH --output=/u/area/jenkins_onpexp/scratch/jenkins_logs/tmp/data_flow.out
#SBATCH --error=/u/area/jenkins_onpexp/scratch/jenkins_logs/tmp/data_flow.err
#SBATCH -A lage
#SBATCH -p DGX
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=6
#SBATCH --mem=10GB

source=$1
dest=$2

#source /u/area/jenkins_onpexp/python_venvs/epyc_venv_jenkins/bin/activate
source /u/area/jenkins_onpexp/python_venvs/dgx_venv_jenkins/bin/activate

python3 /u/area/jenkins_onpexp/BC-pipelines/simulation-pipeline/utility/data_flow_emulator.py $source $dest