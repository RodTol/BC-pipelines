import os
import re
import csv
import sys
import json

# Function to load JSON data from a file
def load_json(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
        return data


def parse_BCP_logs(config, path_BCP_log):
    # Define the pattern to match the lines in the log files
    pattern = re.compile(r'Found (\d+) input read files to process\.\s+Processing \.\.\.\s+Caller time: (\d+) ms, Samples called: (\d+), samples/s: ([\d\.]+)')

    # List of node names
    nodes_list = config['Resources']['nodes_list']

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
                    # Initialize variables to store extracted information
                    input_read_files = None
                    caller_time = None
                    samples_called = None
                    samples_per_second = None

                    # Loop through each line in the log file
                    for line in log_file:
                        match = pattern.search(line)
                        if match:
                            input_read_files, caller_time, samples_called, samples_per_second = match.groups()
                            break

                    # Write the extracted information to the CSV file
                    csv_writer.writerow({
                        'Node': node_name,
                        'Input Read Files': input_read_files,
                        'Caller Time (ms)': caller_time,
                        'Samples Called': samples_called,
                        'Samples/s': samples_per_second
                    })

    print(f'Data has been extracted and saved to {csv_filename}')


if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 3:
        print("Error!")
        print("Usage: python script.py <path_to_json_file>")
        sys.exit(1)
    
    # Load the configuration from the specified JSON file
    json_file = sys.argv[1]
    path_BCP_log = sys.argv[2]

    config = load_json(json_file)

    parse_BCP_logs(config, path_BCP_log)