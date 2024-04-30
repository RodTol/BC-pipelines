import sys
from jenkins_trigger import Jenkins_trigger
from live_reading import Live_Reading
from final_processing import Final_processing
import json

if __name__ == "__main__":
   # Authentication
   password = sys.argv[1]
   username ="tolloi"

   token = sys.argv[2]

   # Jenkins URL
   jenkins_url = "http://jenkins-sandbox.rd.areasciencepark.it:8080" 
   # Jenkins job name
   job_name = "tolloi/basecalling_pipeline"  

   # Parameters for the Jenkins pipeline. This config will be used as a "template"
   # and for each run we will modify:
   # - run_name
   # - basecalling input
   # - basecalling output
   # - logs dir
   job_config = {
      "configFilePath": sys.argv[3],
      # "configFilePath": "/home/rodolfo/BC-pipelines/configurations/config_1_dgx_template.json",
   }
   
   # Create the Jenkins handler
   jenkins_handler = Jenkins_trigger(jenkins_url, username, password, token)
   
   reader = Live_Reading(sys.argv[4], jenkins_handler, job_name, job_config)
   reader.live_reading_dir()

   final_processing = Final_processing(job_config["configFilePath"])
   final_processing.put_togheter_outputs()
