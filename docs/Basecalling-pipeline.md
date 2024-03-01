---
layout: default
title: Basecalling-pipeline
nav_order: 3
---
# Basecalling-pipeline

## Overview

This Jenkins pipeline is designed for parallelizing the basecalling procedure on multiple nodes through the BC_software. Most commands are executed on the ORFEO cluster through SSH, utilizing the 'orfeo_jenkins_onpexp' credentials.

## Pipeline Structure

The pipeline consists of the following stages:

### 1. Cleanup tmp dir

- **Purpose:** Cleans up from temporary files in logs, output, input, and BC_software directories on the cluster.
- **Actions:**
  - Remove and recreate temporary directories for logs and output.
  - Cleanup input directory from previous runs.
  - Cleanup BC_software directories from the temporary directories called *server_node_(node_name)*.

### 2. Pull project repository on the Cluster

- **Purpose:** Ensures the latest version of the BC-pipelines repository is pulled on the cluster.
- **Actions:**
  - Execute 'git pull' in the BC-pipelines directory.

### 3. Generate setup based on configuration file

- **Purpose:** Uses the provided configuration file to create the sbatch file for the basecalling procedure.
- **Actions:**
  - Execute configuration.py using the provided JSON file.
  - Display the content of the generated script_resources.sh file.

### 4. Start the basecalling run

- **Purpose:** Launches the basecalling procedure on the cluster.
- **Actions:**
  - Execute the bash script with the configured parameters.
  - Capture the job ID for monitoring.

### 5. Wait for Basecalling to end

- **Purpose:** Pauses the pipeline until the basecalling job is completed.
- **Actions:**
  - Use a waiting script to monitor the completion of the basecalling job.

### 6. Create Final file

- **Purpose:** Placeholder stage for potential step to recap data about the run.
- **Actions:**
  - Display a message indicating the creation of the final file.

### 7. Send Report to User

- **Purpose:** Sends a report to the user, possibly through a messaging service.
- **Actions:**
  - Display a message indicating the report is being sent.

## Pipeline Parameters

- **configFilePath:** Path to the configuration JSON file. Default value is set to '/u/area/jenkins_onpexp/BC-pipelines/configurations/config_1_dgx.json'

## Triggers

The pipeline is triggered periodically using the 'pollSCM' trigger every hour.  

In the future, a trigger based on the live reading of a directory will be included.
