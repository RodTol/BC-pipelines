---
layout: default
title: Home
nav_order: 1
---

<p align="center">
  <img src="assets/area_for_white_bkg.png" alt="Area logo" width="200"/>
</p>

# BC-pipelines 🧬 
This project contains some Jenkins-pipeline created to perform Basecalling on the Orfeo cluster at AreaSciencePark. This project is based on the Master degree thesis of Rodolfo Tolloi. To se a full documentation about this software and how to use it, click [here](https://rodtol.github.io/BC-pipelines/)

## Requirements:
The file in this project are thought to be run on [Orfeo](https://orfeo-doc.areasciencepark.it/), so they are not fully generalized for any system, and if a user wish to run on its custom platform it will require to adapt different files.  
Given this premise, the basic requirements are:
- **Python3** : installed on every node. [Here](/BC_software/requirements.txt) you can find a list of the packages used by the software.
- **Dorado**: the dorado_server and the ont_basecaller_supervisor are the two componets that actually performs the basecalling. You can find the standlone dorado basecaller software [here](https://github.com/nanoporetech/dorado), but the server version and the ont_basecaller_supervisor are accesible only to "full" members of the ONT community.
- **Jenkins**: the pipeline is designed to be runned with Jenkins. Of course, the Jenkins agent needs to be able to connect to the cluster, but, that said, only very basic plugins were used.

## How to use it: 
1. The user needs to setup Jenkins, using the jenksinfile provided in this directory as definition of the pipeline
2. ⚠️ The directory needs to be cloned on the cluster, since inside the pipeline there's a step to pull the latest version of the directory.
3. Write your own config.json file
4. The pipeline is parametrized with the path to the configuration file, so the user can point to its personal config.json
5. VIRTUALENV

## Repository structure 
The repository is organized in the following way:  
- [basecalling-pipeline](Basecalling-pipeline.md): a directory with the jenkinsfile that defines the pipeline for basecalling.
- [configurations](Configuration.md): the directory containing the JSON file with all the settings for a run.
- [BC_software](BC_software.md): this directory contains the "BC_software" that enables the parallelizzation across multiple nodes of the basecalling process.
- [BC_scripts](BC_scripts.md): here you'll find some bash and python scripts. They are used by both the pipeline itself and the BC_software to setup and launch the whole basecalling process.


## TODO
See [here](todo.md).

