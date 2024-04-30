import re
import sys
import json
import os
import pandas as pd
from datetime import datetime

import matplotlib.pyplot as plt
import hashlib
import numpy as np

def generate_colors(ips):
    colors = []
    np.random.seed(1)  # Set a fixed seed for reproducibility
    for ip in ips:
        # Convert the IP address to a unique hash
        hash_object = hashlib.md5(ip.encode())
        hash_digest = hash_object.hexdigest()
        
        # Take the first 6 characters of the hash to represent the color
        color_hex = '#' + hash_digest[:6]
        
        # Convert hex color to RGB
        r = int(color_hex[1:3], 16) / 255.0
        g = int(color_hex[3:5], 16) / 255.0
        b = int(color_hex[5:7], 16) / 255.0
        
        # Normalize RGB values to fit into Viridis colormap
        color = np.array([r, g, b]).reshape(1, -1)
        viridis_color = plt.cm.viridis(color)[0, :3]  # Get RGB values from Viridis colormap
        
        colors.append(viridis_color)
    
    return colors

# Function to load JSON data from a file
def load_json(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
        return data

def find_unique_ips(log_file):
    unique_ips = set()
    with open(log_file, 'r') as file:
        # Skipping the first 8 lines
        for _ in range(8):
            next(file)
        # Reading the remaining lines and extracting IPs
        for line in file:
            if line.strip():
                ip_address = line.split()[0]
                unique_ips.add(ip_address)
    return unique_ips

def find_job_id(log_file, ip_address):
    jobs = set()
    with open(log_file, 'r') as file:
        ip_pattern = re.compile(r'^{}.*'.format(re.escape(ip_address)))
        job_id_pattern = re.compile(r'job_id=(\d+)')
        line_number = 0
        for line in file:
            line_number += 1
            if line_number < 8:
                continue  # Skip lines until the 8th line
            if ip_pattern.match(line):
                match = job_id_pattern.search(line)
                if match:
                    jobs.add(match.group(1))

    return jobs

def extract_timestamp(line):
    # Regular expression pattern to extract timestamp between []
    pattern = r'\[\d{2}/\w{3}/\d{4} (\d{2}:\d{2}:\d{2})\]'
    
    # Using re.search() to find the first match of the pattern
    match = re.search(pattern, line)
    
    if match:
        # Extracting the timestamp from the matched group
        timestamp = match.group(1)
        return timestamp
    else:
        return None

def find_for_job_id_times(log_file, job_id):
    matching_lines = []
    with open(log_file, 'r') as file:
        for line in file:
            if f'job_id={job_id}' in line:
                matching_lines.append(line)

    #save first as starting and last as ending time
    start_time = extract_timestamp(matching_lines[0])
    end_time = extract_timestamp(matching_lines[-1])
    
    #print("JOB ID: ", job_id)
    #print("Start time: ", start_time)
    #print("End time: ", end_time)

    time_format = "%H:%M:%S"
    time1 = datetime.strptime(start_time, time_format)
    time2 = datetime.strptime(end_time, time_format)

    # Calculate the time difference
    elapsed_time = (time2 - time1).total_seconds()

    times = [start_time, end_time, elapsed_time]

    return times

def insert_times_in_df(log_file_path, df):
    start_times = []
    end_times = []
    elapsed_times = []
    for index, row in  df.iterrows():
        start_run_for_this_ip = []
        end_run_for_this_ip = []
        elapsed_run_for_this_ip = []
        for job_id in row['job_ids']:
            times = find_for_job_id_times(log_file_path, job_id)
            start_run_for_this_ip.append(times[0])
            end_run_for_this_ip.append(times[1])
            elapsed_run_for_this_ip.append(times[2])
        start_times.append(start_run_for_this_ip)
        end_times.append(end_run_for_this_ip)
        elapsed_times.append(elapsed_run_for_this_ip)
    
    df['start_times'] = start_times
    df['end_times'] = end_times
    df['elapsed_times'] = elapsed_times

    return None


def plot(df):

    colors = generate_colors(df['ips'])
    x = [0]
    for i, row in df.iterrows():
        x.append((len(row['job_ids'])+1)*0.25)
    # Plot each row
    for i, row in df.iterrows():
        for j, elapsed_time in enumerate(row['elapsed_times']):
            if j==0:
                plt.bar(x[i] + j*0.25, elapsed_time, label=row['ips'], color=colors[i], width=0.2, align='center')
            else:
                plt.bar(x[i] + j*0.25, elapsed_time, color=colors[i], width=0.2, align='center')
    plt.ylabel('Elapsed Time')
    plt.xlabel('IPs')
    plt.title('Elapsed Time by IP Address')

    # Set x-axis ticks and labels to empty list
    plt.xticks([], [])

    # Create legend
    plt.legend()

    # Save the plot to a file
    plt.savefig('plot_times.png')

if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 2:
        print("Error!")
        print("Usage: python script.py <path_to_json_file>")
        sys.exit(1)
    
    # Load the configuration from the specified JSON file
    json_file = sys.argv[1]
    config = load_json(json_file)

    # Usage examples
    path_to_log_dir = config["Basecalling"]["logs_dir"]
    log_file_name = "BCManager_log.txt"
    log_file_path = os.path.join(path_to_log_dir, log_file_name)


    # Finding unique IP addresses
    unique_ips = find_unique_ips(log_file_path)
    table = pd.DataFrame({'ips' : list(unique_ips)})

    # Counting job IDs associated with each IP address
    job_ids = []
    for ips in unique_ips:
        job_ids.append(list(find_job_id(log_file_path, ips)))
    table["job_ids"] = job_ids

    insert_times_in_df(log_file_path, table)

    #print(table)
    # Create a CSV file to store the extracted information
    csv_output = 'times_' + config['General']['run_name'] + '.csv'
    table.to_csv(csv_output, index=False)

    plot(table)