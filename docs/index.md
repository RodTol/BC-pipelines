
<p align="center">
  <img src="docs/images/logo-area.png" alt="Area logo" width="200"/>
</p>

# BC-pipelines 🧬
This project contains some Jenkins-pipeline created to perform Basecalling on the Orfeo cluster at AreaSciencePark. This project is based on the Master degree thesis of Rodolfo Tolloi.

## Repository structure
The repository is organized in the following way:  
- BC_software
- BC_scripts
- docs
- basecalling-pipeline: prova

## TODO
see [here](/docs/todo.md) for the roadmap of things to do

## Observations
- I need launch the server, BCM and BCP on the same dir in order to have
the supervisor being able to find the connection file ?
- Let's try with each server having its own connection file in separate dir

## Mkdocs Commands

* `mkdocs new [dir-name]` - Create a new project.
* `mkdocs serve` - Start the live-reloading docs server.
* `mkdocs build` - Build the documentation site.
* `mkdocs -h` - Print help message and exit.
