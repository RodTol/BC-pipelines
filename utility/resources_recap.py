import json
import pandas as pd
import matplotlib.pyplot as plt
import sys

def create_table(json_path):
    # Load JSON data
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)
    
    # Extract relevant data
    nodes_queue = data["Resources"]["nodes_queue"]
    nodes_list = data["Resources"]["nodes_list"]           
    nodes_ip = data["Resources"]["nodes_ip"]
    nodes_cpus = data["Resources"]["nodes_cpus"]
    nodes_mem = data["Resources"]["nodes_mem"]
    nodes_gpus = data["Resources"]["nodes_gpus"]
    batch_size_list = data["Resources"]["batch_size_list"]
    
    # Create DataFrame
    df = pd.DataFrame({
        'Nodes Queue': nodes_queue,
        'Nodes List': nodes_list,
        'Nodes IP': nodes_ip,
        'Nodes CPUs': nodes_cpus,
        'Nodes Memory': nodes_mem,
        'Nodes GPUs': nodes_gpus,
        'Batch Size': batch_size_list
    })

    # Plot table
    plt.figure(figsize=(10, 6))
    table = plt.table(cellText=df.values,
                      colLabels=df.columns,
                      cellLoc='center',
                      loc='center',
                      colColours=[(0.9, 0.9, 1)] * len(df.columns))  # Light blue background for column labels

    # Bold text in the first row
    for (i, j), cell in table.get_celld().items():
        if i == 0:  # First row
            cell.set_text_props(fontweight='bold')

    table.scale(1, 2.5)
    plt.axis('off')  # Turn off axis
    plt.title('Resource Information')
    
    # Save table as image
    plt.savefig('resource_table.png', bbox_inches='tight')

if __name__ == "__main__":
    # Check if the path to JSON file is provided
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_json>")
        sys.exit(1)

    json_path = sys.argv[1]
    create_table(json_path)
