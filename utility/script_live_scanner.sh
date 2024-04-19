#!/bin/bash
#SBATCH --job-name=live_scanner_jenkins
#SBATCH --time=03:00:00
#SBATCH --output=/u/area/jenkins_onpexp/scratch/jenkins_logs/tmp/live_scanner.out
#SBATCH --error=/u/area/jenkins_onpexp/scratch/jenkins_logs/tmp/live_scanner.err
#SBATCH -A lage
#SBATCH -p EPYC
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=6
#SBATCH --mem=10GB

# The $1 argument is the path to the template_config.json file

source /u/area/jenkins_onpexp/python_venvs/epyc_venv_jenkins/bin/activate
python3 /u/area/jenkins_onpexp/BC-pipelines/utility/main.py Alfredo95 elefante $1
