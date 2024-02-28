---
layout: default
title: BC_software
nav_order: 4
---
# BC_software
This directory contains all the 

## BCManager

### BCWorkloadState:
Class that represents the state of the basecalling processing, as well as
providing methods for operating on it.  

Essentially all the raw output from the Oxford Nano Pore sequencing machine
consists of .POD5 files that the machine writes to a specific directory we'll
refer to as INPUT_DIR.  

Each raw file, is the recording of the electrical signal corresponding to the
particular DNA chunk that was sequenced. The chunks are known as frags, while the
recordings are also called squibbles because of the shape of the resulting graph.

Basically this raw data represents electrical current/potential over time.  
For each file, a corresponding .FASTQ file must be produced and stored in
OUTPUT_DIR.  

This is the basecalled file: a very long string of 4 letters representing the
biological bases, G A T C, that translates the raw electrical signals.  
The actual basecalling functionality is carried out by a different software/system,
i.e. the DORADO system. But there are also other systems such as BONITO that can be used.

This software is needed because the algorithms involved in basecalling make use of
neural networks in order to translate the electrical signals, and so are rather
specialised for the task requiring also the availability of GPUs.  

Several instances of the DORADO servers are expected to be available: at least one for each
GPU in the infrastructure. Moreover, each DORADO server is designed to work on multiple files
which it expects to be present in a specified directory.  

The class allows raw files to be assigned to one of the DORADO server for processing. This
will be reflected in the filesystem by the presence of the following structure:

INPUT_DIR
    |- JOB-ID1_DORADO-SERVER-NAME_inputdir
        |- file1.pod5   (ATTENTION! IT WILL BE A SYMLINK!)
        |- file2.pod5   (ATTENTION! IT WILL BE A SYMLINK!)
        |- file3.pod5   (ATTENTION! IT WILL BE A SYMLINK!)

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