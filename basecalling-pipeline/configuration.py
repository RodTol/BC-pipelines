import sys
import json

def load_json(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
        return data
    
def create_sbatch_file(config):
    run_name = config['General']['run_name']
    nodes_list = config['Resources']['nodes_list']
    # Define the content of the sbatch script
    sbatch_content = f'''**********PYTHON SCRIPT**********
#!/bin/bash
#SBATCH --job-name={run_name}
#SBATCH --time=00:20:00
#SBATCH --output=/u/area/jenkins_onpexp/scratch/jenkins_logs/tmp/%x-%j.out  
#SBATCH --error=/u/area/jenkins_onpexp/scratch/jenkins_logs/tmp/%x-%j.err  

#SBATCH -A lage -p DGX --nodelist={nodes_list[0]} --nodes=1 --ntasks-per-node=1 --cpus-per-task=24 --gpus=2
#SBATCH hetjob
#SBATCH -A lage -p DGX --nodelist={nodes_list[0]} --nodes=1 --ntasks-per-node=1 --cpus-per-task=1

json_file=$1
index_host=$(jq -r '.Resources.index_host' "$json_file")

#Only one node, launched with index for host node
#srun ~/BC-pipelines/BC_scripts/instructions.sh $json_file $index_host

srun --het-group=0 ~/BC-pipelines/BC_scripts/instructions.sh $json_file $index_host
sleep 10
srun --het-group=1 ~/BC-pipelines/utility/prova.sh
'''
    # Write the content to the sbatch script file
    with open("script_resources.sh", "w") as sbatch_file:
        sbatch_file.write(sbatch_content)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error!")
        print("Usage: python script.py <path_to_json_file>")
        sys.exit(1)
    
    json_file = sys.argv[1]
    config = load_json(json_file)

    create_sbatch_file(config)

    model = config['Basecalling']['model']
    input_dir = config['Basecalling']['input_dir']
    output_dir = config['Basecalling']['output_dir']
    logs_dir = config['Basecalling']['logs_dir']
    
    print(f"Selected MODEL : {model}")
    print(f"Value of INPUT_DIR: {input_dir}")
    print(f"Value of OUTPUT_DIR: {output_dir}")
    print(f"Value of LOGS_DIR: {logs_dir}")

