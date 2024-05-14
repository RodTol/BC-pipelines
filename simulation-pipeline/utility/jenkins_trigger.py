import requests
from datetime import datetime
import re
import time

class Jenkins_trigger:

    def __init__(self, jenkins_url, username, password, token): 

        self.jenkins_url=jenkins_url
        self.username = username
        self.password = password
        self.token = token

        #Get the Jenkins server info

        # self.server = jenkins.Jenkins(self.jenkins_url, username=self.username, password=self.password, timeout=60)
        # user = self.server.get_whoami()
        # version = self.server.get_version()
        # print('Hello %s from Jenkins %s' % (user['fullName'], version))

        self._get_jenkins_info

    def _get_jenkins_info(self):
        # Create a session to persist the authentication cookies
        api_url = f"{self.jenkins_url}/me/api/json"
        session = requests.Session()
        session.auth = (self.username, self.password)

        try:
            # Fetch user information
            response = session.get(api_url)
            response.raise_for_status() 
            
            # Parse response JSON
            user_info = response.json()
            user_name = user_info.get('fullName', 'Unknown')
            
            # Fetch Jenkins version
            version_url = f"{self.jenkins_url}/api/json"
            response = session.get(version_url)
            response.raise_for_status()
            
            # Parse response JSON
            version_info = response.json()
            print(version_info)
            jenkins_version = version_info.get('version', 'Unknown')
            
            print('Hello %s from Jenkins %s' % (user_name, jenkins_version))
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to Jenkins: {e}")

    def _get_current_stage(self,job_name, build_number, build_status, previous_stage = None):
        while build_status not in ['SUCCESS', 'UNSTABLE', 'FAILURE', 'NOT_BUILT', 'ABORTED']  :
            try :
                console_output = self.server.get_build_console_output(job_name, build_number)
            except Exception as exc:
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),  " Reconnecting", flush=True)
                self.server = jenkins.Jenkins(self.jenkins_url, username=self.username, password=self.password, timeout=60)
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
                    print("\033[36m" + f"{timestamp} - Stage : {stage}" + "\033[0m")
                    print("\033[36m" + "Build is " + "\033[0m", build_status)
                    previous_stage = stage
                elif stage == 'Send Report to User':
                    break
            time.sleep(5)
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
        print("\033[91mBuild Number:", build_info['number'], "\033[0m")
        print("\033[91mResult:", build_info['result'], "\033[0m")
        print("\033[91mDuration (seconds):", duration_seconds, "\033[0m")
        print("\033[91mTimestamp (UTC):", timestamp_date, "\033[0m")
        print("\033[91murl", build_info['url'], "\033[0m", flush=True)

        self._get_current_stage(job_name, build_info['number'], build_info['result'])
