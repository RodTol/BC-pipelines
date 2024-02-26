# TODO
## File to comment
1. BC software
    1. [ ] BCConfiguration
    2. [ ] BCController
    3. [ ] BCManagement
    4. [ ] BCProcessor
2. scripts
    1. [x] instructions.sh
    2. [x] server.sh
    3. [x] supervisor.sh
    4. [x] wait.sh
3. basecalling-pipeline
   1. [x] jenkinsfile
   2. [x] configuration
   3. [x] telegram_bot
   4. [x] configs: you can't. Do a page only for them

## Features to implement
1. [ ] Final report construction
2. [ ] Send report to user
3. [ ] Adding modifiable number of clients for ont supervisor. Now fixed to 5
4. [x] Copying index.md to README at each push if there are changes. Using packages

## Errors 
1. [ ] GPU node do not see cuda:0,1. Probably it's something related to how I launch
the scripts and the env variables