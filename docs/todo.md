---
layout: default
title: TODO
nav_order: 6
---

# TODO
## File to comment
1. BC software
    1. [x] BCConfiguration
    2. [x] BCController
    3. [x] BCManagement
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

## Features to implement
1. [ ] Final report construction
2. [ ] Send report to user
3. [ ] Adding modifiable number of clients for ont supervisor. Now fixed to 5
4. [x] Copying index.md to README at each push if there are changes. Using packages
5. [x] Note that the page is build correctlu but not when Github do it!!

## Errors 
1. [ ] GPU node do not see cuda:0,1. Probably it's something related to how I launch
the scripts and the env variables

## Observations
- I need launch the server, BCM and BCP on the same dir in order to have
the supervisor being able to find the connection file ?
- Let's try with each server having its own connection file in separate dir
- engine_polling_interval: Indicates after how long it will try to do a polling. It's multiplied by 60