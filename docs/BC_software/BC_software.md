---
layout: default
title: BC_software
nav_order: 4
has_children: true
---
# BC_software

## Overview
The core of the infrastructure is the BC_software, which enables the parallelizzation across multiple nodes of the basecalling computation. This is achieved through a client-server setup, where the [BC_Manager](https://github.com/RodTol/BC-pipelines/blob/master/BC_software/BCManagement.py) acts as the server and the [BC_Processor](https://github.com/RodTol/BC-pipelines/blob/master/BC_software/BCProcessors.py) as the client. The whole infrastructure is built upon the dorado_basecaller_server.  
The image below illustrates the fundamental concept underlying this software:
<figure>
    <img src="../assets/Tirocinio - Network security diagram example(3).png"
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





