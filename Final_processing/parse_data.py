import os
import re
import csv
import json

# Function to load JSON data from a file
def load_json(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
        return data

def extrapolate_node_names(config, path_BCP_log):
    nodes_list = []
    for filename in os.listdir(path_BCP_log):
        if filename.startswith("BCProcessor_log_"):
            name = filename.split("_")[-1].split(".")[0]
            nodes_list.append(name)

    number_of_nodes = len(config['Resources']['nodes_list'])
    if  number_of_nodes != len(nodes_list):
        raise
    
    return nodes_list    

def parse_BCP_logs(config):

    path_BCP_log = config["Basecalling"]["logs_dir"]

    # List of node names
    try :
        nodes_list = extrapolate_node_names(config, path_BCP_log)
    except Exception as exc:
        print("Something went wrong. Log files indicates a different number of nodes")

    # Create a CSV file to store the extracted information
    csv_filename = 'output_' + config['General']['run_name'] + '.csv'

    with open(csv_filename, 'w', newline='') as csvfile:
        # Define CSV header
        fieldnames = ['Node', 'Input Read Files', 'Caller Time (ms)', 'Samples Called', 'Samples/s']
        csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write the header to the CSV file
        csv_writer.writeheader()

        # Loop through each node
        for node_name in nodes_list:
            log_filename = os.path.join(path_BCP_log, f'BCProcessor_log_{node_name}.txt')
            print(log_filename)

            # Check if the log file exists
            if os.path.exists(log_filename):
                with open(log_filename, 'r') as log_file:

                    content = log_file.read()
                    
                    # Initialize variables to store extracted information
                    input_read_files = None
                    caller_time = None
                    samples_called = None
                    samples_per_second = None

                    # Extracting information using regular expressions
                    input_read_files = re.findall(r'Found (\d+) input read file[s]? to process', content)
                    caller_time = re.findall(r'Caller time: (\d+) ms', content)
                    samples_called = re.findall(r'Samples called: (\d+)', content)
                    samples_per_second = re.findall(r'samples/s: ([\d.]+e[+\-]\d+)', content)

                    # Write the extracted information to the CSV file
                    csv_writer.writerow({
                        'Node': node_name,
                        'Input Read Files': input_read_files,
                        'Caller Time (ms)': caller_time,
                        'Samples Called': samples_called,
                        'Samples/s': samples_per_second
                    })
                    
                    # Debugging
                    #print("Node:", node_name)
                    #print("Input Read Files:", input_read_files)
                    #print("Caller Time (ms):", caller_time)
                    #print("Samples Called:", samples_called)
                    #print("Samples/s:", samples_per_second)


    print(f'Data has been extracted and saved to {csv_filename}')
    return csv_filename

def rework_csv(csv_filename):
    # Read the original CSV file
    with open(csv_filename, 'r') as file:
        reader = csv.DictReader(file)
        data = list(reader) 
    # Create a new list to store the modified data
    modified_data = []

    # Iterate through the original data
    for row in data:
        # Extract values from the lists
        node = row['Node']
        input_files = eval(row['Input Read Files'])
        caller_times = eval(row['Caller Time (ms)'])
        samples_called = eval(row['Samples Called'])
        samples_per_second = eval(row['Samples/s'])

        # Create a new row for each value in the lists
        for i in range(len(input_files)):
            new_row = {
                'Node': node,
                'Input Read Files': str(input_files[i]),
                'Caller Time (ms)': str(caller_times[i]),
                'Samples Called': str(samples_called[i]),
                'Samples/s': str(samples_per_second[i])
            }
            modified_data.append(new_row)

    # Write the modified data to a new CSV file
    new_csv_filename = csv_filename
    with open(new_csv_filename, 'w', newline='') as file:
        fieldnames = ['Node', 'Input Read Files', 'Caller Time (ms)', 'Samples Called', 'Samples/s']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        # Write the header
        writer.writeheader()

        # Write the modified data
        writer.writerows(modified_data)

    print(f'Modified CSV file created: {new_csv_filename}')