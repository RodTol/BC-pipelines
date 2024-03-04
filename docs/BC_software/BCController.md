---
layout: default
title: BCController
parent: BC_software
---

# BCController

## Overview

This script represents a class, called **BCController** that acts as a controller that checks if the Basecalling infrastructure is still working and, if not, shutdowns the whole process. The shutdown is performed by killing the SLURM job. To do so, it will Periodically asks for a 'heartbeat' and checks if the inactivity time is higher than a specified threshold.

- **Attributes**
    - `last_heartbeat_time`: Timestamp of the last received heartbeat.
    - `heartbeat_url`: URL for requesting the heartbeat from BCManagement.
    - `slurm_job_id`: Job ID of the SLURM job.
- **Methods**
    - `__init__(self, json_file_path, node_index)`: Initializes the BCController object by reading configuration from a JSON file and setting up initial values.
    - `return_datetime()`: A static method that returns the current datetime in a specific format.
    - `check_heartbeat(self)`: Checks the heartbeat status by sending a request to the specified URL in the settings. Returns True if the inactivity is higher than the threshold, False if it's lower, and None otherwise.
    - `monitor_heartbeat(self)`: Monitors the heartbeat continuously and starts the shutdown if the heartbeat returns a True value.
    - `cancel_slurm_job(self)`: Cancels a SLURM job using its job ID.
