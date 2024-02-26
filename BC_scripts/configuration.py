import sys
import json

# Function to load JSON data from a file
def load_json(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
        return data


'''
 Function to create a Slurm sbatch script based on a configuration
 file (config.json). See the documentation to understand what each 
 parameter represents
'''
def create_sbatch_file(config):
    # Get the number of nodes that will be used for the basecalling
    how_many_nodes = len(config['Resources']['nodes_list'])

    # Open the sbatch file for writing
    with open("script_resources.sh", "w") as sbatch_file:
        # Write the basic sbatch directives
        sbatch_file.write('#!/bin/bash\n')
        sbatch_file.write(f"#SBATCH --job-name={config['General']['run_name']}\n")
        sbatch_file.write(f"#SBATCH --time={config['General']['run_time']}\n")
        sbatch_file.write(f"#SBATCH --output={config['Slurm']['output']}\n")
        sbatch_file.write(f"#SBATCH --error={config['Slurm']['error']}\n")
        
        sbatch_file.write("\n")

        # Loop through each node and write its directives
        for i in range(how_many_nodes):
            sbatch_file.write(f"#SBATCH -A lage -p {config['Resources']['nodes_queue'][i]}")
            sbatch_file.write(f" --nodelist={config['Resources']['nodes_list'][i]}")
            sbatch_file.write(f" --nodes=1 --ntasks-per-node=1")
            sbatch_file.write(f" --cpus-per-task={config['Resources']['nodes_cpus'][i]}")
            
            if config['Resources']['nodes_gpus'][i] != "None":
                sbatch_file.write(f" --gpus {config['Resources']['nodes_gpus'][i]}\n")
            else:
                sbatch_file.write("\n")

            # Add a hetjob directive after each node except the last one
            if i != how_many_nodes-1:
                sbatch_file.write("#SBATCH hetjob\n\n")
            else:
                sbatch_file.write("\n")

        sbatch_file.write("\n")
        
        # Write additional sbatch directives for script execution
        sbatch_file.write('json_file=$1\n')
        sbatch_file.write("index_host=$(jq -r '.Resources.index_host' ")
        sbatch_file.write('"$json_file")\n')
        sbatch_file.write("echo 'INDEX_HOST' $index_host\n")

        sbatch_file.write("\n")

        # Loop through each node and write srun commands
        for i in range(how_many_nodes):
            # If I have only one node I do not need to use het-group
            if how_many_nodes == 1:
                sbatch_file.write(f"srun ")
            else:
                sbatch_file.write(f"srun --het-group={i} ")

            sbatch_file.write(f"{config['Slurm']['instructions']} $json_file $((index_host + {i})) &\n")

            # Add a sleep command after each srun command except the last one
            if i != how_many_nodes-1:
                sbatch_file.write("sleep 5\n")
            else:
                sbatch_file.write("wait\n")

        # Add a comment indicating the script was generated by configuration.py
        sbatch_file.write('#**********WRITTEN BY CONFIGURATION.PY**********\n')

if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 2:
        print("Error!")
        print("Usage: python script.py <path_to_json_file>")
        sys.exit(1)
    
    # Load the configuration from the specified JSON file
    json_file = sys.argv[1]
    config = load_json(json_file)

    # Generate the sbatch script based on the configuration
    create_sbatch_file(config)
