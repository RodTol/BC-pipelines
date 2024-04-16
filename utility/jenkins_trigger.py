import jenkins
from datetime import datetime
import re
import time

class Jenkins_trigger:

    def __init__(self, jenkins_url, username, password, token): 

        self.jenkins_url=jenkins_url
        self.username = username
        self.password = password
        self.token = token

        #Get the Jenkins server 
        self.server = jenkins.Jenkins(self.jenkins_url, username=self.username, password=self.password)
        user = self.server.get_whoami()
        version = self.server.get_version()
        print('Hello %s from Jenkins %s' % (user['fullName'], version))


    def _get_current_stage(self,job_name, build_number, build_status, previous_stage = None):
        while build_status not in ['SUCCESS', 'UNSTABLE', 'FAILURE', 'NOT_BUILT', 'ABORTED']  :
            console_output = self.server.get_build_console_output(job_name, build_number)
            #print(console_output)
            last_stage_line = ""
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

        self._get_current_stage(job_name, build_info['number'], build_info['result'])
