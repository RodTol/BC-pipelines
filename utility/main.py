import sys
from jenkins_trigger import Jenkins_trigger
from live_reading import Live_Reading

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
    job_config = {
       "configFilePath": "/u/area/jenkins_onpexp/BC-pipelines/configurations/config_1_dgx_template.json",
       # "configFilePath": "/home/rodolfo/BC-pipelines/configurations/config_1_dgx_template.json",
    }

    # Create the Jenkins handler
    jenkins_handler = Jenkins_trigger(jenkins_url, username, password, token)
    
    reader = Live_Reading('/u/area/jenkins_onpexp/scratch/test_10G_dataset_POD5', jenkins_handler, job_name, job_config)
    # reader = Live_Reading('/home/rodolfo/dataset_10G_bc/test', jenkins_handler, job_name, job_config)
    reader.live_reading_dir()