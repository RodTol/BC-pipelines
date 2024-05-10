#!/bin/bash

JOB_ID=$1

# Function to check the job status
check_job_status() {
    scontrol show job $JOB_ID &> /dev/null
}

# Function to send a message to Telegram with code block formatting
send_formatted_message() {
    local message=$1
    local formatted_message="\`\`\` $message \`\`\`"

    response=$(curl -s -X POST "https://api.telegram.org/bot$BOT_TOKEN/sendMessage" \
    -d "chat_id=$CHAT_ID" \
    -d "text=$message" \
    -d "parse_mode=HTML")
    # Extract message ID from response and save it to a variable
    message_id=$(echo "$response" | jq -r '.result.message_id')    
}

# Function to send a message to Telegram with standard formatting
send_message_standard() {
    local message=$1
    response=$(curl -s -X POST "https://api.telegram.org/bot$BOT_TOKEN/sendMessage" \
    -d "chat_id=$CHAT_ID" \
    -d "text=$message" \
    -d "parse_mode=HTML")
    # Extract message ID from response and save it to a variable
    message_id=$(echo "$response" | jq -r '.result.message_id')    
}

# Function to delete a message
delete_message() {
    local message_id="$1"
    curl -s -X POST "https://api.telegram.org/bot$BOT_TOKEN/deleteMessage" \
    -d "chat_id=$CHAT_ID" \
    -d "message_id=$message_id" >/dev/null
}


BOT_TOKEN="$BC_TOKEN_BOT"
CHAT_ID="-4270864261"

count=0
send_message_standard "Job $JOB_ID is queued at $(date +"%H:%M:%S")" > /dev/null

# Loop until the job is completed
while check_job_status; do

    JOB_STATUS=$(scontrol show job $JOB_ID | awk '/JobState=/{print $1}')
    send_message_standard "At $(date +"%H:%M:%S") Slurm job $JOB_ID status is $JOB_STATUS" > /dev/null
        
    ((count++))
    if ((count >= 3)); then        
        # Capture the output of squeue -p DGX,GPU
        squeue_output=$(squeue -p DGX,GPU -o " %.9P %.8j %.8u %.2t %.10M %.6C %.6m %.10N %.10l")
        send_formatted_message "$squeue_output" > /dev/null
        count=0
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

    sleep 120
    delete_message "$message_id"
    echo "Deleted $message_id"
done