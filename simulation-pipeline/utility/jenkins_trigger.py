import requests
from datetime import datetime
import re
import time
from urllib.parse import urlencode
from urllib.parse import urljoin



class Jenkins_trigger:

    def __init__(self, jenkins_url, username, password, token): 

        self.jenkins_url=jenkins_url
        self.username = username
        self.password = password
        self.token = token
        self.session = requests.Session()
        self.session.auth = (self.username, self.password)

        #Get the Jenkins server info
        self._get_jenkins_info

    def _get_jenkins_info(self):
        # Create a session to persist the authentication cookies
        api_url = f"{self.jenkins_url}/me/api/json"

        try:
            # Fetch user information
            response = self.session.get(api_url)
            response.raise_for_status() 
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to Jenkins: {e}")

        # Parse response JSON
        user_info = response.json()
        user_name = user_info.get('fullName', 'Unknown')
            
        try:
            # Fetch Jenkins version
            request = requests.Request('GET', self.jenkins_url)
            request.headers['X-Jenkins'] = '0.0'
            response = self.session.send(self.session.prepare_request(request))
        except (requests.exceptions.RequestException, requests.exceptions.HTTPError):
            raise Exception("Error communicating with server[%s]" % self.url)

        # Parse response JSON
        jenkins_version = response.headers.get('X-Jenkins')
        print('Hello %s from Jenkins %s' % (user_name, jenkins_version))

    def _get_job_folder(self, name):
        '''Return the name and folder (see cloudbees plugin)
        :param name: Job name, ``str``
        :returns: Tuple [ 'folder path for Request', 'Name of job without folder path' ]
        '''
        a_path = name.split('/')
        short_name = a_path[-1]
        folder_url = (('job/' + '/job/'.join(a_path[:-1]) + '/')
                      if len(a_path) > 1 else '')

        return folder_url, short_name

    def _get_build_console_output(self, name, number):
            '''Get build console text.

            :param name: Job name, ``str``
            :param number: Build number, ``str`` (also accepts ``int``)
            :returns: Build console output,  ``str``
            '''
            # Create url to job console
            folder_url, short_name = self._get_job_folder(name)
            console_url = f'/{folder_url}job/{short_name}/{number}/consoleText'
            full_url = self.jenkins_url + console_url
            cookies = self.session.cookies.get_dict()

            try:
                response = self.session.get(full_url, cookies=cookies)
                if response:
                    return response.text
                else:
                    print(f"Error: Failed to retrieve console output. Status code: {response.status_code}")
                    print("Console url is ", full_url )
                    return
            except requests.RequestException as e:
                return f"Error: {e}"


    def _get_current_stage(self,job_name, build_number, build_status, previous_stage = None):
        while build_status not in ['SUCCESS', 'UNSTABLE', 'FAILURE', 'NOT_BUILT', 'ABORTED']  :
            # Reconnection try. Old version
            # try :
            #     console_output = self.server.get_build_console_output(job_name, build_number)
            # except Exception as exc:
            #     print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),  " Reconnecting", flush=True)
            #     self.server = jenkins.Jenkins(self.jenkins_url, username=self.username, password=self.password, timeout=60)
            #     console_output = self.server.get_build_console_output(job_name, build_number)
            #print(console_output)
            console_output = self._get_build_console_output(job_name, build_number)
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
 
    # def _build_job_url(self, name, parameters, token=False):
    #     # Construct the base build URL
    #     folder_url, short_name = self._get_job_folder(name)
    #     job_url = f"{self.jenkins_url.rstrip('/')}/job/{short_name}/buildWithParameters"
        
 
    #     params_str = "&".join([f"{key}={value}" for key, value in parameters.items()])
    #     job_url += f"?{params_str}"
        
    #     # Add token to the URL if provided
    #     if token:
    #         job_url += f"&token={token}" 
        
    #     return job_url    

    def _build_job_url(self, job_name, parameters):
        base_url = f"{self.jenkins_url}/job/{job_name}/buildWithParameters"
        params_string = '&'.join([f"{key}={value}" for key, value in parameters.items()])

        url = f"{base_url}?{params_string}&token={self.token}"

        return url


    def get_jenkins_crumb(self):
        crumb_url = f"{self.jenkins_url}/crumbIssuer/api/json"

        try:
            response = self.session.get(crumb_url)
            response.raise_for_status()
            crumb_data = response.json()
            return {crumb_data['crumbRequestField']: crumb_data['crumb']}
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to get Jenkins crumb: {e}")       

    def trigger_jenkins_pipeline(self, job_name, parameters):
        
        #Trigger the build on jenkins
        #queue_item = self.server.build_job(job_name, parameters, token=self.token)
        build_url = self._build_job_url(job_name, parameters)
        print(build_url)

        crumb_header = self.get_jenkins_crumb()

        try:
            response = self.session.post(build_url, headers=crumb_header)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return f"Build triggered successfully: {response.status_code}"
        except requests.RequestException as e:
            return f"Error triggering build: {e}"
        
        #Missing the part to retrieve the queue item
        # TRY FIRST IF THE JOB IS BEING LAUNCHED

        #Get build number and infos
        # while True:
        #     queue_info = self.server.get_queue_item(queue_item)
        #     if 'executable' in queue_info:
        #         build_info = self.server.get_build_info(job_name, queue_info['executable']['number'])
        #         break
        #     else:
        #         print("Build not started yet. Waiting...")
        #         time.sleep(5)  # Wait for 5 seconds before checking the queue again            

        # # Convert duration from milliseconds to seconds
        # duration_seconds = build_info['duration'] / 1000

        # # Convert timestamp to standard date format
        # timestamp_seconds = build_info['timestamp'] / 1000
        # timestamp_date = datetime.utcfromtimestamp(timestamp_seconds).strftime('%Y-%m-%d %H:%M:%S')

        # # Print basic information about the build
        # print("\033[91mBuild Number:", build_info['number'], "\033[0m")
        # print("\033[91mResult:", build_info['result'], "\033[0m")
        # print("\033[91mDuration (seconds):", duration_seconds, "\033[0m")
        # print("\033[91mTimestamp (UTC):", timestamp_date, "\033[0m")
        # print("\033[91murl", build_info['url'], "\033[0m", flush=True)

        # self._get_current_stage(job_name, build_info['number'], build_info['result'])
