
<p align="center">
  <img src="docs/assets/logo-area.png" alt="Area logo" width="200"/>
</p>

# BC-pipelines 🧬
This project contains some Jenkins-pipeline created to perform Basecalling on the Orfeo cluster at AreaSciencePark. This project is based on the Master degree thesis of Rodolfo Tolloi.

## Repository structure
The repository is organized in the following way:  
- [BC_software](/docs/BCsoftware/intro.md): this directory contains the "BC_software" that enables the parallelizzation across multiple nodes of the basecalling process
- [BC_scripts](/docs/BCscripts/intro.md): here you'll find some bash and python scripts. They are used by both the pipeline itself, the BC_software and also from each other.
- basecalling-pipeline: a directory with a pipeline for basecalling
- docs: a directory with all the documentation file.

## TODO
see [here](/docs/todo.md) for the roadmap of things to do

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
