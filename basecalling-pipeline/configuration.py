import sys
import json

def load_json(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
        return data
    
def create_sbatch_file(config):
    run_name = config['General']['run_name']

    # Define the content of the sbatch script
    sbatch_content = f'''#!/bin/bash
#SBATCH --job-name={run_name}
#SBATCH --nodes={nodes}
#SBATCH --ntasks-per-node={tasks_per_node}
#SBATCH --time=1:00:00
#SBATCH --job-name={script_name}
#SBATCH --output={script_name}_%j.out
#SBATCH --error={script_name}_%j.err


srun ~/BC-pipelines/utility/prova.sh
'''

    # Write the content to the sbatch script file
    with open(script_name + ".sbatch", "w") as sbatch_file:
        sbatch_file.write(sbatch_content)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error!")
        print("Usage: python script.py <path_to_json_file>")
        sys.exit(1)
    
    json_file = sys.argv[1]
    config = load_json(json_file)

    model = config['Basecalling']['model']
    input_dir = config['Basecalling']['input_dir']
    output_dir = config['Basecalling']['output_dir']
    logs_dir = config['Basecalling']['logs_dir']
    
    print(f"Selected MODEL : {model}")
    print(f"Value of INPUT_DIR: {input_dir}")
    print(f"Value of OUTPUT_DIR: {output_dir}")
    print(f"Value of LOGS_DIR: {logs_dir}")

