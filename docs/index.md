---
title: Home
layout: home
---

<p align="center">
  <img src="assets/area_for_white_bkg.png" alt="Area logo" width="200"/>
</p>

# BC-pipelines 🧬
This project contains some Jenkins-pipeline created to perform Basecalling on the Orfeo cluster at AreaSciencePark. This project is based on the Master degree thesis of Rodolfo Tolloi.

## Repository structure
The repository is organized in the following way:  
- [BC_software](BC_software.md): this directory contains the "BC_software" that enables the parallelizzation across multiple nodes of the basecalling process
- [BC_scripts](BC_scripts.md): here you'll find some bash and python scripts. They are used by both the pipeline itself, the BC_software and also from each other.
- basecalling-pipeline: a directory with a pipeline for basecalling
- docs: a directory with all the documentation file.

## TODO
### File to comment
1. BC software
    1. [x] BCConfiguration
    2. [x] BCController
    3. [ ] BCManagement
    4. [ ] BCProcessor
2. scripts
    1. [x] instructions.sh
    2. [x] server.sh
    3. [x] supervisor.sh
    4. [x] wait.sh
    5. [x] configuration
3. basecalling-pipeline
   1. [x] jenkinsfile
   2. [x] telegram_bot
   3. [x] configs: you can't. Do a page only for them

### Features to implement
1. [ ] Final report construction
2. [ ] Send report to user
3. [ ] Adding modifiable number of clients for ont supervisor. Now fixed to 5
4. [x] Copying index.md to README at each push if there are changes. Using packages
5. [ ] Note that the page is build correctlu but not when Github do it!!

### Errors 
1. [ ] GPU node do not see cuda:0,1. Probably it's something related to how I launch
the scripts and the env variables

## Observations
- I need launch the server, BCM and BCP on the same dir in order to have
the supervisor being able to find the connection file ?
- Let's try with each server having its own connection file in separate dir
- engine_polling_interval: Indicates after how long it will try to do a polling. It's multiplied by 60

## Mkdocs Commands

* `mkdocs new [dir-name]` - Create a new project.
* `mkdocs serve` - Start the live-reloading docs server.
* `mkdocs build` - Build the documentation site.
* `mkdocs -h` - Print help message and exit.
