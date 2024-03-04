---
layout: default
title: BCManager
parent: BC_software
---


# BCManagement.py

## Overview

**BCManagement** is the Python script that serves as a RESTful service for managing basecalling work requests from basecalling engines. It facilitates the assignment of work, tracking of job status, and handling of completed job information. The script utilizes the Flask framework for building the RESTful API.

## Classes

### 1. `BCBatch`

- Represents a batch of pod5 files assigned for processing.
- Attributes:
  - `report_back_period`: Time interval for reporting back the status.
  - `jobid`: Unique identifier for the job.
  - `job_input_dir`: Directory containing symlinks to pod5 files for processing.
  - `job_output_dir`: Directory for storing output FASTQ files.
  - `bc_engine_id`: Identifier for the dorado server assigned to processing.
  - `batch_size`: Actual size of the batch.
  - `batch`: List of filenames in the batch.

### 2. `BCWorkloadState`

- Represents the state of basecalling processing, as well as
providing methods for operating on it. Essentially all the raw output from the Oxford Nano Pore sequencing machine consists of .POD5 files that the machine writes to a specific directory we'll
refer to as INPUT_DIR.  
Basically this raw data represents electrical current/potential over time.  
For each file, a corresponding .FASTQ file must be produced and stored in
OUTPUT_DIR.  
This is the basecalled file: a very long string of 4 letters representing the
biological bases, G A T C, that translates the raw electrical signals.  
The actual basecalling functionality is carried out by a different software/system,
i.e. the DORADO system.
This software is needed because the algorithms involved in basecalling make use of
neural networks in order to translate the electrical signals, and so are rather
specialised for the task requiring also the availability of GPUs.  
The class allows raw files to be assigned to one of the DORADO server for processing. This
will be reflected in the filesystem by the presence of the following structure:
```
INPUT_DIR
    |- ASSIGNED_{JOB-ID1}_{DORADO-SERVER-NAME}  #ASSIGNED_262817286294989972663956585584100365723_gpu004
        |- file1.pod5   (ATTENTION! IT WILL BE A SYMLINK!)
        |- file2.pod5   (ATTENTION! IT WILL BE A SYMLINK!)
        |- file3.pod5   (ATTENTION! IT WILL BE A SYMLINK!)
```
- Attributes:
  - `INPUTDIR`: Path to the directory containing raw .POD5 files.
  - `OUTPUTDIR`: Path to the directory for basecalling output.
  - `unassigned_bc`: List of pod5 files yet to be basecalled.
  - `default_batch_size`: Default size of the batch.
  - `assigned_batches`: Dictionary tracking assigned batches.

- Methods:
  - `update()`: Updates the state based on the filesystem, detecting new pod5 files and reconstructing the internal state after a crash.
  - `assign_work_to(bc_engine_id, batch_size)`: Assigns work to a specified dorado server with an optional batch size.
  - `completed_work(jobid, jobstate)`: Handles completion of processing for a given job.

### 3. `BCManager`

- Represents the RESTful service for managing basecalling work.
- Attributes:
  - `lock`: Threading lock for ensuring thread safety.
  - `tracker`: Dictionary tracking job status with last acknowledgment time, state, and report back period.
  - `bc_state`: Instance of `BCWorkloadState` representing the current workload state.
  - `app`: Flask application instance.
  - `shutdown_interval`: Interval for shutting down due to inactivity.
  - `last_activity_time`: Time of the last activity.

- Methods:
  - `get_assignwork()`: Handles GET requests to assign work to a basecalling engine.
  - `get_keepalive()`: Handles GET requests to keep a job alive.
  - `get_completed()`: Handles GET requests to retrieve completed job information.
  - `heartbeat()`: Handles GET requests to check the server's status based on the inactivity interval.
  - `update_last_activity_time()`: Updates the last_activity_time when a relevant instance method is called.

