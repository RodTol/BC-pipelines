import sys
from merge_and_config import *

sys.path.append("../simulation-pipeline/utility/")
from jenkins_trigger import Jenkins_trigger
#from live_reading import telegram_send_message


if __name__ == "__main__":

    config_file_path = sys.argv[1]

    #Create a unique fastq file
    merge_fastq(config_file_path)
    #Create the configuration file for the alignment
    al_config_path = create_configurations_file(config_file_path)

    jenkins_parameter =  {
            "configFilePath": al_config_path,
    }
    print("Parameter for Jenkins pipeline: ", jenkins_parameter)

    password = "Alfredo95"
    username ="tolloi"
    token = "panda"
    jenkins_url = "http://jenkins-sandbox.rd.areasciencepark.it:8080" 
    # Jenkins job name
    job_name = "tolloi/alignment_pipeline"  
    #Launch the alignment
    jenkins = Jenkins_trigger(jenkins_url, username, password, token)
    #telegram_send_message("Launching the alignment")
    jenkins.trigger_jenkins_pipeline(job_name, jenkins_parameter)
