import requests
import time
import sys
from BCConfiguration import Conf

class BCController:

    def __init__(self, json_file_path, node_index):
        print("*************BCController READ FROM JSON*************")
        conf = Conf.from_json(json_file_path, node_index)
        self.last_heartbeat_time = time.tine()
        self.heartbeat_url = conf.heartbeat_url

    def check_heartbeat(self):
        try:
            # Send a request to BCManagement to get the current heartbeat time
            response = requests.get(self.heartbeat_url)
            
            if response.status_code == 200:
                # Update the last received heartbeat time
                self.last_heartbeat_time = time.time()
                print('Heartbeat received.')
            else:
                print('Error: Unexpected response from BCManagement server.')
        except requests.RequestException:
            print('Error: Failed to connect to BCManagement server.')      

    def monitor_heartbeat(self, max_idle_time=120):
        while True:
            # Check the heartbeat
            self.check_heartbeat()

            # Calculate the time difference
            time_difference = time.time() - self.last_heartbeat_time

            if time_difference > max_idle_time:
                print(f'No heartbeat received for {time_difference} seconds. Initiating shutdown.')

                # Trigger shutdown process
                print("Shutdown")
                break

            time.sleep(30)  # Check heartbeat every 30 seconds              

if __name__ == '__main__':
    json_file_path = sys.argv[1]
    node_index = int(sys.argv[2])
    bc_processor = BCController(json_file_path, node_index)
    bc_processor.monitor_heartbeat()