#!/bin/bash
#SBATCH --job-name=live_scanner_jenkins
#SBATCH --time=12:00:00
#SBATCH --output=/u/area/jenkins_onpexp/scratch/jenkins_logs/tmp/live_scanner.out
#SBATCH --error=/u/area/jenkins_onpexp/scratch/jenkins_logs/tmp/live_scanner.err
#SBATCH -A lage
#SBATCH -p DGX
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=20
#SBATCH --mem=200GB

# The $1 argument is the path to the template_config.json file
# The $2 is the path to the input directory that will be studied

source /u/area/jenkins_onpexp/python_venvs/epyc_venv_jenkins/bin/activate
python3 /u/area/jenkins_onpexp/BC-pipelines/simulation-pipeline/utility/main.py Alfredo95 elefante $1 $2
