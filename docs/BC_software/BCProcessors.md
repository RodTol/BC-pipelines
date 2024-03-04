---
layout: default
title: BCProcessor
parent: BC_software
---
# BCProcessor

## Overview
**BCProcessor** contains 2 classes: the BCEngine and the BCKeepAlive. The first one represents a Basecalling Engine sitting in a physical node where GPUs are available; it will periodically connects back to BCManager to request work for processing and then, invoke a dorado to carry out the basecalling.  
The second one encapsulates a thread where the BCEngine constantly informs the BCManager about the state of ongoing processing. It implements a resilience protocol to handle communication problems with the BC Controller and should be used by the main thread where basecalling is happening.


### BCEngine
- **Attributes**
  - `conf`: Configuration data obtained by reading the JSON file.
  - `optimal_request_size`: Ideal number of pod5 files to process per request.
  - `engine_id`: Unique ID of the engine.
  - `polling_interval`: Minimum time in minutes between successive requests.
  - `INPUTDIR`: ROOT of the input directory where pod5 files are stored.
  - `OUTPUTDIR`: Path to the directory where the basecalling should direct its output for this job.
  - `bc_script`: Local script to execute for BC processing.
  - `bc_model`: Basecalling model (e.g., dna_r10.4.1_e8.2_400bps_hac.cfg).
  - `PROCESSING_STATE`: Internal state of processing.
  - `api_url`: URL for the request work route to the BCManager.
  - `shutdown`: Boolean option for stopping asking batches of work to the BCManager.
  - `work_until_none_left`: Boolean option for working until none is left.
- **Methods**
  - `__init__(self, json_file_path, node_index)`: Initializes the BCEngine object with configuration settings loaded from a JSON file.
  - `begin_working(self)`: Starts continuous periodic polling for new batches of pod5 files to process. Polling occurs every polling_interval minutes. If there are any issues communicating with the BC Controller, the loop will be interrupted, and the client will shut down.
  - `_request_a_batch(self, api_url, engine_id, optimal_request_size)`: Requests a batch for processing from the BC Controller using the provided API URL, engine ID, and optimal request size. In case of any error with the BC Controller, this client will shut down.
  -  `_basecalling_work(self, input_dir, output_dir, model)`: Handles the basecall processing by invoking an external script that interacts with dorado_server. Updates the internal variable `self.PROCESSING_STATE` based on the output of the external script. If an exception is raised, `self.PROCESSING_STATE` is set to `FAILED` and `self.shutdown` is set to `True` for a clean shutdown.
  - `_sleep_before_next_batch(self, start_time, end_time)`: Sleeps for a specific duration before requesting a new batch for processing. If the processing time exceeds the polling interval, it sleeps for 30 seconds; otherwise, it waits for the polling interval duration.

### BCKeepAlive
- **Attributes**
  - `report_back_interval`: Seconds between successive keep-alive messages.
  - `job_id`: The ID of the batch being processed.
  - `starting_state`: The current starting processing state.
  - `final_state`: Volatile variable to indicate the final state reached by the processing main thread.
  - `keep_alive_url`: URL for the `/keepalive` route (depends on what node is hosting the BCManager).
  - `keep_alive_terminate_url`: URL for the `/completed` route (depends on what node is hosting the BCManager).
  - `BCManager_PB`: Volatile variable to indicate to the main thread it should stop and shutdown.
- **Methods**
  - `__init__(self, report_back_interval, job_id, starting_state, conf)`: Initializes a KeepAliveManager object with the specified parameters.
  - `run(self)`: Starts a loop periodically calling back the BCManager to inform it of the ongoing processing. Once the final state is reached, regardless of success or failure, the BCManager is informed, the keep-alive is stopped, and the loop exits.
  - `shutdown_if_broken_keepalive(self)`: Checks for a spotted problematic BC Controller: it crashed, the network is down, an exception on the server is returned back. Initiates a client shutdown as per protocol, should the BCManager be problematic.
  - `terminate_keepalive(self, final_state)`: Tells the keep_alive_thread that processing is complete. Blocks until that thread ends. Invoked from the main thread where the processing is taking place.
  - `started_instance(cls, answer, starting_state, conf)` Class method that initializes an instance of BCKeepAlive and starts an internal keep-alive thread. Returns an instance of BCKeepAlive with a running keep-alive thread connected to the BC Controller.

