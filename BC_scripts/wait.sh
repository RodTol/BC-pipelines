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

    sleep 60
done

echo "Slurm job $JOB_ID has finished."
