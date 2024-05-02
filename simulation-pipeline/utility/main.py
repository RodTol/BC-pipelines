import sys
from jenkins_trigger import Jenkins_trigger
from live_reading import Live_Reading
from final_processing import Final_processing
import os
from merge_and_QC import merge_files

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

   # Put togheter the outputs
   final_processing = Final_processing(job_config["configFilePath"])
   final_processing.put_togheter_outputs()
   
   # Merge and QC
   pass_total_dir = final_processing.total_pass_dir
   pass_total_file = os.path.join(final_processing.total_output_dir, "total_pass_reads.fastq")

   merge_files(pass_total_dir, pass_total_file)

   fail_total_dir = final_processing.total_fail_dir
   fail_total_file = os.path.join(final_processing.total_output_dir, "total_fail_reads.fastq")

   merge_files(fail_total_dir, fail_total_file)


