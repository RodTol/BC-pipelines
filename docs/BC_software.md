---
layout: default
title: BC_software
nav_order: 4
---
# BC_software

## Overview
The core of the infrastructure is the BC_software, which enables the parallelizzation across multiple nodes of the basecalling computation. This is achieved through a client-server setup, where the [BC_Manager](https://github.com/RodTol/BC-pipelines/blob/master/BC_software/BCManagement.py) acts as the server and the [BC_Processor](https://github.com/RodTol/BC-pipelines/blob/master/BC_software/BCProcessors.py) as the client. The whole infrastructure is built upon the dorado_basecaller_server.  
The image below illustrates the fundamental concept underlying this software:
<figure>
    <img src="assets/Tirocinio - Network security diagram example(3).png"
         alt="diagram_BC"
         width="800">
</figure>  

In order to work correctly, the software use the following [packages](https://github.com/RodTol/BC-pipelines/blob/master/BC_software/requirements.txt)

## How it works:
- All the nodes need to have an instance of the dorado_basecaller_server up and running
- One node will start the BCManager.py
- All the nodes involved will then start the BCProcessor, which will ask to the BCManager for a batch of work. The maximum size of this batch is definied inside the config.json file.
    - Every time a batch is assigned, the BCProcessor will launch a [supervisor.sh](https://github.com/RodTol/BC-pipelines/blob/master/BC_scripts/supervisor.sh) script, that will launch the dorado_basecaller_supervisor
    - The dorado suite will perform the actual basecalling
    - Each BCProcessor, after the batch is finished, will ask for a new one, until work is available.
- If there are no file to process, the BCProcessor will shutdown
- The BCManager shutdown is managed by the BCController. This 3rd actor will monitor for any activity of the BCManager and, after a certain threshold of inactivity, will kill the Slurm job, ending the basecalling. 


## BCConfiguration.py
The purpouse of this file is to collect all the settings about the basecalling. It has only one class with a creator that reads a provided .json file.

## BCManagement.py

**BCManagement** is the Python script that serves as a RESTful service for managing basecalling work requests from basecalling engines. It facilitates the assignment of work, tracking of job status, and handling of completed job information. The script utilizes the Flask framework for building the RESTful API.

### Classes

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
    |- {JOB-ID1}_{DORADO-SERVER-NAME}_inputdir # 
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


## BCController
Class that encapsulates a thread where the BCEngine constantly informs the BCManager on the state
of the ongoing processing.  

It implements a resiliance protocol, thereby signalling to initiate a SHUTDOWN should the communication with the BC Controller encounter any problem: a crash, a network interruption, a malfunctioning.  

Likewise the BC Controller is aware of this protocol, so it knows we'll shutdown as soon as possible and eventually be restarted with a cleared internal state.  

In general, the Single Writer principle is followed: volatile variables are used where there is by design a single Thread expected to write/change a variable, while any number of threads can read that variable.  

In Python this is not needed, but it's important to spell it out in order to clarify the design and intended way of usage (indeed there is no 'volatile' in python).  

Essentially, the main thread where basecalling is happening, should get an instance and start the keepalive; then it should periodically check whether there are problems with the bc controller and so terminate; or upon completion of processing, it should communicate back the result and terminate the keepalive thread.  

Convenience methods have been provided, so they can be invoked on a BCKeepAlive instance; however it is possible also to check/interact directly with the internal 'volatile' variables: provided the resiliance protocol logic is implemented i.e. decide when to shutdown.  

### BCEngine.begin_working
However, after a batch has been processed, if the processing time took longer than the polling
interval, then only 30 secs will be waited for before a new request is made. This is to allow
for sustained processing throughput, while at the same time not heavily loading the server with
useless requests when there is nothing to process.


#### NOTES:
what if the keepalive arrived late?  
missing entry?  
active deleting thread?  
multiple requests for same jobid?  
try:  
MAKE A DEFENSIVE COPY OF THE WHOLE ENTRY: we have a deleting thread in the background that operates on it!  

AS PER BEST PRACTICE, EACH THREAD NEVER WORKS DIRECTLY IN THE ENTRY, BUT MAKES FIRST A DEFENSIVE COPY AND THEN MODIFIES IT, BEFORE ASSIGNING IT BACK TO THE DICTIONARY. SO THE COPY IS SAFE AS NO DATA CHANGES.  

THIS ONLY GUARANTEES THE LOGICAL CONSISTENCY OF ANY DECISION/OPERATION MADE ON THE RETRIEVED DATA, WHICH IS GUARANTEED FREE OF INTERLEAVING OF "PARTIAL CHUNKS" AS THE OTHER THREAD OPERATES ON THE DATA.  

IT DOES _NOT_ GUARANTEE ABSENCE OF RACE CONDITION / STALE READS! FOR THAT YOU STILL NEED SYNCHRONIZATION OF SOME SORT.    

INDEED, THE RELEVANT SCENARIO IS WHEN WE GET A REFERENCE TO THE ENTRY, WHICH GETS REPLACED IMMEDIATELY AFTER WE OBTAIN IT. WE'LL THEN GO ON TO MAKE A LOGICALLY CONSISTENT DECISION BASED ON THE DATA IN THE ENTRY, WHICH IS NOW CLEARLY STALE/OLD.  
IN GENERAL WHETHER WE CAN TOLERATE OPERATION ON STALE DATA, OR WHETHER WE REALLY NEED TO FORCE THE OTHER THREAD TO WAIT FOR US TO COMPLETE, WILL DEPEND ON THE ACTUAL PROBLEM DOMAIN. 
```python
# entry = self.tracker[req_job_id].copy()
last_time = entry[0]
report_back_period = entry[2]
right_now = time.time()

if right_now <= last_time + report_back_period:
    # OK: keep alive arrived before expiry
    entry[0] = right_now
    entry[1] = req_job_state
    # entry[2] stays the same
    self.tracker[req_job_id] = entry
    return json.dumps({"late": False})
else:
    # BAD: keepalive arrived late
    print("WARNING! NOT IMPLEMENTED YET! keepalive arrived too late: client should shutdown, and work be re-assigned!")
    # remove from tracking ?
    # clear state so old work can be reassigned?
    # tell client it was late?
    # interaction with deleting thread and other threads?
    return json.dumps({"late": True})

except KeyError:
    # ENTRY DOES NOT EXIST! EITHER IT WAS DELETED BY THE DELETING THREAD BECAUSE IT WAS EXPIRED, OR IT NEVER EXISTED.
    # INFORM CLIENT! AS PER PROTOCOL, IT SHOULD STOP PROCESSING AND INITIATE A SHUTDOWN.
    print("WARNING! NOT IMPLEMENTED YET! keepalive arrived for non-existent jobid!")
    # tell client?
    return json.dumps({"late": True})
```


