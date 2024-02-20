import sys
import json

def load_json(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
        return data

# Only need is to have host node as first one! INDEX HOST ALWAYS 0!
def create_sbatch_file(config):
    # Define the content of the sbatch script
    how_many_nodes = len(config['Resources']['nodes_list'])

    with open("script_resources.sh", "w") as sbatch_file:
        sbatch_file.write('#!/bin/bash\n')
        sbatch_file.write(f"#SBATCH --job-name={config['General']['run_name']}\n")
        sbatch_file.write(f"#SBATCH --time={config['General']['run_time']}\n")
        sbatch_file.write(f"#SBATCH --output={config['Slurm']['output']}\n")
        sbatch_file.write(f"#SBATCH --error={config['Slurm']['error']}\n")
        
        sbatch_file.write("\n")

        for i in range(how_many_nodes):
            sbatch_file.write(f"#SBATCH -A lage -p {config['Resources']['nodes_queue'][i]}")
            sbatch_file.write(f" --nodelist={config['Resources']['nodes_list'][i]}")
            sbatch_file.write(f" --nodes=1 --ntasks-per-node=1")
            sbatch_file.write(f" --cpus-per-task={config['Resources']['nodes_cpus'][i]}")
            
            if config['Resources']['nodes_gpus'][i] != "None":
                sbatch_file.write(f" --gpus {config['Resources']['nodes_gpus'][i]}\n")
            else:
                sbatch_file.write("\n")

            if i!=how_many_nodes-1:
                sbatch_file.write("#SBATCH hetjob\n\n")
            else :
                sbatch_file.write("\n")

        sbatch_file.write("\n")
        
        sbatch_file.write('json_file=$1\n')
        sbatch_file.write("index_host=$(jq -r '.Resources.index_host' '$json_file')\n")

        sbatch_file.write("\n")

        for i in range(how_many_nodes):
            if how_many_nodes==1:
                sbatch_file.write(f"srun ")
            else :
                sbatch_file.write(f"srun --het-group={i} ")

            sbatch_file.write(f"{config['Slurm']['instructions']} $json_file $((index_host + {i})) &\n")

            if i!=how_many_nodes-1:
                sbatch_file.write("sleep 5\n")
            else :
                sbatch_file.write("wait\n")

        sbatch_file.write('#**********WRITTEN BY CONFIGURATION.PY**********\n')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error!")
        print("Usage: python script.py <path_to_json_file>")
        sys.exit(1)
    
    json_file = sys.argv[1]
    config = load_json(json_file)

    create_sbatch_file(config)

    # model = config['Basecalling']['model']
    # input_dir = config['Basecalling']['input_dir']
    # output_dir = config['Basecalling']['output_dir']
    # logs_dir = config['Basecalling']['logs_dir']
    
    # print(f"Selected MODEL : {model}")
    # print(f"Value of INPUT_DIR: {input_dir}")
    # print(f"Value of OUTPUT_DIR: {output_dir}")
    # print(f"Value of LOGS_DIR: {logs_dir}")

