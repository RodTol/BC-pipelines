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

    if [[ "$JOB_STATUS" == "JobState=FAILED" || "$JOB_STATUS" == "JobState=CANCELLED" || "$JOB_STATUS" == "JobState=COMPLETED" ]]; then
        echo "Slurm job $JOB_ID has finished with status: $JOB_STATUS"
        break
    fi

    if ! check_job_status; then
        echo "Slurm job $JOB_ID not found. It might have been canceled or completed."
        break
    fi

    sleep 30
done