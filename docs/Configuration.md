---
layout: default
title: Configuration file
nav_order: 2
---
# Configuration file

## Overview
One of the main advantages of this project's architecture is its customizability. Each user can write and input its own JSON file, in order to use the selected configuration. 

## config.json structure

The JSON file has the following structures:

### 1. General
- **Overview**: Collects some general information about the run
- **Properties**
  - `run_name`: The name of the run;
  - `run_time`: The maximum run time that the script can allocate the node;
  - `version`: version of the JSON structure;

### 2. Slurm
- **Overview**: some Slurm configuration for the run
- **Properties**
  - `output`: output file for Slurm;
  - `error`: error file for Slurm;
  - `instructions`: the parametrized script that each node will execute. To have more details, see [here](BC_scripts.md) 

### 3. Basecalling
- **Overview** some basecalling settings for the run
- **Properties**
  - `model`: the basecalling model;
  - `input_dir`: the input directory. Here you'll find all the .pod5 files;
  - `output_dir`: the output directory of the whole basecalling process;
  - `logs_dir`: path for the log file produced by the dorado_server software;
  - `supervisor_script_path`: the path to the script that launches the ont_basecalling_supervisor. See [here](BC_scripts.md) for more details;

### 4. Resources
- **Overview** indicates what resource needs to be allocated for this run. Many properties in this category are lists, and it is assumed that each position in these lists corresponds to the same node
- **Properties**
  - `index_host`: an integer number that selects what node from `nodes_list` will host the BCManager;
  - `nodes_queue`: list composed by the Slurm partition for each of the nodes;
  - `nodes_list`: the list of nodes that will perform the basecalling. If no nodes are specified, let slurm decide what node to pick;
  - `nodes_ip`: list of the ip of the selected nodes (usually on network 2);
  - `nodes_cpus`: list with the value of how many cores will be allocated to each node;
  - `nodes_gpus`: list of how many GPUs will be allocated by each node. If a node does not require this parameter, it needs to be setup to "None"
  - `gpus`: Within this list, the value indicates the number of GPUs that the dorado_basecalling_server needs to utilize. Typically, this value is set to "cuda:all" to eliminate any ambiguity;
  - `batch_size_list`: a list with the maximum number of file that each node will request to the BCManager. This a crucial value to have an optimal load balance;

## Example
This run will take on 3 nodes: both dgx nodes and one available gpu node, selected by slurm

```json
{
    "General": {
      "run_name": "ExampleRun",
      "run_time": "00:20:00",
      "version": "3.0"
    },
    "Slurm": {
      "output": "/u/area/jenkins_onpexp/scratch/jenkins_logs/tmp/%x-%j.out",
      "error": "/u/area/jenkins_onpexp/scratch/jenkins_logs/tmp/%x-%j.err",
      "instructions": "/u/area/jenkins_onpexp/BC-pipelines/BC_scripts/instructions.sh "
    },
    "Basecalling": {
      "model": "dna_r10.4.1_e8.2_400bps_hac.cfg",
      "input_dir": "/u/area/jenkins_onpexp/scratch/10G_dataset_POD5",
      "output_dir": "/u/area/jenkins_onpexp/scratch/BC-pipeline_output_test/tmp",
      "logs_dir": "/u/area/jenkins_onpexp/scratch/dorado_logs",
      "supervisor_script_path" : "/u/area/jenkins_onpexp/BC-pipelines/BC_scripts/supervisor.sh"
    },
    "Resources": {
      "index_host" : "0", 
      "nodes_queue" : ["DGX", "DGX", "GPU"],
      "nodes_list" : ["dgx001", "dgx002",""],
      "nodes_ip" : ["10.128.2.161", "10.128.2.162", "10.128.2.151"],
      "nodes_cpus" : ["64", "64", "24"],
      "nodes_gpus" : ["2", "3", "None"],
      "gpus" : ["cuda:all", "cuda:all", "cuda:all"],
      "batch_size_list" : ["3", "5", "4"]
    }
  }

```