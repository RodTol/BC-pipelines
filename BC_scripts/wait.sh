#!/bin/bash

JOB_ID=$1

# Function to check the job status
check_job_status() {
    scontrol show job $JOB_ID &> /dev/null
}

# Function to send a message to Telegram
send_message() {
 local message="$1"
 local formatted_message="```\n $message \n```"
 curl -s -X POST "https://api.telegram.org/bot$BOT_TOKEN/sendMessage" \
 -d "chat_id=$CHAT_ID" \
 -d "text=$message"
}

BOT_TOKEN="$BC_TOKEN_BOT"
CHAT_ID="-4074077922"

# Set initial time and interval
start_time=$(date +%s)
interval=300 

send_message "Job $JOB_ID is queued at $(date +"%H:%M:%S")"

# Loop until the job is completed
while check_job_status; do

    # Print the current status of the job every interval
    current_time=$(date +%s)
    elapsed_time=$((current_time - start_time))

    if ((elapsed_time >= interval)); then
        JOB_STATUS=$(scontrol show job $JOB_ID | awk '/JobState=/{print $1}')
        echo "Slurm job $JOB_ID status: $JOB_STATUS"
        send_message "At $(date +"%H:%M:%S") Slurm job $JOB_ID status is $JOB_STATUS"
        
        # Capture the output of squeue -p DGX,GPU
        squeue_output=$(squeue -p DGX,GPU)

        # Send the captured output as a message
        send_message "$squeue_output"

        # Reset the start time
        start_time=$current_time
    fi

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