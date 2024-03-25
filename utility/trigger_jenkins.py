import sys
import jenkins
from datetime import datetime
import re
import time
import os

def get_current_stage(server, job_name, build_number, build_status, previous_stage = None):
    while build_status not in ['SUCCESS', 'UNSTABLE', 'FAILURE', 'NOT_BUILT', 'ABORTED']  :
        console_output = server.get_build_console_output(job_name, build_number)
        #print(console_output)

        for i,line in enumerate(console_output.split('\n')):
                if line.endswith("[Pipeline] stage") and i < len(console_output.split('\n')) - 1:
                    last_stage_line = console_output.split('\n')[i + 1]

        #print(last_stage_line)
        pattern = r'\((.*?)\)'
        match = re.search(pattern, last_stage_line)    

        if match:
            stage = match.group(1)
            if previous_stage != stage:
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                print(f"{timestamp} - Stage : {stage}")
                print("Build is ", build_status)
                previous_stage = stage
            #else if previous_stage = 'Send Report to User':
    print("Build is ", build_status)


def trigger_jenkins_pipeline(jenkins_url, job_name, username, password, parameters, token):
    
    server = jenkins.Jenkins(jenkins_url, username=username, password=password)
    #server.build_job(job_name, parameters, token=token)
    # Startup time for the build
    time.sleep(5)

    last_build_number = server.get_job_info('tolloi/basecalling_pipeline')['lastBuild']['number']
    build_info = server.get_build_info('tolloi/basecalling_pipeline', last_build_number)

    # Convert duration from milliseconds to seconds
    duration_seconds = build_info['duration'] / 1000

    # Convert timestamp to standard date format
    timestamp_seconds = build_info['timestamp'] / 1000
    timestamp_date = datetime.utcfromtimestamp(timestamp_seconds).strftime('%Y-%m-%d %H:%M:%S')

    # Print basic information about the build
    print("Build Number:", build_info['number'])
    print("Result:", build_info['result'])
    print("Duration (seconds):", duration_seconds)
    print("Timestamp (UTC):", timestamp_date)
    print("url", build_info['url'])

    get_current_stage(server, job_name, last_build_number, build_info['result'])


def count_files(dir_path):
    file_count = 0
    for _, _, files in os.walk(dir_path):
        file_count += len(files)

    return file_count

def create_input_dir(input_dir_path):
    tmp_dir = 'tmp_ASSIGNED'
    dirfullpath = os.path.join(tmp_dir, input_dir_path)
    os.mkdir(dirfullpath)


def live_reading_dir(input_dir_path, threshold=5, scanning_time=10):
    '''
    The purpouse of this function is to scan the input directory and trigger
    the basecalling pipeline when we have added more than "threshold" files.
    Idea: 
    1. Each 10 seconds the dir will be scanned
    2. If # of files has reached a threshold, create a tmp dir with a work 
    batch. Save what files have been assigned 
    3. Keep scanning the dir and repeat
    '''
    assigned_files = []
    prev_total_files = 0
    while True:
        curr_total_files = count_files(input_dir_path)
        print("Current amount of files : ", curr_total_files, "Previous : ", prev_total_files)
        time.sleep(10)


if __name__ == "__main__":
    # Authentication
    password = sys.argv[1]
    username ="tolloi"

    token = sys.argv[2]

    # Jenkins URL
    jenkins_url = "http://jenkins-sandbox.rd.areasciencepark.it:8080" 
    # Jenkins job name
    job_name = "tolloi/basecalling_pipeline"  
    # Parameters for the Jenkins pipeline
    config_path = {
        "configFilePath": "/u/area/jenkins_onpexp/BC-pipelines/configurations/config_1_dgx.json",
    }

    # Trigger the Jenkins pipeline with parameters
    #trigger_jenkins_pipeline(jenkins_url, job_name, username, password, config_path, token)
    live_reading_dir('$HOME/dataset_10G_bc')
