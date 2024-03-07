---
layout: default
title: TODO
nav_order: 6
---

# TODO

<!-- ## File to comment
1. BC software
    1. [x] BCConfiguration
    2. [x] BCController
    3. [x] BCManagement
    4. [x] BCProcessor
2. scripts
    1. [x] instructions.sh
    2. [x] server.sh
    3. [x] supervisor.sh
    4. [x] wait.sh
    5. [x] configuration
3. basecalling-pipeline
   1. [x] jenkinsfile
   2. [x] telegram_bot
   3. [x] configs: you can't. Do a page only for them -->

## Doc to write
1. [x] index.md
2. [x] BC_software.md
3. [ ] BC_scripts.md
4. [x] Basecalling-pipeline.md
5. [x] Configuration.md: add example 

### Doc final structure:
1. index.md: In the index.md explains the structure and then the Installation procedure + the usage procedure  
   it's a intro 
2. config.json: first thing that needs to be explained is how to setup the json. All the options explained
   in a precise way. The user will work with this!
3. basecalling-pipeline: what will happen. From start to finish. Here I'all also the report ?
4. BC_software: the core
5. BC_scripts: the auxiliary files required for working


## Features to implement
1. [x] Final report construction
2. [x] Send report to user
3. [ ] Adding modifiable number of clients for ont supervisor. Now fixed to 5
4. [ ] **Live reading trigger from an input directory**
   

## Errors 
1. [ ] GPU node do not see cuda:0,1. Probably it's something related to how I launch
the scripts and the env variables

## Observations
- I need launch the server, BCM and BCP on the same dir in order to have
the supervisor being able to find the connection file ?
