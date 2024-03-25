import requests
import sys

def trigger_jenkins_pipeline(jenkins_url, job_name, parameters, api_token):
    # Jenkins job URL
    job_url = f"{jenkins_url}/job/{job_name}/buildWithParameters?token={api_token}"

    try:
        # Send POST request to trigger the Jenkins pipeline with parameters
        response = requests.post(job_url, data=parameters)
        response.raise_for_status()
        print("Jenkins pipeline triggered successfully.")
    except requests.RequestException as e:
        print(f"Failed to trigger Jenkins pipeline: {e}")

if __name__ == "__main__":
    #Token
    api_token = sys.argv[1]  # Source directory

    # Jenkins URL
    jenkins_url = "http://jenkins-sandbox.rd.areasciencepark.it:8080"  # Replace with your Jenkins server URL

    # Jenkins job name
    job_name = "tolloi/job/basecalling_pipeline"  # Replace with your Jenkins pipeline job name

    # Parameters for the Jenkins pipeline
    config_path = {
        "configFilePath": "/u/area/jenkins_onpexp/BC-pipelines/configurations/config.json",
    }

    # Trigger the Jenkins pipeline with parameters
    trigger_jenkins_pipeline(jenkins_url, job_name, config_path, api_token)
