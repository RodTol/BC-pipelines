import time
import os
import uuid
import json
from datetime import datetime
import sys
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


class Live_Reading :

    def __init__(self, input_dir, Jenkins_handler, Jenkins_job_name, Jenkins_job_config) :
        self.input_dir = input_dir
        self.Jenkins = Jenkins_handler
        self.job_name = Jenkins_job_name 
        self.job_config = Jenkins_job_config

    def _list_all_pod5_files(self) :
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
                    print(f'Appended file {file} at ', datetime.now().strftime("%H:%M:%S"))
        return pod5_files        
    
    def _create_batch(self,  all_files, assigned_files, size=5):
        
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
    
    def _create_tmp_input_dir(self, batchid, batch):
        '''
        This function will create a dir called tmp_BATCH inside the input_dir
        with a symlink to each file assigned to this batch
        '''
        tmp_dir = "_".join(["BATCH", str(batchid)])
        tmp_dir_fullpath = os.path.join(self.input_dir, tmp_dir )
        os.mkdir(tmp_dir_fullpath)
        for fl in batch:
            os.symlink(os.path.join(self.input_dir, fl), os.path.join(tmp_dir_fullpath, fl))

    def _create_tmp_output_dir(self, base_output_dir, batchid):
        tmp_output_dir = "_".join(["BATCH", str(batchid)])
        tmp_output_dir_fullpath = os.path.join(base_output_dir, tmp_output_dir )

        # Create 'pass' directory
        pass_dir = os.path.join(tmp_output_dir_fullpath, 'pass')
        os.makedirs(pass_dir, exist_ok=True)

        # Create 'fail' directory
        fail_dir = os.path.join(tmp_output_dir_fullpath, 'fail')
        os.makedirs(fail_dir, exist_ok=True)

        return tmp_output_dir_fullpath
    
    def _modify_configurations_file(self, job_config_template, batchid) :
        '''
        This function needs to modify the config.json file in order
        to launch the basecalling from the batch temprary directory to a
        temporary selected output directory
        '''

        # Get the output directory from template config
        with open(job_config_template["configFilePath"], 'r') as file:
            template_config = json.load(file)
        template_output_dir = template_config['Basecalling']['output_dir']
        template_logs_dir = template_config['Basecalling']['logs_dir']

        # Create path for the tmp JSON file
        config_dir = os.path.dirname(job_config_template["configFilePath"])
        tmp_config_name = f'config_{str(batchid)}.json'
        path_for_tmp_config = os.path.join(config_dir, f'tmp_config/{tmp_config_name}')

        #print('path_for_tmp_config ', path_for_tmp_config)

        # Copy the template file to the new location
        shutil.copy(job_config_template["configFilePath"], path_for_tmp_config)

        # Modify it
        with open(path_for_tmp_config, 'r') as file:
            tmp_config = json.load(file)

        tmp_config['General']['run_name'] = f"run_{str(batchid)}"
        
        tmp_input_dir = "_".join(["BATCH", str(batchid)])
        tmp_input_dir_fullpath = os.path.join(self.input_dir, tmp_input_dir )
        tmp_config['Basecalling']['input_dir'] = tmp_input_dir_fullpath

        tmp_output_dir_fullpath = self._create_tmp_output_dir(template_output_dir, batchid)
        tmp_config['Basecalling']['output_dir'] = tmp_output_dir_fullpath

        # Basecalling log dir
        tmp_logs_dir = "_".join(["BATCH", str(batchid)])
        tmp_logs_dir_fullpath = os.path.join(template_logs_dir, tmp_logs_dir)
        tmp_config['Basecalling']['logs_dir'] = tmp_logs_dir_fullpath

        # Slurm log dir
        os.makedirs(tmp_logs_dir_fullpath, exist_ok=True)
        tmp_config['Slurm']['output'] = os.path.join(tmp_logs_dir_fullpath, "%x-%j.out")
        tmp_config['Slurm']['error'] = os.path.join(tmp_logs_dir_fullpath, "%x-%j.err")

        # Convert the modified data structure back to JSON format
        json_content = json.dumps(tmp_config, indent=2)

        # Write the modified JSON content back to the copied file
        with open(path_for_tmp_config, 'w') as file:
            file.write(json_content)

        jenkins_parameter =  {
            "configFilePath": path_for_tmp_config,
        }

        return jenkins_parameter

    def live_reading_dir(self, threshold=5, scanning_time=5, max_retry=5):
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
        counter = 0
        print("\033[91mI am watching\033[0m: ", self.input_dir)

        while True:
            time.sleep(scanning_time)
            pod5_files = self._list_all_pod5_files()
            curr_total_files = len(pod5_files)
            
            number_new_file = curr_total_files-prev_total_files

            print("\033[32m" + "Current amount of files : " + "\033[0m", curr_total_files, "\n",
                "\033[32m" + "Previous : " + "\033[0m", prev_total_files, "\n",
                "\033[32m" + "Number of assigned files : " + "\033[0m", len(pod5_assigned), flush=True)

            if number_new_file >= threshold or curr_total_files-len(pod5_assigned)>=threshold :
                print("Current amount of files : ", curr_total_files, "Previous : ", prev_total_files)
                prev_total_files = curr_total_files

                print("All files: ", pod5_files)
                print("Assigned files: ", pod5_assigned, " \033[91m LENGTH: ", len(pod5_assigned), "\033[0m")

                # Update unassigned files and create a batch
                batch = self._create_batch(pod5_files, pod5_assigned, size=number_new_file)
                batchid = str(uuid.uuid4().int)

                #print("Assigned files: ", pod5_assigned, " \033[91m LENGTH: ", len(pod5_assigned), "\033[0m")

                print("Create and launch batch ", batchid, flush=True)
                self._create_tmp_input_dir(batchid, batch)

                tmp_job_config = self._modify_configurations_file(self.job_config, batchid)
                print(tmp_job_config)
                # Launch the Jenkins pipeline
                self.Jenkins.trigger_jenkins_pipeline(self.job_name,tmp_job_config)
                counter = 0
            if number_new_file==0:
                # How can I exit gracefully ? What tells me that the writing has stopped ? 
                # I need to dispatch of all the remaing files
                # This is a temporary solution that if the directory does not change for 
                # 5 times, will shutdown
                counter = counter +1
                print (f"This is the {counter} time the directory is the same", flush=True)
                if counter == max_retry:
                    print("\033[31m" + f"For {max_retry} times the directory wasn't updated" + "\033[0m")
                    print("\033[31m" + "Exiting gracefully..." + "\033[0m")
                    
                    return #no sys.exit(0) otherwise I will not perform the final processing





