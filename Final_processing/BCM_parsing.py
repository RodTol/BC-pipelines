import re
import pandas as pd

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
    pattern = r'\[(.*?)\]'
    
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
    
    print("JOB ID: ", job_id)
    print("Start time: ", start_time)
    print("End time: ", end_time)

    times = [start_time, end_time]

    return times

def insert_times_in_df(log_file_path, df):
    start_times = []
    end_times = []
    for index, row in  df.iterrows():
        start_run_for_this_ip = []
        end_run_for_this_ip = []
        for job_id in row['job_ids']:
            times = find_for_job_id_times(log_file_path, job_id)
            start_run_for_this_ip.append(times[0])
            end_run_for_this_ip.append(times[1])
        start_times.append(start_run_for_this_ip)
        end_times.append(end_run_for_this_ip)
    
    df['start_times'] = start_times
    df['end_times'] = end_times

    return None


# Usage examples
log_file_path = "BCManager_log.txt"


# Finding unique IP addresses
unique_ips = find_unique_ips(log_file_path)
table = pd.DataFrame({'ips' : list(unique_ips)})
print(table)

# Counting job IDs associated with each IP address
job_ids = []
for ips in unique_ips:
    job_ids.append(list(find_job_id(log_file_path, ips)))
table["job_ids"] = job_ids
print(table)

insert_times_in_df(log_file_path, table)
print(table)