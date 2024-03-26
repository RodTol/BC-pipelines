import sys
import jenkins
from datetime import datetime
import re
import time
import os
import uuid

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

    def __init__(self, input_dir) :
        self.input_dir = input_dir

    def __list_all_pod5_files(self) :
        all_files= os.listdir(self.input_dir)
        pod5_files = [file for file in all_files if file.endswith('.pod5')]
        return pod5_files

    def __create_tmp_input_dir(self, batchid, batch):
        '''
        This function will create a dir called tmp_ASSIGNED inside the input_dir
        with a symlink to each file assigned to this batch
        '''
        tmp_dir = "_".join(["ASSIGNED", str(batchid)])
        tmp_dir_fullpath = os.path.join(tmp_dir, self.input_dir)
        os.mkdir(tmp_dir_fullpath)
        for fl in batch:
            os.symlink(os.path.join(self.input_dir, fl), os.path.join(tmp_dir_fullpath, fl))


    def live_reading_dir(self, threshold=5, scanning_time=2):
        '''
        The purpouse of this function is to scan the input directory and trigger
        the basecalling pipeline when we have added more than "threshold" files.
        Idea: 
        1. Each 10 seconds the dir will be scanned
        2. If # of files has reached a threshold, create a tmp dir with a work 
        batch. Save what files have been assigned. For now the batch size is made of all the files
        that have been added over the threshold
        3. Keep scanning the dir and repeat
        '''
        pod5_files = []
        prev_total_files = 0

        while True:
            time.sleep(scanning_time)
            pod5_files = self.__list_all_pod5_files()
            curr_total_files = len(pod5_files)
            
            number_new_file = curr_total_files-prev_total_files

            if number_new_file >=threshold :
                print("Current amount of files : ", curr_total_files, "Previous : ", prev_total_files)
                prev_total_files = curr_total_files

                batchid = str(uuid.uuid4().int)
                print("Create and launch batch ", batchid)
                #batch = 
                #self.__create_tmp_input_dir(batchid, batch)



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
    #jenkins_handler = Jenkins_trigger(jenkins_url, username, password, token)
    #jenkins_handler.trigger_jenkins_pipeline(job_name,config_path)
    
    reader = Live_Reading('/home/rodolfo/dataset_10G_bc/test')
    reader.live_reading_dir()
