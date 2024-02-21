#!/bin/bash

JOB_ID=$1

# Function to check the job status
check_job_status() {
    scontrol show job $JOB_ID &> /dev/null
}

# Loop until the job is completed
while check_job_status; do
    # Print the current status of the job
    JOB_STATUS=$(scontrol show job $JOB_ID | awk '/JobState=/{print $1}')
    echo "Slurm job $JOB_ID status: $JOB_STATUS"

    # If job is Finished, Cancelled or Failed, jenkins will stop waiting
    if [[ "$JOB_STATUS" == "JobState=FAILED" || "$JOB_STATUS" == "JobState=CANCELLED" || "$JOB_STATUS" == "JobState=COMPLETED" ]]; then
        echo "Slurm job $JOB_ID has finished with status: $JOB_STATUS"
        exit 0
    fi

    # If it can't find the job in queue it will raise an error
    if ! check_job_status; then
        echo "Slurm job $JOB_ID not found. It has disappeared from queue."
        exit 0
    fi

    sleep 15
done