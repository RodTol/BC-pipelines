import sys
import jenkins
from datetime import datetime
import re
import time
import os
import uuid
import json
import shutil
# I need to rewrite the function in order to raise the exception!
from pathlib import Path
from typing import Callable, Dict, List
import pod5
from pod5.tools.pod5_inspect import do_debug_command, do_read_command, do_reads_command, do_summary_command
from pod5.tools.utils import collect_inputs
from pod5.tools.parsers import prepare_pod5_inspect_argparser


def inspect_pod5(
    command: str, input_files: List[Path], recursive: bool = False, **kwargs
):
    """
    Determine which inspect command to run from the parsed arguments and run it.

    Rewrote by myself in order to throw an exception in case something went wrong
    (like in my case the file is yet to to be finished to be copied).
    """

    commands: Dict[str, Callable] = {
        "reads": do_reads_command,
        "read": do_read_command,
        "summary": do_summary_command,
        "debug": do_debug_command,
    }

    for idx, filename in enumerate(
        collect_inputs(input_files, recursive=recursive, pattern="*.pod5")
    ):
        try:
            reader = pod5.Reader(filename)
        except Exception as exc:
            print(f"Failed to open pod5 file: {filename}: {exc}", file=sys.stderr)
            raise #ONLY DIFFERENCE

        kwargs["reader"] = reader
        kwargs["write_header"] = idx == 0
        commands[command](**kwargs)


class Jenkins_trigger:

    def __init__(self, jenkins_url, username, password, token): 

        self.jenkins_url=jenkins_url
        self.username = username
        self.password = password
        self.token = token

        # Jenkins server
        self.server = jenkins.Jenkins(self.jenkins_url, username=self.username, password=self.password)
        user = self.server.get_whoami()
        version = self.server.get_version()
        print('Hello %s from Jenkins %s' % (user['fullName'], version))


    def __get_current_stage(self,job_name, build_number, build_status, previous_stage = None):
        while build_status not in ['SUCCESS', 'UNSTABLE', 'FAILURE', 'NOT_BUILT', 'ABORTED']  :
            console_output = self.server.get_build_console_output(job_name, build_number)
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
                elif stage == 'Send Report to User':
                    break
        print("Build is ", build_status)        
 

    def trigger_jenkins_pipeline(self, job_name, parameters):
        
        #Trigger the build on jenkins
        queue_item = self.server.build_job(job_name, parameters, token=self.token)

        #Get build number and infos
        while True:
            queue_info = self.server.get_queue_item(queue_item)
            if 'executable' in queue_info:
                build_info = self.server.get_build_info(job_name, queue_info['executable']['number'])
                break
            else:
                print("Build not started yet. Waiting...")
                time.sleep(5)  # Wait for 5 seconds before checking the queue again            

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

        self.__get_current_stage(job_name, build_info['number'], build_info['result'])


class Live_Reading :

    def __init__(self, input_dir, Jenkins_handler, Jenkins_job_name, Jenkins_job_config) :
        self.input_dir = input_dir
        self.Jenkins = Jenkins_handler
        self.job_name = Jenkins_job_name 
        self.job_config = Jenkins_job_config

    def __list_all_pod5_files(self) :
        '''
        This function will list only the closed files, which means
        that they are fully copied into the filesystem. If a file is open, an
        exception will be thrown and catched and a debug message printed. This
        will continue until the file is closed 
        '''
        pod5_files = []
        all_files= os.listdir(self.input_dir)
        
        print("Reading...")

        for file in all_files:
            # Check if it is .pod5
            if file.endswith('.pod5'):
                # Check if it is closed
                path_to_file = os.path.join(self.input_dir, file)

                # I have to parse the inputs with the provided parser
                parser = prepare_pod5_inspect_argparser()
                args = parser.parse_args(['debug', path_to_file])

                # Redirect stdout in order to have no prints
                sys.stdout = open(os.devnull, 'w')
                try :
                    inspect_pod5(command=args.command, input_files=args.input_files)
                except Exception as exc:
                    # This is how we handle this exception THAT IS NOT RAISEED
                    sys.stdout = sys.__stdout__ 
                    #print(f"Failed to open file {file} due to {exc}") 
                else:
                    # But we must reset stdout to its default value every time
                    sys.stdout = sys.__stdout__ 
                    #print('Added ', file , ' to the list')
                    pod5_files.append(file)
        return pod5_files        
    
    def __create_batch(self,  all_files, assigned_files, size=5):
        
        if size>len(all_files)-len(assigned_files):
            print("Error: batch is bigger than number of available files")
            return None
        batch = []
        for file in all_files:
            if file not in assigned_files:
                batch.append(file)
                assigned_files.append(file)
        
        #print("Batch: ", batch)    
                
        return batch
    
    def __create_tmp_input_dir(self, batchid, batch):
        '''
        This function will create a dir called tmp_ASSIGNED inside the input_dir
        with a symlink to each file assigned to this batch
        '''
        tmp_dir = "_".join(["ASSIGNED", str(batchid)])
        tmp_dir_fullpath = os.path.join(self.input_dir, tmp_dir )
        os.mkdir(tmp_dir_fullpath)
        for fl in batch:
            os.symlink(os.path.join(self.input_dir, fl), os.path.join(tmp_dir_fullpath, fl))

    def _modify_configurations_file(self, job_config_template, batchid) :
        '''
        This function needs to modify the config.json file in order
        to launch the basecalling from the batch temprary directory to a
        temporary selected output directory
        '''
        # Create path for the tmp JSON file
        config_dir = os.path.dirname(job_config_template["configFilePath"])
        tmp_config_name = f'config_{str(batchid)}.json'
        path_for_tmp_config = os.path.join(config_dir, f'tmp_config/{tmp_config_name}')

        print('path_for_tmp_config ', path_for_tmp_config)

        # Copy the template file to the new location
        shutil.copy(job_config["configFilePath"], path_for_tmp_config)

        # Modify it
        with open(path_for_tmp_config, 'r') as file:
            tmp_config = json.load(file)

        tmp_config['General']['run_name'] = f"run_{str(batchid)}"
        
        tmp_input_dir = "_".join(["ASSIGNED", str(batchid)])
        tmp_input_dir_fullpath = os.path.join(self.input_dir, tmp_input_dir )

        tmp_config['Basecalling']['input_dir'] = tmp_input_dir_fullpath

        tmp_output_dir = "_".join(["ASSIGNED", str(batchid)])
        tmp_output_dir_fullpath = os.path.join(self.input_dir, tmp_output_dir )

        tmp_config['Basecalling']['output_dir'] = tmp_output_dir_fullpath

        # Convert the modified data structure back to JSON format
        json_content = json.dumps(tmp_config, indent=2)

        # Write the modified JSON content back to the copied file
        with open(path_for_tmp_config, 'w') as file:
            file.write(json_content)

        jenkins_parameter =  {
            "configFilePath": path_for_tmp_config,
        }

        return jenkins_parameter

    def live_reading_dir(self, threshold=5, scanning_time=5):
        '''
        The purpouse of this function is to scan the input directory and trigger
        the basecalling pipeline when we have added more than "threshold" files.
        Idea: 
        1. Each 10 seconds the dir will be scanned
        2. If # of files has reached a threshold, create a tmp dir with a work 
        batch. Save what files have been assigned. For now the batch size is made
        of all the files that have been added over the threshold
        3. Keep scanning the dir and repeat
        '''
        pod5_files = []
        pod5_assigned = []
        prev_total_files = 0
        print("\033[91mI am watching\033[0m: ", self.input_dir)

        while True:
            time.sleep(scanning_time)
            pod5_files = self.__list_all_pod5_files()
            curr_total_files = len(pod5_files)
            
            number_new_file = curr_total_files-prev_total_files

            print("Current amount of files : ", curr_total_files, "\n",
                   "Previous : ", prev_total_files, "\n",
                   "Number of assigned files : ", len(pod5_assigned))

            if number_new_file >= threshold or curr_total_files-len(pod5_assigned)>=threshold :
                print("Current amount of files : ", curr_total_files, "Previous : ", prev_total_files)
                prev_total_files = curr_total_files

                print("All files: ", pod5_files)
                print("Assigned files: ", pod5_assigned, " \033[91m LENGTH: ", len(pod5_assigned), "\033[0m")

                # Update unassigned files and create a batch
                batch = self.__create_batch(pod5_files, pod5_assigned, size=number_new_file)
                batchid = str(uuid.uuid4().int)

                #print("Assigned files: ", pod5_assigned, " \033[91m LENGTH: ", len(pod5_assigned), "\033[0m")

                print("Create and launch batch ", batchid)
                self.__create_tmp_input_dir(batchid, batch)

                tmp_job_config = self._modify_configurations_file(self.job_config, batchid)
                print(tmp_job_config)
                self.Jenkins.trigger_jenkins_pipeline(self.job_name,tmp_job_config)
                
                # How can I use this on the login node ?

                # How can I exit gracefully ? What tells me that 
                # the writing has stopped ? 
                # I need to dispatch of all the remaing files




if __name__ == "__main__":
    # Authentication
    password = sys.argv[1]
    username ="tolloi"

    token = sys.argv[2]

    # Jenkins URL
    jenkins_url = "http://jenkins-sandbox.rd.areasciencepark.it:8080" 
    # Jenkins job name
    job_name = "tolloi/basecalling_pipeline"  
    # Parameters for the Jenkins pipeline. This will be used as a "template"
    # and for each run we will modify:
    # - run_name
    # - basecalling input
    # - basecalling output
    job_config = {
       "configFilePath": "/u/area/jenkins_onpexp/BC-pipelines/configurations/config_1_dgx_template.json",
       # "configFilePath": "/home/rodolfo/BC-pipelines/configurations/config_1_dgx_template.json",
    }

    # Create the Jenkins handler
    jenkins_handler = Jenkins_trigger(jenkins_url, username, password, token)
    
    reader = Live_Reading('/u/area/jenkins_onpexp/scratch/test_10G_dataset_POD5', jenkins_handler, job_name, job_config)
    reader.live_reading_dir()