1. [Introduction](#introduction)
2. [Downloads](#downloads)
3. [Quick Start](#quick-start)
4. [Features, settings and analysis](#features-settings-and-analysis)
5. [Bioinformatics toolkit](#bioinformatics-toolkit)
6. [FAQ and Troubleshooting](#faq-and-troubleshooting)

# Introduction

## Dorado Basecall Server software overview

**IMPORTANT**

### Dorado Basecall Server license

Dorado Basecall Server is available under the Oxford Nanopore Technologies [Terms and Conditions](https://community.nanoporetech.com/posts/terms).

### Dorado Basecall Server software

Dorado Basecall Server is a data processing toolkit that contains the Oxford Nanopore Technologies' production basecalling algorithms and several bioinformatic post-processing features. It is a wrapper around the [dorado basecaller](https://github.com/nanoporetech/dorado), which is designed to provide basecalling as a service. It can be run from the command line in Windows, Mac OS (Intel and M1/M2), and on multiple Linux platforms. Dorado Basecall Server is also integrated with our sequencing instrument software, MinKNOW, and basecalling features are available via the MinKNOW UI. A selection of configuration files allows basecalling of DNA and RNA libraries made with Oxford Nanopore Technologies’ current sequencing kits, in a range of flow cells.

The Dorado Basecall Server software contains many configurable parameters that can be used to specify exactly how the data analysis is performed. Adjusting some of these parameters requires a deep knowledge of nanopore data, and as such, using Dorado Basecall Server at the command line is aimed at more advanced users. For those who are new to sequencing or have limited knowledge of sequencing data analysis, we recommend using the options presented in the MinKNOW software UI for basecalling.

For more information about Oxford Nanopore Technologies’ basecalling algorithms, see the [Data Analysis technical document](https://community.nanoporetech.com/docs/sequence/sequencing_software/data-analysis/).

### General system requirements for Dorado Basecall Server

These system requirements are guidelines - the actual amount of memory and disk space required to run Dorado Basecall Server tools will heavily depend on options and input data.

-   4 GB RAM plus 1 GB per thread for basecalling (more RAM may be required for duplex basecalling)
-   Administrator access for .deb or .msi installers
-   ~2 GB of drive space for installation required. We recommend a minimum of 512 GB storage space for basecalled read files.

### CPU and GPU basecalling with Dorado Basecall Server

Oxford Nanopore Technologies provides executables that can be run on Central Processing Units (CPUs) on Windows, Mac OS and Linux, M1/2 GPUs, or on Graphics Processing Units (GPUs) on Windows and certain Linux platforms:

-   **Windows:** ont-dorado-server archive installer (supports both CPU and GPU)
-   **macOS (Intel):** ont-dorado-server archive installer (CPU only)
-   **macOS (M1/M2):** ont-dorado-server archive installer (CPU and Metal-accelerated GPU)
-   **Linux (x64):**
    -   ont-dorado-server .deb for Ubuntu 18.04, 20.04, 22.04
    -   ont-dorado-server .tar.gz – general Linux archives with pre-built binaries (compatible with most Linux versions, including CentOS 7/8)
-   **Linux (ARM):**
    -   ont-dorado-server .deb for Ubuntu 18.04
    -   ont-dorado-server .tar.gz – general Linux archives with pre-built binaries (these archives are CUDA 10 versions for use with Linux 4 Tegra running Ubuntu 18).

GPU basecalling requires NVIDIA drivers which support a minimum CUDA version of:

- CUDA 10 for Linux 4 Tegra running Ubuntu 18.
- CUDA 11.8 for Linux x86 systems.
- CUDA 11.8 for Windows systems.

In general it is recommended to install the latest GPU drivers available for your system and graphics card. See the [NVIDIA driver download page](https://www.nvidia.co.uk/Download/index.aspx) for details.

Using external GPUs can dramatically increase basecalling speed. Dorado works with only NVIDIA GPUs, and has been tested using the following specific models:

-   NVIDIA A100 40GB
-   NVIDIA A100 80GB
-   NVIDIA Tesla V100
-   NVIDIA Quadro GV100
-   NVIDIA Jetson TX2
-   NVIDIA Jetson Xavier

If working with a different model of NVIDIA GPU than those listed above, the Dorado software requires CUDA Compute Capability >=6.1 (for more information about CUDA-enabled GPUs, see the [NVIDIA website](https://developer.nvidia.com/cuda-gpus))

It is possible to use other NVIDIA GPUs for basecalling, however Oxford Nanopore Technologies develops and tests software on the models stated above, so support for other models is limited.

### Fast vs High Accuracy vs Super-Accurate models

The Dorado basecaller offers three different CRF models: a Fast model, a High accuracy (HAC) model, and a Super accurate (sup) model. The Fast model is designed to keep up with data generation on Oxford Nanopore devices (MinION Mk1C, GridION, PromethION). The HAC model provides a higher raw read accuracy than the Fast model and is more computationally-intensive. The Super accurate model has an even higher raw read accuracy, and is even more intensive than the HAC model.

For more information about basecalling accuracy, please consult the [Accuracy page on the Oxford Nanopore website](https://nanoporetech.com/accuracy)

A comparison of the speed of the three models is provided in the table below.

*Please note that these numbers represent the theoretical best speeds achievable with the basecallers, and a real sequencing experiment may be basecalled more slowly.*

![.](img/2021-05_Guppy_speed_benchmarking.png)

# Downloads

The installers for each platform can be found on the [Software Downloads](https://community.nanoporetech.com/downloads) page of the Community.

## Installing Dorado Basecall Server on Windows

### Supported platforms for Dorado Basecall Server:

Operating system:
-   64-bit Windows 10

GPU devices:
-   A supported NVIDIA GPU in order to perform GPU basecalling

### Install instructions:
1.  Download the .tar.gz installer for Dorado Basecall Server:
2.  Extract the archive using a program which supports .tar.gz files, such as [7-Zip](https://www.7-zip.org/), to the desired location.
3.  (Optional) Add the install location's <path>/bin subfolder to the system path, so executables can be called from any working folder.

## Installing Dorado Basecall Server on Linux

### Supported platforms for Dorado Basecall Server:

Operating system:
-   Most 64-bit amd64 Linux platforms (for either GPU-enabled CPU-only basecalling – the package was built on Centos 7)
-   64-bit Ubuntu 18 arm64v8 (the package was built on a Jetson TX2)

GPU devices:
-   A supported NVIDIA GPU in order to perform GPU basecalling

Note: Dorado Basecall Server only supports GPUs with an [NVIDIA compute version](https://developer.nvidia.com/cuda-gpus) of 6.1 or higher.

### Install instructions:
1.  Download the .tar.gz installer for Dorado Basecall Server:
2.  Extract the archive to the desired location.
3.  (Optional) Add the install location's <path>/bin subfolder to the system path, so executables can be called from any working folder.

## Installing Dorado Basecall Server on macOS

### Supported platforms:

Operating system:
-   Intel Mac: 64-bit OSX 10.15 (Catalina) or higher (Note that Intel mac support is limited to CPU only basecalling).
-   Apple Silicon (Arm M1/M2) Mac: 64-bit OSX 12.0 (Monterey) or higher (CPU or GPU-accelerated basecalling).

1.  Download the .zip archive. This can be found on the [Software Downloads](https://community.nanoporetech.com/downloads) page in the Community.
2.  Extract the archive to a location of your choice. Note: You may require Administrator access depending on the location into which you unzip the archive.

# Quick Start

## Running Dorado Basecall Server

### Required parameters

To start a sequencing run with Dorado Basecall Server, you will need to launch the dorado_basecall_server application, and then launch a basecall client in order to pass reads to the server to be processed.

A basecalling server command needs to specify, as a minumum, the following parameters:
-   A logging directory to use, `--log_path`.
-   A basecalling configuration to initialise the server with, `--config`.
-   A port to listen on for connections, `--port`.

A basecalling client command needs to specify, as a minimum, the following parameters:

-   The full path to the directory where the raw read files are located, `--input_path`. The folder can be absolute (e.g. `C:\data\my_reads`) or a relative path to the current working directory (e.g. `..\my_reads`)
-   The full path to the directory where the basecalled files will be saved, `--save_path`. The folder can be absolute or a relative path to the current working directory. This folder will be created if it does not exist using the path you provide. (e.g. if it is a relative path, it will be relative to the current working directory)

Then either:
-   `--config` configuration file containing basecalling parameters

or

-   `--flowcell` flow_cell_version `--kit` sequencing_kit version

### Default parameters

If you only specify the parameters listed above, Dorado Basecall Server will run with a number of other parameters set at their default values, for example:

-   Q-score filtering will be set to ON
-   File compression will be set to OFF
-   GPU acceleration will be disabled.

For a full list of all the optional parameters and their default values, refer to the “Setting up a run: configurations and parameters” section of the protocol.

## Running Dorado Basecall Server on Windows

### Command prompt:

Launch a command prompt. To do this, click on Start and type "Command prompt" in the search box, then click the link. You will be running all operations from here:

![.](img/win_cmd.png)

### Simplex sequencing: command-line entries for basecalling

The following examples assume the Dorado package was extracted to `C:\ont-dorado-server`.
To basecall simplex reads with Dorado Basecall Server, you will need to use the following commands:

-   `"C:\ont-dorado-server\bin\dorado_basecall_server.exe"` to start a basecall server
-   The server will remain running and not return to the prompt, so start a new command prompt.
-   `"C:\ont-dorado-server\bin\ont_basecall_client.exe"` to start a client

**EXAMPLE**

### Simplex Sequencing: Example command-line entries for basecalling an SQK-LSK114 kit with a FLO-MIN114 flow cell experiment

```
C:\ont-dorado-server\bin\dorado_basecall_server.exe --log_path output_folder\server_logs --config dna_r10.4.1_e8.2_400bps_hac.cfg -p 5555
```

then

```
"C:\ont-dorado-server\bin\ont_basecall_client.exe" --input_path reads --save_path output_folder\basecall --config dna_r10.4.1_e8.2_400bps_hac.cfg -p 5555
```

or

```
"C:\ont-dorado-server\bin\ont_basecall_client.exe" --input_path C:\my_folder\reads --save_path C:\output_folder\basecall --flowcell FLO-MIN114 --kit SQK-LSK114 -p 5555
```

**IMPORTANT**

### Dorado Basecall Server executable in Windows:

By default, the Dorado executables (such as `dorado_basecall_server.exe`) will not be on the Windows file path. As a result, you will need to type the full path directory to use an executable.

##   Run Dorado Basecall Server on Linux

### Command prompt

Launch a terminal on your system. For example, when using Ubuntu, you can type Ctrl + Alt + T.

![.](img/linux_cmd.png)

### Simplex Sequencing: command-line entries for basecalling

The following examples assume the dorado package was decompressed to `~/ont-dorado-server`.
To basecall simplex reads with Dorado Basecall Server, you will need to use the following commands:

-   `"~/ont-dorado-server/bin/dorado_basecall_server"` to start a basecall server
-   The server will remain running and not return to the prompt, so start a new command prompt.
-   `"~/ont-dorado-server/bin/ont_basecall_client"` to start a client

**EXAMPLE**

### Simplex Sequencing: Example command-line entries for basecalling an SQK-LSK114 kit with a FLO-MIN114 flow cell experiment

```
~/ont-dorado-server/bin/dorado_basecall_server --log_path output_folder/server_logs --config dna_r10.4.1_e8.2_400bps_hac.cfg -p 5555
```

then

```
~/ont-dorado-server/bin/ont_basecall_client  --input_path /data/my_folder/reads --save_path /data/output_folder/basecall --flowcell FLO-MIN114 --kit SQK-LSK114 -p 5555
```

or

```
~/ont-dorado-server/bin/ont_basecall_client  --input_path reads --save_path output_folder/basecall --config dna_r10.4.1_e8.2_400bps_hac.cfg -p 5555
```

***TIP***

### Alternative commands

On Linux-based platforms, it is also possible to enter files into the basecall client, as follows:

```
ls input_folder/*.fast5 | ont_basecall_client --save_path output_folder/basecall --config dna_r10.4.1_e8.2_400bps_hac.cfg
```


## Run Dorado Basecall Server on macOS

### Command prompt:

Open a command-line terminal. Open your Applications folder, then open the Utilities folder. Click on the Terminal application to open:

![.](img/osx_cmd.png)

**IMPORTANT**

### Before starting:

You must find where the unzipped 'dorado archive' is located – this will give you the path you will need to enter in order to run the basecalling executables.

For example, if you extracted the .zip archive to `/Users/myuser/ont-dorado-server`, then you can run the basecall server using this:

```
/Users/myuser/ont-dorado-server/bin/dorado_basecall_server
```

### Simplex Sequencing: Command-line entries for basecalling

To basecall simplex reads with Dorado Basecall Server, you will need to use the following commands:

-   `"/Users/myuser/ont-dorado-server/bin/dorado_basecall_server"` to start a basecall server
-   The server will remain running and not return to the prompt, so start a new command prompt.
-   `"/Users/myuser/ont-dorado-server/bin/ont_basecall_client"` to start a client

***EXAMPLE***

### Simplex Sequencing: Example command-line entries for basecalling a SQK-LSK114 kit with a FLO-MIN114 flow cell experiment

```
/Users/myuser/ont-dorado-server/bin/dorado_basecall_server --log_path output_folder/server_logs --config dna_r10.4.1_e8.2_400bps_hac.cfg -p 5555
```

then

```
/Users/myuser/ont-dorado-server/bin/ont_basecall_client  --input_path /data/my_folder/reads --save_path /data/output_folder/basecall --flowcell FLO-MIN114 --kit SQK-LSK114 -p 5555
```

or

```
/Users/myuser/ont-dorado-server/bin/ont_basecall_client  --input_path reads --save_path output_folder/basecall --config dna_r10.4.1_e8.2_400bps_hac.cfg -p 5555
```

## General help command-line options

For general help, the following available command-line options, `-h` or `--help`, are provided within the toolkit, for example:

```
<path_to_install>/dorado_basecall_server --help
```

The command `--version` shows the version of Dorado Basecall Server that is installed.

```
<path_to_install>/dorado_basecall_server --version
```

# Features, settings and analysis

## Setting up a run: configurations and parameters

**IMPORTANT**

### Config files - variable parameters

You will need to specify which basecalling configuration to use in Dorado. This can be provided in one of two ways:

-   By selecting a config file:
    -   Config (`-c` or `--config`): either the name of the config file to use, or a full path to a config file (see the section below). If the argument is only the name of a config file then it must correspond to one of the standard configuration files provided by the package.
-   Or by selecting a flow cell and a kit:
    -   Flow cell (`-f` or `--flowcell`): the name of the flow cell used for sequencing (e.g. FLO-MIN114).
    -   Kit (`-k` or `--kit`): the name of the kit used for sequencing (e.g. SQK-LSK114).

Note: If you use the `--config` argument, then `--flowcell` and `--kit` arguments are not needed, and will be ignored.

### Choosing a config file for Dorado

Dorado contains several types of basecalling configurations, many of which are not available by using the flow cell and kit selector. These models will usually have their own config file, and they may then be used with the `--config` argument.

Generally speaking, the configuration file names are structured as follows:

<strand_type>_<pore_type>_<enzyme_type>_[modbases_specifier]_<model_type>_[instrument_type].cfg

-   `strand_type`: This will be the string "dna" or "rna", depending on the sample type.
-   `pore_type`: The pore that the basecalling model was trained for, indicated by the letter "r" followed by a version number. For example: "r9.4.1" or "r10.4.1".
-   `enzyme_type`: The enzyme motor the model was trained for. This will either be the letter "e" followed by a version number, and/or a number indicating the enzyme speed, followed by "bps". For example: "e8.1" or "450bps".
-   `modbase_specifier`: Optional. If specified, indicates that modified base detection will be performed. This will be the string "modbases_" followed by an indicator of the modification supported, such as "5mc_cg" or "5hmc_5mc_cg".
-   `model_type`: The type of basecalling model to use, depending on whether you want optimal basecalling speed or accuracy. See below.
-   `instrument_type`: Optional. If this is not specified, then the configuration is target to a GridION device, or a PC. The strings "mk1c" or "prom" are used to indicate that the configuration parameters and model are optimised for the MinION Mk1C or PromethION devices, respectively. Note that if the kit and flow cell are specified on the command-line instead of a specific config file, then the config file chosen will be one without an instrument type specified.

 The model types are:

-   `sup`: Super-accurate basecalling.
-   `hac`: High accuracy basecalling. These are the configurations that will be selected when a kit and flow cell are specified on the command-line instead of a specific config file.
-   `fast`: Fast basecalling.

For example, to basecall data generated with the r10.4.1 pore and the e8.2 enzyme, sequenced at 400bps, using the Fast model, use:

```
ont_basecall_client -c dna_r10.4.1_e8.2_400bps_fast.cfg [...]
```

To run this on a MinION Mk1C device, use:

```
ont_basecall_client -c dna_r10.4.1_e8.2_400bps_fast_mk1c.cfg [...]
```

#### Config files - selecting kit and flow cell

These should be clearly labelled on the corresponding boxes. Flow cell product codes start with "FLO", and and sequencing kit codes start with "SQK" or "VSK".

To see the supported flow cells and kits, run dorado_basecall_server with the `--print_workflows` option:

```
dorado_basecall_server --print_workflows
```

which will produce an output like this:

```
Available flowcell + kit combinations are:
flowcell       kit               barcoding config_name                    model version
FLO-MIN114     SQK-LSK114                  dna_r10.4.1_e8.2_400bps_hac    dna_r10.4.1_e8.2_400bps_hac@v3.5.2
FLO-MIN114     SQK-LSK114-XL               dna_r10.4.1_e8.2_400bps_hac    dna_r10.4.1_e8.2_400bps_hac@v3.5.2
FLO-MIN114     SQK-ULK114                  dna_r10.4.1_e8.2_400bps_hac    dna_r10.4.1_e8.2_400bps_hac@v3.5.2
FLO-MIN114     SQK-RAD114                  dna_r10.4.1_e8.2_400bps_hac    dna_r10.4.1_e8.2_400bps_hac@v3.5.2
FLO-MIN114     SQK-NBD114-24     included  dna_r10.4.1_e8.2_400bps_hac    dna_r10.4.1_e8.2_400bps_hac@v3.5.2
FLO-MIN114     SQK-NBD114-96     included  dna_r10.4.1_e8.2_400bps_hac    dna_r10.4.1_e8.2_400bps_hac@v3.5.2
FLO-MIN114     SQK-RBK114-24     included  dna_r10.4.1_e8.2_400bps_hac    dna_r10.4.1_e8.2_400bps_hac@v3.5.2
FLO-MIN114     SQK-RBK114-96     included  dna_r10.4.1_e8.2_400bps_hac    dna_r10.4.1_e8.2_400bps_hac@v3.5.2
FLO-PRO002     SQK-LSK112                  dna_r9.4.1_e8.1_hac_prom       2021-09-13_dna_r9.4.1_minion_promethion_384_ca963bcb
FLO-PRO002     SQK-LSK112-XL               dna_r9.4.1_e8.1_hac_prom       2021-09-13_dna_r9.4.1_minion_promethion_384_ca963bcb
FLO-PRO002     SQK-RAD112                  dna_r9.4.1_e8.1_hac_prom       2021-09-13_dna_r9.4.1_minion_promethion_384_ca963bcb
FLO-PRO002     SQK-NBD112-24     included  dna_r9.4.1_e8.1_hac_prom       2021-09-13_dna_r9.4.1_minion_promethion_384_ca963bcb
FLO-PRO002     SQK-NBD112-96     included  dna_r9.4.1_e8.1_hac_prom       2021-09-13_dna_r9.4.1_minion_promethion_384_ca963bcb
FLO-PRO002     SQK-RBK112-24     included  dna_r9.4.1_e8.1_hac_prom       2021-09-13_dna_r9.4.1_minion_promethion_384_ca963bcb
FLO-PRO002     SQK-RBK112-96     included  dna_r9.4.1_e8.1_hac_prom       2021-09-13_dna_r9.4.1_minion_promethion_384_ca963bcb
FLO-PRO002M    SQK-LSK112                  dna_r9.4.1_e8.1_hac_prom       2021-09-13_dna_r9.4.1_minion_promethion_384_ca963bcb
FLO-PRO002M    SQK-LSK112-XL               dna_r9.4.1_e8.1_hac_prom       2021-09-13_dna_r9.4.1_minion_promethion_384_ca963bcb
FLO-PRO002M    SQK-RAD112                  dna_r9.4.1_e8.1_hac_prom       2021-09-13_dna_r9.4.1_minion_promethion_384_ca963bcb
FLO-PRO002M    SQK-NBD112-24     included  dna_r9.4.1_e8.1_hac_prom       2021-09-13_dna_r9.4.1_minion_promethion_384_ca963bcb
FLO-PRO002M    SQK-NBD112-96     included  dna_r9.4.1_e8.1_hac_prom       2021-09-13_dna_r9.4.1_minion_promethion_384_ca963bcb
FLO-PRO002M    SQK-RBK112-24     included  dna_r9.4.1_e8.1_hac_prom       2021-09-13_dna_r9.4.1_minion_promethion_384_ca963bcb
FLO-PRO002M    SQK-RBK112-96     included  dna_r9.4.1_e8.1_hac_prom       2021-09-13_dna_r9.4.1_minion_promethion_384_ca963bcb
FLO-MIN106     SQK-LSK112                  dna_r9.4.1_e8.1_hac            2021-09-13_dna_r9.4.1_minion_promethion_384_ca963bcb
FLO-MIN106     SQK-LSK112-XL               dna_r9.4.1_e8.1_hac            2021-09-13_dna_r9.4.1_minion_promethion_384_ca963bcb
FLO-MIN106     SQK-RAD112                  dna_r9.4.1_e8.1_hac            2021-09-13_dna_r9.4.1_minion_promethion_384_ca963bcb
FLO-MIN106     SQK-NBD112-24     included  dna_r9.4.1_e8.1_hac            2021-09-13_dna_r9.4.1_minion_promethion_384_ca963bcb
FLO-MIN106     SQK-NBD112-96     included  dna_r9.4.1_e8.1_hac            2021-09-13_dna_r9.4.1_minion_promethion_384_ca963bcb
FLO-MIN106     SQK-RBK112-24     included  dna_r9.4.1_e8.1_hac            2021-09-13_dna_r9.4.1_minion_promethion_384_ca963bcb
FLO-MIN106     SQK-RBK112-96     included  dna_r9.4.1_e8.1_hac            2021-09-13_dna_r9.4.1_minion_promethion_384_ca963bcb
FLO-PRO111     SQK-CS9109                  dna_r10.3_450bps_hac_prom      2021-04-20_dna_r10.3_minion_promethion_384_72309afc
FLO-PRO111     SQK-DCS108                  dna_r10.3_450bps_hac_prom      2021-04-20_dna_r10.3_minion_promethion_384_72309afc
FLO-PRO111     SQK-DCS109                  dna_r10.3_450bps_hac_prom      2021-04-20_dna_r10.3_minion_promethion_384_72309afc
[...]
```

When kits come with barcodes included, the barcoding column will specify "included". Reads which have been prepared with these kits can be demultiplexed using `ont_barcoder` (see below).


### Optional parameters

In addition to the required parameters described in the Quick Start section, Dorado has many optional parameters. You can use them if they are applicable to your experiment. The following optional parameters are commonly used:

#### Data features:

-   Q-score filtering (`--disable_qscore_filtering`): Flag to disable filtering of reads into pass/fail folders inside the output folder, based on their strand q-score. See `--min_qscore`
-   Alignment filtering (`--alignment_filtering`): Flag for filtering of reads into pass/fail folders inside the output folder, based on their number of alignments. Can be set to `none` (default) or `fail` to disable or enable this feature.
-   Minimum q-score (`--min_qscore`): The minimum q-score a read must have to pass q-score filtering. The default value for this varies by configuration, ranging from 7.0 for the lower-accuracy models up to 10.0 for the "sup" models. This should have a minimal impact on output.
-   Calibration strand detection (`--calib_detect`): Flag to enable calibration strand detection and filtering. If enabled, any reads which align to the calibration strand reference will be filtered into a separate output folder to simplify downstream processing. Off by default.
-   Alignment reference file (`-a` or `--align_ref`): Optional reference genome file name. If an align_ref is provided, Dorado will perform alignment against the reference for called strands, using the minimap2 library. Providing an align_ref will automatically enable BAM output (see `--bam_out`). See the Alignment section for more information on alignment in Dorado.
-   Read splitting (`--do_read_splitting`): Split potentially concatenated input reads into separate outputs, based on the score obtained from mid-strand adapter detection. See `--min_score_read_splitting`. If enabled, reads which exceed this threshold will be split into two.
-   Read splitting depth (`--max_read_split_depth`): Limit the number of times a read will be passed into the read splitter. e.g. `--max_read_split_depth 2` would permit the read to be split, and then each resulting read to be split a second time, resulting in up to 4 reads. The default value is 2.
-   Minimum read splitting score (`--min_score_read_splitting`): The minimum score a read must generate from mid-strand adapter detection for the read to be considered a concatamer and to be split into two reads for subsequent processing and output. The default is 58.
#### Input/output:

-   Quiet mode (`-z` or `--quiet`): This option prevents the Dorado basecaller from outputting anything to stdout. Stdout is short for “standard output” and is the default location to which a running program sends its output. For a command line executable, stdout will typically be sent to the terminal window from which the program was run.
-   Verbose logging (`--verbose_logs`): Flag to enable verbose logging (outputting a verbose log file, in addition to the standard log files, which contains detailed information about the application). Off by default.
-   Reads per FASTQ file (`-q` or `--records_per_fastq`): The number of reads to put in a single FASTQ file (see output format below). Set this to zero to output all reads into one file (per run id, per caller). The default value is 4000.
-   Perform FASTQ compression (`--compress_fastq`): Flag to enable gzip compression of output FASTQ files; this reduces file size to about 50% of the original.
-   Recursive (`-r` or `--recursive`): Flag to require searching through all subfolders contained in the `--input_path` value, and basecall any .POD5 files found in them.
-   .bam file output (`--bam_out`): Flag to enable output of .bam files containing basecall result sequence.  If a modified base model was used, the modified base locations and probabilities will be emitted. If alignment was performed, the results will also be emitted. BAM file output will be implicitly enabled if `--align_ref` is popultated or a modbase model is selected. Off by default.
-   .bam file indexing (`--index`): Flag to enable the generation of the .bai index file for .bam file output. Requires `--bam_out`. Off by default.
-   Emit move tables (`--moves_out`): Return move table in output BAM file.
-   Methylation probability cutoff (`--bam_methylation_threshold`): The value below which a predicted methylation probability will not be emitted into a BAM file, expressed as a percentage. Default is 5.0(%). Note that if the configuration being used specifies a context to look for base modifications within, then this parameter will not be applied. Instead, any instances of the base which match the context will be emitted in the BAM file, even if the predicted methylation probability is zero.
-   Override default data path (`-d` or `--data_path`): Option to explicitly specify the path to use for loading any data files the application requires (for example, if you have created your own model files or config files).
-   Input file list (`--input_file_list`): Optional file containing list of input read files (fast5/POD5) to process from the input_path.
-   Progress stats reporting frequency (`--progress_stats_frequency`): Frequency in seconds in which Dorado reports progress statistics.  If a frequency is supplied, it will replace the default progress display.
-   Maximum queue size (`--max_queued_reads`): Maximum number of reads "in flight", defaults to 2000. Helps to limit the amount of memory used in the case where basecalling cannnot keep up with the speed reads are loaded.

#### Optimisation:

-   GPU device (`-x` or `--device`): Specify CPU or a GPU device to use to accelerate basecalling. If this option is not selected, dorado_basecall_server will default to CPU usage. You can specify one or more devices where GPUs are counted from zero. Examples:

    | device | result |
    | --- | --- |
    | `cuda:0` | Use the first NVIDIA GPU in the system |
    | `cuda:0,1` | Use the first two NVIDIA GPUs in the system |
    | `cuda:1,3` | Use the second and fourth NVIDIA GPUs in the system |
    | `cuda:all` | Use all NVIDIA GPUs in the system |
    | `cpu` | Use CPU mode, this is the default behaviour if device is not specified |
    | `auto` | Will be resolved as 'cpu' or 'cuda:all' depending on the presence of a cuda device |
    | `metal` | Use the Apple M1/M2 GPU in the system (OSX Arm only) |
    Note: Multiple device IDs are separated by a comma without a space. It is strongly recommended to use a supported GPU if one is available, as basecalling will typically perform orders of magnitude faster.

-   Resume previous run (`--resume`): Flag to enable resuming a previous basecalling run. This option can be used to resume a partially completed basecall if it was interrupted for some reason, or to re-basecall an input directory if more reads were added.

### Resuming runs

If a run of the ont_basecall_client is interrupted for some reason, it is possible to use the `--resume` option to attempt to re-start the basecall from where it was halted. This is useful if basecalling fails during processing particularly large batches of files. Resume should be used with exactly the same parameters as the previous run, or undefined behaviour may occur. If the `--resume` option is specified, the following steps occur:

-   The basecaller checks the output directory to find log files from any previous runs
-   The log files are interrogated to discover any successfully completed reads (and their source files) from previous runs
-   Any files in the output directory, which do not belong to successfully completed reads, are removed (i.e. reads which were partially completed)
-   The data for previously completed reads is extracted from the summary file for the previous run

The basecaller then proceeds as normal, filtering out any input reads which were previously processed.

After resumption of a basecall run, a single summary file will have been produced with all reads from the input folder in it, as if the run was completed normally.

Note: It is possible to chain resume operations together, and it is also possible to resume from a successfully completed operation. This allows the resume functionality to be used to re-basecall an input folder to basecall just the read files which have appeared in that folder since the last basecall operation was invoked on it.

The resume system batches reads internally and records to the logfile when those batches have been completed and written to disk. You can use the `--read_batch_size` argument to control the size of these batches, and control the granularity at which resume operations can occur. Increasing the batch size will reduce the fragmentation of output FASTQ files but can increase the amount of time a resume operation takes, as more previously basecalled reads may be re-called, because their batch was not completed.

## Input and output files

### Input files

POD5 files and FAST5 files (both single- and multi-read) are supported as input.

Both the alignment and barcoding software accept FASTQ files as input. These can be generated either by the Dorado basecallers or by the MinKNOW software.

### Folder structure

If using a version of MinKNOW which outputs raw read files in separate subfolders, it is necessary to use the `--recursive` option listed above to search through them to find input read files.

For example, if the MinKNOW output folder structure looks like this:

```
minknow_output_folder/
--- 0/
      | --- file1.fast5
      | --- file2.fast5
      | [...]
--- 1/
    | --- file10.fast5
    | --- file11.fast5
    | [...]
```

Then calling ont_basecall_client as follows will search through the numbered subfolders for input read files:

```
ont_basecall_client --input_path minknow_output_folder --recursive [...]
```

###  Output formats

ont_basecall_client supports outputting FASTQ files, and optionally BAM, via the `--bam_out` argument. By default, FASTQ or BAM files will contain 4000 reads per file, according to the `--records_per_fastq` argument.

Each FASTQ file contains only reads from a specified run. The default FASTQ filename is:

```
fastq_runid_{run_id}_{batch_id}_{batch_counter}.fastq
```

Where batch_id and batch_counter both increment from zero.

The default FASTQ header is:

```
{read_id} runid={run_id} sampleid={sample_id} read={read_number} ch={channel_id} start_time={start_time_utc}
```
-   **read_id** is the unique ID for the read.
-   **sample_id** is the user-specified sample ID which the read belongs to (read from `tracking_id/sample_id` in the source read file).
-   **read_number** is the sequential read number for the channel (read from the read's `read_number` in the source read file).
-   **channel_id** is the source channel within the flowcell for the read (read from the read's `channel_number` in the source read file).
-   **start_time_utc** is the read's start time (calculated from `tracking_id/exp_start_time` and the read's `start_time` in the source read file).

If barcoding was performed, the FASTQ header will also include a `barcodeid={barcode}` field, where `barcode` is the normalised ID of the detected barcode arrangement.
If read splitting was performed, the FASTQ header will also include a `parent_read_id={parent_read_id}` field, where `parent_read_id` is the `read_id` of the original read from which this read was split.

Multiple input files from the same run_id will be grouped into batches, where the number of reads in a batch is less than or equal to `--read_batch_size`. Individual input files will not be split across batches, even if this means a batch is larger than `--read_batch_size`. Output files for a batch will be split when `--records_per_fastq` reads have been recorded. In the case where `--records_per_fastq` is set to 0, all reads from a batch will be written into a single file (per run_id).

### Contents of the output folder
The save path will have the following structure once ont_basecall_client has finished running:

-   `ont_basecall_client_log_<time_and_date>.log` A log file of what ont_basecall_client did during this basecall session.
-   `sequencing_summary.txt` A tab-delimited text file containing useful information for each read analysed during this basecall.
-   `fastq_runid_<run_id>_<batch_id>_<file_number>.fastq` A collection of FASTQ files will be emitted containing the basecall results. Each FASTQ file may contain many reads. A set of FASTQ files will be generated for each run ID in the input file set. Additionally, depending on the `--read_batch_size` and `--records_per_fastq` settings, a single run ID may generate multiple FASTQ files.

Note: The FASTQ files in the output folder may be separated into 'pass', 'fail', and 'calibration_strands' folders, depending on whether they pass or fail the filtering conditions or whether they have been identified as a calibration strand. This behaviour may be controlled with the `--disable_qscore_filtering` and `--calib_detect` options. For example, if both options are enabled, the output folder structure would look like this:

```
output_folder/
--- pass/
| fastq_runid_777_0_0.fastq
| fastq_runid_abc_0_0.fastq
| fastq_runid_abc_0_1.fastq
| fastq_runid_abc_1_0.fastq
--- fail/
| fastq_runid_777_0_0.fastq
--- calibration_strands/
| fastq_runid_777_0_0.fastq
```

Whereas turning both options off would produce a folder layout like this:

```
output_folder/
| fastq_runid_777_0_0.fastq
| fastq_runid_abc_0_0.fastq
| fastq_runid_abc_0_1.fastq
| fastq_runid_abc_1_0.fastq
```

If barcode detection was performed, the basecaller will demultiplex the reads into separate subfolders (within the 'pass' and 'fail' and 'calibration_strands' folders if applicable), like this example:
```
output_folder/
--- pass/
| ---barcode01/
| | fastq_runid_abc_0_0.fastq
| ---unclassified/
| | fastq_runid_abc_0_0.fastq
--- fail/
| ---unclassified
| | fastq_runid_abc_0_0.fastq
```

ont_basecall_client will not empty the save path before writing the output, but it will overwrite existing FASTQ files.

#### Nested output folders

ont_basecall_client also supports an alternative output folder structure, designed to match that produced by MinKNOW.  This can be enabled using the command line switch `--nested_output_folder`.  When enabled, ont_basecall_client will further organise the output subfolders as follows:
```
output_folder/
--- {protocol_group_id} (if it exists is source fast5 files)/
| ---{sample_id}/
| | ---{experiment_start_time}_{device_id}_{flow_cell_id}_{protocol_run_id}/
| | | ---fastq_pass or fastq_fail/
| | | | ---{barcode classification} (if it exists for the read, otherwise this folder is absent)
```

An alternative nested folder output is available which is very similar to the above, but places the barcode classification directly under the protocol group id.  This scheme can be enabled using the command line switch `--barcode_nested_output_folder`.  The folders are organised as follows:
```
output_folder/
--- {protocol_group_id} (if it exists is source fast5 files)/
| ---{barcode classification}/ (if it exists for the read, otherwise this folder is absent)
| | ---{sample_id}/
| | | ---{experiment_start_time}_{device_id}_{flow_cell_id}_{protocol_run_id}/
| | | | ---fastq_pass or fastq_fail
```

### Ping information

ont_basecall_client collects high-level summary information when it is used, and by default this information is sent over your internet connection to Oxford Nanopore Technologies. This is important information that allows us to analyse the performance of our basecaller and identify areas where we need to improve. Nothing specific about the genomic content of individual reads is included - only generic information is logged, such as sequence length and q-score, aggregated over all the reads processed by the basecaller. The sending of this summary information can be turned off if desired by providing the `--disable_pings` option to ont_basecall_client.

ont_basecall_client collects this high-level summary information as follows:

-   Individual reads are added to an aggregator as they are basecalled
-   The summary ping(s) are written out to a file (js)
-   If not disabled, the summary ping(s) are sent to Oxford Nanopore

This type of information is collected:

-   General information about the configuration of the basecaller and the run(s) that the data came from:
    -   the options provided to ont_basecall_client
    -   the total number of reads seen, and those seen per channel
-   Basecalling information:
    -   the numbers of reads which passed or failed basecalling
    -   the average sequence length
    -   the distribution of mean q-scores
    -   the distribution of basecalling speeds

We encourage you to browse the `summary_telemetry.js` file if you wish to see exactly what information is aggregated for telemetry.

### Summary file contents

ont_basecall_client produces a summary file named `sequencing_summary.txt` during basecalling, which contains high-level information on every read analysed by the basecaller. This file is a tab-delimited text file which can be imported into common spreadsheet applications such as Excel or LibreOffice Calc, or read by software libraries such as numpy or pandas. Every read that is sent to the basecaller will have an entry in the summary file, regardless of whether or not that read was successfully basecalled.

When enabling extra functionality such as barcoding or alignment, additional columns will be added to the summary file. For this reason, and because the columns may occasionally be re-ordered, it is recommended that specific columns are accessed by their name (e.g. the `read_id` column) instead of the order in which they occur in the file.

Below is a list of summary file columns with a description of their contents. Note: very occasionally new columns may be added to the file without being described here; these columns should be considered unreliable and subject to change or removal.

-    **filename** The name of the input read file that the read came from.
-    **read_id** The uuid that uniquely identifies this read.
-    **parent_read_id** The uuid that uniquely identifies the original input read from which this read was generated. This column will only be present if `--do_read_splitting` is enabled. For unsplit reads, this value will be identical to **read_id**.
-    **run_id** The uuid that uniquely identifies the sequencing run that this read came from.
-    **batch_id** Integer identifier of the batch that the basecaller put this read in. See the `--read_batch_size` parameter and the `--resume` option.
-    **channel** The channel on the flow cell that the read came from.
-    **mux** The mux in the channel that the read came from.
-    **start_time** Start time of the read, in seconds since the beginning of the run.
-    **duration** Duration of the read, in seconds.
-    **minknow_events** The number of events detected by MinKNOW. Defaults to zero if unknown, or if the value cannot be determined due to read-splitting.
-    **passes_filtering** Whether or not the read passed the q-score and alignment filters (the value is not affected by the `--disable_qscore_filtering` and `--alignment_filtering` flags). See the `--min_qscore` parameter.
-    **template_start** Start time of the portion of the read that was sent to the basecaller after adapter trimming, in seconds since the beginning of the run.
-    **num_events_template** Legacy field -- **template_duration** should be used instead.
-    **template_duration** Duration of the portion of the read that was sent to the basecaller after adapter trimming, in seconds.
-    **sequence_length_template** Number of bases in the output sequence, taking into account any sequence trimming. See [Barcode Trimming](#barcode-trimming).
-    **mean_qscore_template** The q-score corresponding to the mean error rate of the sequence.
-    **median_template** The median current of the read, in pA.
-    **scaling_median_template** The "median_template" value used by the basecaller to scale incoming data. May be different than **median_template** if adapter scaling or scaling overrides are used. See the  `--scaling_med` parameter.
-    **scaling_mad_template** The "mad_template" value used by the basecaller to scale incoming data. May be different than **mad_template** if adapter scaling or scaling overrides are used. See the `--scaling_mad` parameter.

If barcoding/demultiplexing is enabled via the `--barcode_kits` argument, then the following columns are added to the sequencing summary file:

-    **barcode_arrangement** The normalised name of the barcode classification, without a kit (e.g. "barcode01"), or "unclassified" if no classification could be made.
-    **barcode_full_arrangement** The full name for the highest-scoring barcode match, including kit, variation, and direction (e.g. "RAB19\_var2").
-    **barcode_kit** The kit name belonging to the highest-scoring barcode match (e.g. "RAB").
-    **barcode_variant** Which of the forward / reverse variants the highest-scoring barcode matched (e.g. "var1"), or "n/a" if no variants are available.
-    **barcode_score** The score for either the front or rear barcode, whichever is higher. The maximum score is 100, with no minimum.
-    **barcode_front_id** The full name for the barcode at the front of the strand, including direction (forward / reverse) and variant (1st / 2nd) (e.g. "RAB19\_2nd\_FWD").
-    **barcode_front_score** The score for the barcode at the front of the strand.
-    **barcode_front_refseq** The reference sequence that the barcode at the front of the strand was matched against.
-    **barcode_front_foundseq** The sequence of the barcode at the front of the strand that matched `barcode_front_refseq`.
-    **barcode_front_foundseq_length** The length of `barcode_front_foundseq`.
-    **barcode_front_begin_index** The position in the called sequence, counting from the beginning, that `barcode_front_foundseq` begins at.
-    **barcode_rear_score** The score for the barcode at the rear of the strand.
-    **barcode_rear_refseq** The reference sequence that the barcode at the rear of the strand was matched against.
-    **barcode_rear_foundseq** The sequence of the barcode at the rear of the strand that matched `barcode_rear_refseq`.
-    **barcode_rear_foundseq_length** The length of `barcode_rear_foundseq`.
-    **barcode_rear_end_index** The position in the called sequence, counting backwards from the end, that `barcode_rear_foundseq` ends at.

If dual barcoding is used the following additional columns will be present:

-    **barcode_front_id_inner**
-    **barcode_front_score_inner**
-    **barcode_rear_id_inner**
-    **barcode_rear_score_inner**

These columns have the same meaning as the standard "id" and "score" columns above, but apply only to the inner front and rear barcodes. The standard "id" and "score" columns now apply to the outer barcodes.

If LAMPore detection is enabled via the `--lamp_detect` argument, the following additional columns will be present:
-    **lamp_barcode_id** The normalized name of the LAMP FIP barcode classification, (e.g. "FIP01"), or "unclassified" if no classification could be made.
-    **lamp_barcode_score** The alignment score for the best-scoring LAMP FIP barcode. Note that if the best score is below the threshold specified by `--min_score_lamp`, the score will still be reported here, although the classification will be "unclassified".
-    **lamp_target_id** The target name of the LAMP target classification (e.g. "ACTB"), or "unclassified if no classification could be made.
-    **lamp_target_score** The alignment score for the best-scoring LAMP target. Note that if the best score is below the threshold specified by `--min_score_lamp_target`, the score will still be reported here, although the classification will be "unclassified".

If adapter detection is enabled via the `--detect_adapter` argument, the following additional columns will be present:
-    **adapter_front_id** The name of the adapter (if any) found at the front of the strand. This will be "unclassified" if no adapter was found.
-    **adapter_front_score** The alignment score of the adapter at the front of the strand. If unclassified, this will be the score that was highest among the rejected sequences.
-    **adapter_front_begin_index** The position in the called sequence of the beginning of the adapter, counting from the beginning of the strand.
-    **adapter_front_foundseq_length** The length of the portion of the strand that aligned to the adapter.
-    **adapter_rear_id** The name of the adapter (if any) found at the rear of the strand. This will be "unclassified" if no adapter was found.
-    **adapter_rear_score** The alignment score of the adapter at the rear of the strand. If unclassified, this will be the score that was highest among the rejected sequences.
-    **adapter_rear_end_index**  The position in the called sequence of the end of the adapter, counting from the end of the strand.
-    **adapter_rear_foundseq_length** The length of the portion of the strand that aligned to adapter.

If primer detection is enabled via the `--detect_primer` argument, the following additional columns will be present:
-    **primer_front_id** The name of the primer (if any) found at the front of the strand. This will be "unclassified" if no primer was found.
-    **primer_front_score** The alignment score of the primer at the front of the strand. If unclassified this will be the score that was highest among the rejected sequences.
-    **primer_front_begin_index** The position in the called sequence of the beginning of the primer, counting from the beginning of the strand.
-    **primer_front_foundseq_length** The length of the portion of the strand that aligned to primer.
-    **primer_rear_id** The name of the primer (if any) found at the rear of the strand. This will be "unclassified" if no primer was found.
-    **primer_rear_score** The alignment score of the primer at the rear of the strand. If unclassified this will be the score that was highest among the rejected sequences.
-    **primer_rear_end_index**  The position in the called sequence of the end of the primer, counting from the end of the strand.
-    **primer_rear_foundseq_length** The length of the portion of the strand that aligned to primer.

If barcode trimming is enabled via `--enable_trim_barcodes`, or adapter or primer trimming is enabled via the `trim_adapters`, or `trim_primers` arguments, then the following additional columns will also be present:
-    **front_total_trimmed** The number of bases removed from the front of the sequence as part of trimming.
-    **rear_total_trimmed** The number of bases removed from the rear of the sequence as part of trimming.

For further details on how barcoding works, see "how barcode demultiplexing works" below.

If alignment is enabled via the `--align_ref` argument, then the following columns are added to the sequencing summary file:

-    **alignment_genome** The name of the reference which the read aligned to, or "*" if no alignment was found.
-    **alignment_genome_start** The position in the reference where the alignment started, or 0 if no alignment was found.
-    **alignment_genome_end** The position in the reference where the alignment ended, or 0 if no alignment was found.
-    **alignment_strand_start** The position in the called sequence where the alignment started, or 0 if no alignment was found.
-    **alignment_strand_end** The position in the called sequence where the alignment ended, or 0 if no alignment was found.
-    **alignment_num_insertions** The number of insertions in the alignment, or -1 if no alignment was found.
-    **alignment_num_deletions** The number of deletions in the alignment, or -1 if no alignment was found.
-    **alignment_num_aligned** The number of bases in the called sequence which aligned to bases in the reference, or -1 if no alignment was found.
-    **alignment_num_correct** The number of aligned bases in the called sequence which match their corresponding reference base, or -1 if no alignment was found.
-    **alignment_identity** The percentage of aligned bases which correctly match their corresponding reference base (**alignment_num_correct** / **alignment_num_aligned**), or -1 if no alignment was found.
-    **alignment_accuracy** The percentage of all bases in the alignment which are correct (**alignment_num_correct** / (**alignment_num_aligned** + **alignment_num_insertions** + **alignment_num_deletions**)), or -1 if no alignment was found.
-    **alignment_score** The score returned by minimap2, or -1 if no alignment was found.
-    **alignment_coverage** The percentage of either the called sequence or the reference (whichever is shorter) that aligns (e.g. (**alignment_strand_end** - **alignment_strand_start** + 1) / **sequence_length_template**), or -1 if no alignment was found.
-    **alignment_direction** The direction of the alignment, either forwards (+) or reverse (-), or "*" if no alignment was found. Note that genome positions (e.g. **alignment_genome_start**) are always given in the forwards direction.
-    **alignment_mapping_quality** The mapping quality of the alignment. It equals −10 log10 Pr{mapping position is wrong}, rounded to the nearest integer. A value 255 indicates that the mapping quality is not available.
-    **alignment_num_alignments** The total number of alignments found. This will be zero if no alignment was found.
-    **alignment_num_secondary_alignments** The number of alignments that were flagged by minimap2 as secondary alignments.
-    **alignment_num_supplementary_alignments** The number of alignments that were flagged by minimap2 as supplementary alignments.

## dorado_basecall_server

### dorado_basecall_server

The `dorado_basecall_server` executable provides basecalling as a network-enabled service. The basecall server is useful in situations where a set of compute resources such as GPUs need to be shared between several concurrently-running basecalling clients. It enables client applications to perform basecalling by communicating with the server via the ZMQ socket interface. Oxford Nanopore Technologies products which support multiple flow cells typically use Dorado in a server configuration to share the embedded GPUs between all flow cells.

The server is launched as follows:

```
dorado_basecall_server --config <config file> --log_path <log file folder> --port 5555 [--allow_non_local] [--use_tcp]
```

The basecall server requires a basecalling config file. It also requires a `--log_path` to be specified, which will be used to output the server execution log. The final required parameter is `--port`, which specifies the path to a local Unix socket file (on supported systems) or the socket port number on which the server will listen for connections. The `--port` parameter may also be set to `auto`, in which case the server will generate a path in the system temporary folder for socket file connections or provide an available port number for TCP connections.

```
dorado_basecall_server --config <config file> --log_path <log file folder> --port auto
```

To force the use of a tcp connection, pass the optional flag `--use_tcp` on the command line (this flag has no effect on unsupported platforms, e.g. Windows). By default, the server only listens for TCP connections on the localhost interface. The optional flag `--allow_non_local` is used to permit connections to the server from addresses other than localhost - this flag also implies `--use_tcp` on supported systems.

On startup the server will output something similar to the following:

```
ONT Dorado basecall server software version 7.0.2+7e7b7d0
config file:        /opt/ont/dorado/data/dna_r10.4.1_e8.2_400bps_fast.cfg
model file:         /opt/ont/dorado/data/template_r10.4.1_e8.2_400bps_fast.jsn
log path:           /tmp
chunk size:         1000
chunks per runner:  48
max queued reads:   2000
num basecallers:    1
num socket threads: 1
gpu device:         cuda:0
kernel path:
runners per device: 2

Starting server on port: 5555
```

The server may take a few seconds to fully launch, but once the "Starting server" line is output, the server is ready for connections.

If the server fails to start due to being improperly configured, it will exit with exit code 2, and details about what went wrong will be output to the log file. Some examples of things that could go wrong include:
* Required command-line parameters were not provided.
* The configuration file does not exist, or it specifies a model file that does not exist.
* The CUDA device specified does not exist, or is otherwise unavailable.
* The CUDA device does not have enough memory to support the requested configuration.
* The path that the log files should be written to cannot be accessed for writing.

In general, any automated software that is responsible for starting the server should check for a return code of 2, and if present, this means that subsequent attempts to start the server with the same input parameters will also fail if the problem is not addressed.

If the server crashes due to an exception being thrown within the software, details of the error will appear in the logs. In this case the return code will be 1. Any other return codes (other than 0, which indicates normal shutdown), will indicate that the server has crashed in a way that may have prevented any information about the nature of the error being logged properly.

Once the server is running, it can be used to basecall by running the `ont_basecall_client` application. A socket file path or connection port is specified:

```
ont_basecall_client  --input_path reads --save_path output_folder/basecall --config dna_r10.4.1_e8.2_400bps_fast.cfg --port ~/my_socket_files/socket1
```

Note that socket files only permit local connections.

To use a TCP socket connection, add the `--use_tcp` flag in the same way as when launching the server:

```
ont_basecall_client  --input_path reads --save_path output_folder/basecall --config dna_r10.4.1_e8.2_400bps_fast.cfg --port 5555 --use_tcp
```

If only a port is specified to the `ont_basecall_client` as above, it will assume the server is running on the local host. However, it is also possible to specify an address or hostname:

```
ont_basecall_client  --input_path reads --save_path output_folder/basecall --config dna_r10.4.1_e8.2_400bps_fast.cfg --port 192.168.0.64:5555 --use_tcp
```

or

```
ont_basecall_client  --input_path reads --save_path output_folder/basecall --config dna_r9.4.1_450bps_fast.cfg --port my_basecall_server:5555 --use_tcp
```

In this case, the connection can be made to a remote server. Note that to allow connections from clients specified in this way, the server must be launched with the `--allow_non_local` command-line flag. If the server was launched with `--allow_non_local`, the client must use `--use_tcp`, even if this flag was not passed to the server.

Note: Basecalling performance may be compromised by network bandwidth when using a remote server. It is possible for multiple clients to connect to a basecall server simultaneously and the server will distribute processing resource between them using a fair queuing system.

Note: Read trimming and file output will be performed on the client, so any parameters to control those steps must be specified when launching the client, not the server.

### Basecall server-specific parameters

To start the basecall server, you will need to specify the path for logging.

-   Logging path (`--log_path`): The path to the folder to save a basecall log. The logs contain all the messages that are output to the terminal, plus additional informational messages. For example, the log will contain a record for each input file which is loaded and each file which is written out. Any error or warning messages generated during the run will also go in the log, which can be used for diagnosing problems. If you specify the --verbose flag, an additional verbose log file is written out.
-   Maximum queue size (`--max_queued_reads`): Maximum number of reads to queue per client. When running in client/server mode, the client will load files from disk and send them immediately to the server for basecalling. If the client can load and send reads faster than the basecaller can process them, queued reads will pile up on the basecall server, increasing memory consumption. To avoid this problem, `--max_queued_reads` specifies a maximum number of reads that an individual client can have in flight on the server at once. This has a default value of 2000, which is sufficient for MinION Mk 1B and GridION setups with a single client attached. When running multiple clients, the number should be reduced to prevent excessive memory usage.
-   Allow non-local connections (`--allow_non_local`): By default the server will only accept connections from clients on localhost. Pass this flag to allow incoming connections on other interfaces.
-   High priority read threshold (`--high_priority_threshold`):	Number of high priority chunks to process for each medium priority chunk. Default is 10.
-   Medium priority read threshold (`--medium_priority_threshold`):	Number of medium priority chunks to process for each low priority chunk. Default is 4.
-   Maximum IPC message block size (`--max_block_size`): Maximum block size (in samples) of messages. Reads over the maximum size will be sent in multiple parts. Default is 256000.
-   Number of threads for IPC message handling (`--ipc_threads`): Number of threads to use for inter-process communication. Default is 2.

### Basecall client-specific parameters

-   Server connection hostname and port (`-p` or `--port`): Specify a hostname and port for connecting to basecall service (ie 'myserver:5555'), or port only (ie '5555'), in which case localhost is assumed. This is the port used to communicate between the basecall client and server. The client and server both need to use the same port number or they will not be able to connect to each other.
-   Client ID (`--client_id`): An identifier for the `ont_basecall_client` instance. If supplied, this identifier will be included in any files output by the `ont_basecall_client`. This may be used to guarantee unique filenames in the case that multiple `ont_basecall_client` processes are writing to the same output folder. This can used when there are multiple `ont_basecall_client` clients processing reads at the same time. To avoid the clients overwriting each other’s files, giving each one a unique client ID will allow it to label its output files with the ID and make them unique per client.
-   Client connection timeout (`--conn_timeout_ms`): Connection timeout in milliseconds before the server considers the client as disconnected. Set to zero to disable the server auto-disconnecting the client.
-   Max server read failure count (`--max_server_read_failures`): Maximum times to try resending in-flight reads when the server repeatedly crashes.
-   Server file loading timeout (`--server_file_load_timeout`):	Timeout in seconds to wait for the server to load a requested data file (e.g. a basecalling model or alignment index). This may need increasing if very large alignment references are being requested. Default is 180 seconds.


### Oxford Nanopore Technologies basecall supervisor

The package also includes an executable called `ont_basecaller_supervisor`.

A single `ont_basecall_client` will struggle to read files fast enough to supply a `dorado_basecall_server` especially in a multiple GPU system. In order to improve the GPU utilisation it is necessary to have multiple clients connecting to the basecall server. The `ont_basecaller_supervisor` application is provided to simplify the process of connecting multiple clients to a server while all reading from the same input location and writing to the same save path.

This supervisor application ensures that:

1. All files from the input location are distributed amongst the child basecaller clients, and
2. Each client is launched with a unique client_id guaranteeing all files written to the save folder will be uniquely named.

Once all basecaller clients have completed the supervisor exits, a return code of zero indicating success.

### Usage

The basecaller supervisor is launched with exactly the same parameters as the `ont_basecall_client`, but with the addition of a `--num_clients` parameter.

For example, to launch three `ont_basecall_client` processes all reading from the same input location and writing to the same save location:

(The following assumes that the basecall server has already been launched and is listening on tcp port 5555)

```
ont_basecaller_supervisor  --num_clients 5 --input_path reads --save_path ./save_folder/ --config dna_r10.4.1_e8.2_400bps_fast.cfg --port 5555 --use_tcp
```

**Note: the output will be written by each client individually and is not merged. In particular, it is worth noting that there will be one sequencing summary per client.**

Depending on your requirements, some further processing may be necessary to merge the sequencing summary files.

Example output files:

```
--- /save_folder/
		| fastq_runid_6dce0a5_client0_0_0.fastq
		| fastq_runid_6dce0a5_client1_0_0.fastq
		| fastq_runid_6dce0a5_client2_0_0.fastq
		| ont_basecall_client_0_log-2019-11-25_15-11-53.log
		| ont_basecall_client_1_log-2019-11-25_15-11-53.log
		| ont_basecall_client_2_log-2019-11-25_15-11-53.log
		| ont_basecaller_supervisor_log-2019-11-25_15-11-53.log
		| sequencing_summary_0.txt
		| sequencing_summary_1.txt
		| sequencing_summary_2.txt
		| sequencing_telemetry_0.js
		| sequencing_telemetry_1.js
		| sequencing_telemetry_2.js
```

### Command-line configuration arguments

Any configuration parameters currently passed to the `ont_basecall_client`, e.g. `--compress_fastq`, etc., should also be suitable for the `ont_basecall_supervisor` as these will be directly forwarded to the clients.

To choose an optimum value for the `--num_clients` parameter, some trial and error is necessary, for example start with `num_clients 1` and increase until no further benefit is noticed. The output from the supervisor may well be useful in determining this as it reports the samples/second, i.e.

```
Caller time: 5405 ms, Samples called: 186589921, samples/s: 3.45217e+07
```

For more detailed metrics, the `--progress_stats_frequency` argument can be used, although this reports bases called/second as opposed to samples. Below is some sample output with `progress_stats_frequency 5`

```
Found 38 input read files to process.
Processing ...
[PROG_STAT_HDR] time elapsed(secs), time remaining (estimate), total reads processed, total reads (estimate), interval(secs), interval reads processed, interval bases processed, bases/sec
[PROG_STAT] 5.00439, 10.8428, 12, 38, 5.00439, 12, 66073, 13203.0
[PROG_STAT] 10.0091, 8.10263, 21, 38, 5.00466, 9, 61161, 12220.8
[PROG_STAT] 15.0133, 1.76627, 34, 38, 5.0041, 13, 71410, 14270.3
[PROG_STAT] 17.1152, 0, 38, 38, 2.10173, 4, 35785, 17026.5
Caller time: 17530 ms, Samples called: 2157249, samples/s: 123060
All instances of ont_basecall_client completed successfully.
```

#### Notes

- The intended usage is that the supervisor will be running clients that connect to a server, therefore it is necessary to supply the `--port` argument.
- If the basecall server was launched with the `--use_tcp` and/or `--allow_non_local` options then `--use_tcp` should also be supplied when launching the supervisor.
- Since the child basecall clients are using a server for the actual basecalling, the `--device` argument should not be supplied.

## Expert settings

### Changing configuration of the GPU version of Dorado with MinKNOW-for-MinION

In some cases, you may wish to reconfigure how GPU-enabled MinKNOW for MinION installations are set up, to get the best out of the available hardware on the host device. Note that GPU basecalling is supported on NVIDIA GPUs only, and only on Linux and Windows.

Modifying the installation of GPU versions of Dorado and MinKNOW is done at your own risk. Misconfiguration of the GPU may result in slow basecalling and/or a large number of skipped reads if the basecall server crashes due to misparameterisation.

A GPU with at least 12GB of memory is recommended. GPUs with less than 8GB of memory may not work, especially with HAC or SUP models.

#### Linux reconfiguration

The following commands need to be entered into a terminal. Note that some of them will require superuser privileges:

1. Use systemctl to edit the existing doradod service (this will open a text editor with a copy of the existing service file):

```
sudo systemctl edit doradod.service --full
```

   If a prompt appears asking about overwriting the existing doradod.service file, hit 'y' to continue.

2. Edit that new service file to contain the required GPU configuration for the dorado_basecall_server (see "Reconfiguration case" sections below). You can change any other server arguments at the same time.

   To do so, change this line in the service file:

```
ExecStart=/opt/ont/dorado/bin/dorado_basecall_server <arguments>
```

3. Save the file and exit the text editor (the filename may look odd, but don't worry -- systemctl will change it to the correct name later).

4. Stop the MinKNOW service:

```
sudo service minknow stop
```

5. Stop the doradod service.

```
sudo service doradod stop
```

6. Confirm the `dorado_basecall_server` process is not running:

```
ps -A | grep dorado_basecall
```

   If the result of the above command is not blank, manually kill the process:

```
sudo killall dorado_basecall_server
```

7. Start the doradod service.

```
sudo service doradod start
```

8. Confirm the `dorado_basecall_server` is running and is using the GPU:

```
nvidia-smi
```

   If the Dorado basecall server is not launching correctly, check its log output using journalctl ("-n 100" shows the last 100 entries in the journal) to see what went wrong:

```
sudo journalctl -u doradod.service -n 100
```

   Confirm that the newly updated settings are being used by the doradod service:

```
sudo service doradod status
```

   The output should include a line starting "CGroup" which will contain the arguments used by the basecall server.  There should also be a line starting "Active: active (running)".

9. Start the MinKNOW service.

```
sudo service minknow start
```

10. Monitor your first sequencing run using the GUI to make sure basecalling is working as expected.

##### Troubleshooting

 If some part of the above process does not work, then it is possible the doradod service may end up misconfigured, and may be automatically disabled by the system. There are a few diagnostic checks that can be performed:

1. Check in the Dorado basecall server logs.

   Dorado's log files are stored in `/var/log/dorado`

2. Use journalctl to directly read the log entries produced by Dorado and systemctl:

```
sudo journalctl -u doradod.service -n 100
```

3. Check whether the service is enabled.

```
systemctl list-unit-files | grep doradod.service
```

   If the service is not listed as "enabled", then it will either be marked as "disabled" or "masked". You can reset those statuses like this:


   If the service is marked as "disabled":

```
sudo systemctl enable doradod.service
```

   If the service is marked as "masked":

```
sudo systemctl unmask doradod.service
```

   (you may then need to "enable" the service as described above)

4. Reinstall the service.

```
   sudo apt install --reinstall ont-doradod-for-minion
   sudo systemctl revert doradod.service
   sudo service doradod restart
```

  You will then need to repeat the above step to reconfigure doradod's override.conf file.

#### Windows reconfiguration

The following commands need to be entered into a Windows command prompt which has been run as an adminstrator. They also assume a standard MinKNOW installation, where the location of MinKNOW is `C:\Program Files\OxfordNanopore\MinKNOW`.

1. Modify MinKNOW's application configuration to set the appropriate settings depending on the reconfiguration required (see "Reconfiguration case" sections below).

   For example to change the used CUDA devices to just use device 1, you might run:

```
"C:\Program Files\OxfordNanopore\MinKNOW\bin\config_editor.exe" ^
--conf application --filename "C:\Program Files\OxfordNanopore\MinKNOW\conf\app_conf" ^
--set basecaller.server_config.gpu_devices="cuda:1"
```

   Information about basecalling settings can be found in the appropriate section of the dorado protocol on the community.

2. Restart the MinKNOW service:

  - Open the Windows menu.
  - Type "services" and select the "Services" app that is displayed.
  - Scroll down and find the "MinKNOW" service.
  - Right-click on it and select "Restart".

3. Confirm the `dorado_basecall_server` is using the GPU:

```
nvidia-smi
```

   Note that in some instances, nvidia-smi will not report running processes if launched through CMD.  Running nvidia-smi in PowerShell will show the correct processes if this occurs.

4. Monitor your first sequencing run using the GUI to make sure basecalling is working as expected.

##### Troubleshooting

If step 3 above does not show `dorado_basecall_server` using the GPU, or if `dorado_basecall_server` crashes frequently, then it is recommended to check the Dorado log files. Those files are normally found in `C:\data\dorado_logs`, and a new file will be created every time the basecall server is launched.

1. If there is no server log with a timestamp that roughly matches step 2 ("Restart the MinKNOW service") above, then a new basecall server has not been launched. Try restarting the MinKNOW service again. If there is still no new log file created, restart your computer.

2. If there is a new server log file but it does not contain the parameters that were set as part of step 1 ("Modify MinKNOW's application configuration") above, repeat steps 1 and 2.

3. If, during step 1 you see the following error message:

```
Failed to open C:\Program Files\OxfordNanopore\MinKNOW\conf\app_conf for writing.
```

   Then your terminal has not been run as an administrator. Set up Administrator access and run the Windows reconfiguration again.

#### Reconfiguration case: Changing the set of GPUs used.

By default, MinKNOW will configure the `dorado_basecall_server` with `--device cuda:all`, which tells the server to use all the GPUs on the host machine.  If this is not desired, the `--device` parameter can be changed to select specific devices (e.g. `--device cuda:0`).  See the the "Optional parameters" part of the Dorado protocol for more information on the `--device` argument.

- On Linux, edit the doradod service file and change the `--device` command line parameter.
- On Windows, this setting can be changed by specifying a new `basecaller.server_config.gpu_devices` like so:

```
"C:\Program Files\OxfordNanopore\MinKNOW\bin\config_editor.exe" ^
--conf application --filename "C:\Program Files\OxfordNanopore\MinKNOW\conf\app_conf" ^
--set basecaller.server_config.gpu_devices="cuda:1"
```

##### Configure dorado_basecall_server to use TCP and allow remote connections

By default the `dorado_basecall_server` will only allow connections from other processes running on the same computer (for security purposes). In some cases you may want to be able to connect from other PCs to perform basecalling, while at the same time allowing MinKNOW to run as normal and also make use of the `dorado_basecall_server` server.

    - On Linux, edit the doradod service file and add `--use_tcp` and `--allow_non_local` to the `ExecStart` line, before restarting the service.
    - On Windows, edit MinKNOW's application configuration to add `--allow_non_local` to the basecaller's "extra arguments" section:

```
"C:\Program Files\OxfordNanopore\MinKNOW\bin\config_editor" ^
--conf application --filename "C:\Program Files\OxfordNanopore\MinKNOW\conf\app_conf" ^
--set basecaller.server_config.extra_arguments="--allow_non_local"
```

On Linux, it will also be necessary to configure MinKNOW to use TCP to connect to the basecall server (On Windows MinKNOW always uses TCP for these connections).

    - On Linux, edit the file `/opt/ont/minknow/conf/app_conf file` and add the following lines:

```
    - name: server_port
      type: int
      default: 5555
    - name: server_ipc_file
      type: std::string
      default: '"/tmp/.dorado/5555"'
    - name: use_tcp
      type: bool
      default: defaults::basecaller_use_tcp()
```

Then restart MinKNOW with the command: `systemctl restart minknow`

See [Changing configuration of the GPU version of Dorado with MinKNOW-for-MinION](#changing-configuration-of-the-gpu-version-of-dorado-with-minknow-for-minion) for more information.

### Parameters for expert users

There are additional advanced options for expert users. Experimenting with these parameters may significantly impact the performance or accuracy of the basecaller:

#### Data features

-   Calibration strand reference file (`--calib_reference`): Provide a FASTA file to override the reference calibration strand.
-   Calibration strand candidate minimum sequence length (`--calib_min_sequence_length`): Minimum sequence length for reads to be considered candidate calibration strands.
-   Calibration strand candidate maximum sequence length (`--calib_max_sequence_length`): Maximum sequence length for reads to be considered candidate calibration strands.
-   Calibration strand minimum coverage (`--calib_min_coverage`): Minimum reference coverage of candidate strand required for a read to pass calibration strand detection.
-   Override automatic read scaling (`--override_scaling`): Flag to manually provide scaling parameters rather than estimating them from each read. See the `--scaling_med` and `--scaling_mad` options below. Note that if `--ignore_scaling_from_read_files` is not set, scaling overrides will only apply to reads which did not have scaling information stored in the source file.
-   Manual read scaling median (`--scaling_med`): Median current value to use for manual scaling.
-   Manual read scaling median absolute deviation (`--scaling_mad`): Median absolute deviation to use for manual scaling.
-   Disable event table transmission (`--disable_events`): Flag to disable the transmission of event tables when receiving reads back from the basecall server. If the event tables are not required for downstream processing (e.g. for 1D^2) then it is more efficient to disable them.
-   Read ID whitelist (`--read_id_list`): A filename for a text file containing a whitelist of read IDs (one per line, no whitespace). If this option is specified, only reads which have read IDs that are in the whitelist will be basecalled.
-   Barcoding configuration file (`--barcoding_config_file`): A filename from which to load the barcoding configuration, allowing users to override all barcoding parameters without specifying them at the command line. Defaults to 'configuration.cfg'.
-   Sample sheet (`--sample_sheet`): A filename for a MinKNOW-compatible CSV format sample sheet, containing `flow_cell_id`, `experiment_id` and optionally `barcode`, or `internal_barcode` and `external_barcode`, or `rapid_barcode` and `fip_barcode`, used to identify a particular classification of read.  The `alias` column will then be used by the basecaller to rename the output files and folders based on the other classification values. Note that MinKNOW sample sheets can omit the `flow_cell_id` as long as they contain a `position_id`, but in order to be used with the basecaller, the sample sheet MUST contain a `flow_cell_id`. The basecaller will only barcode against the barcodes specified in the sample sheet. To disable this behaviour, use `--disable_barcode_sample_sheet_restricting`.
-   Load scaling from read files (`--load_scaling_info_from_read_files`): Flag to enable loading scaling offset and scale information from source read files, if it exists.  If this flag is set, the basecaller will use the stored values in the input files instead of computing scaling values for reads.
-   Beam cut (`--beam_cut`): Beam score cutoff for beam search decoding.
-   Beam width (`--beam_width`): Beam width to use in beam search decode.

#### Optimisation

-   Model file (`--dorado_model_path`): A path to a RNN model file to use instead of the model specified in the configuration file.
-   Modified base models (`--dorado_modbase_models`): A list of the RNN modbase model files to use instead of the models specified in the configuration file.
-   Chunk size (`--chunk_size`): Set the size of the chunks of data which are sent to the basecaller for analysis. Chunk size is specified in signal blocks, so the total chunk size in samples will be `chunk_size * event_stride`.
-   Chunk overlap (`--overlap`): The overlap between adjacent chunks, specified in signal blocks. An overlap is required for chunks to be stitched back into a continuous read.
-   Stay penalty (`--stay_penalty`): Scaling factor to apply to stay probability calculation during transducer decode.
-   Q-score offset (`--qscore_offset`): Override the q-score offset to apply when calibrating output q-scores for the read. There is an offset and scale (see `--qscore_scale` below) that are applied to the output base probabilities in the FASTQ for a basecall, to make the q-scores as close as possible to the Phred quality scores. Once a basecall model has been trained, these scores are calculated and added to the config files.
-   Q-score scale (`--qscore_scale`): Override the q-score scale to apply when calibrating output q-scores for the read.
-   Num alignment threads (`--num_alignment_threads`): Number of worker threads to use for alignment.
-   Num barcoding threads (`--num_barcoding_threads`): Number of worker threads to use for barcoding.
-   Num modified base basecaller threads (`--num_base_mod_threads`): The number of threads to use for Remora modified base detection in GPU basecalling mode.
-   Num read splitting threads (`--num_read_splitting_threads`): Number of worker threads to use for read splitting.
-   Num read splitting buffers (`--num_read_splitting_buffers`): Number of GPU memory buffers to allocate to perform read splitting. Controls level of parallelism on GPU for read splitting using mid adapter detection.
-   Disable pings (`--disable_pings`): Flag to disable sending any telemetry information to Oxford Nanopore Technologies. See the "Ping information" section for a summary of what is included in the telemetry.
-   Telemetry URL (`--ping_url`): Override the default URL for sending telemetry pings.
-   Ping segment duration (`--ping_segment_duration`): Duration in minutes of each ping segment.
-   Read batch size (`--read_batch_size`): The maximum batch size, in reads, for grouping input files. This controls the granularity at which resume can operate. Note that this value may be exceeded if individual input files contain more than this many reads. Output files for each batch will be contain a maximum of `--records_per_fastq` entries.
-   Log speed frequency (`--log_speed_frequency`): How often to print out basecalling speed.

### Overriding configuration parameters from the command-line

Configuration files specify many of the optional parameters discussed previously. For example, the basecalling section of a configuration file could look like this:

```
# Basecalling.
dorado_model_path                   = dna_r10.4.1_e8.2_400bps_hac@v4.2.0
chunk_size                          = 2000
runners                             = 20
overlap                             = 50
qscore_offset                       = -0.06
qscore_scale                        = 1.16
```

The parameters specified in the configuration file can be overwritten from the command-line by arguments of the form `--parameter value`, e. g.

```
ont_basecall_client --config dna_r9.5_450bps.cfg --runners 40 [other options]
```

Command-line parameters always take priority over config file parameters, so running the basecaller with these arguments would override the `runners` setting from the config file, forcing it to 40. This facilitates small changes to parameters. Please note that no spaces are allowed in arguments, but the argument can be wrapped in quotes. For example, to run the basecall server with two GPU devices, you would set the devices like so:

```
dorado_basecall_server --device "cuda:0 cuda:1" [other options]
```

# Bioinformatics toolkit

## Barcoding/demultiplexing

### Barcoding/demultiplexing overview

In the ont-dorado-server suite, barcoding can be performed by a separate executable. This allows barcoding to be performed as an offline analysis step without having to re-basecall the source reads. To perform barcoding in this way, invoke the barcoder with the minimum required parameters:

```
ont_barcoder --input_path <folder containing FASTQ and/or FASTA files> --save_path <output folder> --config configuration.cfg
```

When performing barcode detection, `ont_barcoder` will create a barcoding_summary.txt file in the output folder, which contains information about the best-matching barcodes for each read in the FASTQ/FASTA files in the input folder (see the section "summary file contents" in the basecalling section above for details). The output FASTQ/FASTA files will be written into barcode-specific subdirectories for the barcode detected. A log file is also emitted with information about the execution run.

### ont_barcoder supports the following optional parameters:

-   Version (`-v` or `--version`): Prints the version of `ont_barcoder`.
-   Help (`-h` or `--help`): Print a help message describing usage and all the available parameters.

#### Data features

-   Require a barcode on both ends of the read (`--require_barcodes_both_ends`): Option to only classify reads where a barcode has been detected at both the front and rear of the read. This can significantly reduce the number of reads that are classified, and is also not a valid argument for the Rapid kits (which do not have a rear barcode).
-   Allow inferior barcodes to be used in arrangements (`--allow_inferior_barcodes`): Option to still classify reads when the barcode selected at each end of the read was not the highest-scoring barcode detected (assuming one was detected above the minimum score). This can slightly increase the number of reads that are classified but can increase the false-positive rate in classifications.
-   Front window size (`--front_window_size`): Specify the maximum window of the start of the read (in bases) to search for the front barcode in. Default is 150 bases.
-   Rear window size (`--rear_window_size`): Specify the maximum window of the end of the read (in bases) to search for the rear barcode in. Default is 150 bases.
-   Detect mid-strand barcodes (`--detect_mid_strand_barcodes`): Flag option to enable detection of barcodes within the strand. This option can be used to detect abnormal reads such as chimeras. If a mid-strand barcode is detected, the read will be classified as "unclassified".
-   Detect mid-strand adapters (`--detect_mid_strand_adapter`): Flag option to enable detection of adapter sequences within the strand. This option can be used to detect abnormal reads such as chimeras.
-   Minimum score for barcode detection (`--min_score_barcode_front`): Specify the minimum score for barcode detection. Unless a minimum score is also set for rear barcodes, this score will be used for both front and rear barcodes. Default is 60.
-   Minimum score for rear barcodes (`--min_score_barcode_rear`): Specify the minimum score for rear barcodes. Use this if you want to set a different minimum score for rear barcodes than for front barcodes. Default is to use the front barcode minimum.
-   Minimum score for detection of barcode contexts (`--min_score_barcode_mask`): Specify the minimum score to consider a barcode context to be a valid location to search for a barcode.  If set to -1.0, this option is ignored and barcode scoring is performed on a weighted average of the barcode and context score. Default is -1.0.
-   Minimum score for detection of mid-strand barcodes (`--min_score_barcode_mid`): Minimum score to consider a barcode detected mid strand to be considered a valid alignment. Mid-strand barcodes below this threshold will be ignored. Default is 40.0.
-   LAMPore kit (`lamp_kit`): Specify the LAMPore kit to use for detection.  Note that unlike `--barcode_kits`, it is not supported to analyse reads against multiple LAMPore kits simultaneously.
-   Minimum score for detection of LAMP FIP barcodes (`--min_score_lamp`): Specify the minimum score to consider a LAMP FIP barcode to be classified.  Default is 80.0.
-   Minimum score for detection of LAMP FIP barcode masks (`--min_score_lamp_mask`): Specify the minimum score to consider a LAMP FIP barcode context to be a valid location to search for a FIP barcode.  Default is 50.0.
-   Minimum score for detection of LAMP targets (`--min_score_lamp_target`): Specify the minimum score to consider a LAMP target sequence alignment to be classified.  Default is 75.
-   Minimum score for detection of adapters (`--min_score_adapter`): Minimum score for an adapter to be considered a valid alignment.  Default is 60.
-   Minimum score for detection of mid strand adapters (`--min_score_adapter_mid`): Minimum score for a mid-strand adapter to be considered a valid alignment.  Default is 50.
-   Minimum score for detection of primers (`--min_score_primer`): Minimum score for a primer to be considered to be a valid alignment.  Default is 60.
-   Minimum length for detection of LAMP FIP barcode masks (`--min_length_lamp_context`): Specify the minimum length to consider a LAMP FIP barcode context to be a valid location to search for a FIP barcode.  Default is 40.
-   Minimum length for detection of LAMP targets (`--min_length_lamp_target`): Specify the minimum length to consider a LAMP target sequence alignment to be classified.  Default is 80.
-   Additional LAMP barcode context bases (`--additional_lamp_context_bases`): Number of bases from a lamp FIP barcode context to append to the front and rear of the FIP barcode before performing matching. Default is 2.
-   Detect adapter sequences at front and rear of the read (`--detect_adapter`): Enables adapter detection. Default is that this is disabled.
-   Detect primer sequences at front and rear of the read (`--detect_primer`): Enables primer detection. Default is that this is disabled.
-   Enable trimming barcodes (`--enable_trim_barcodes`): Flag to enable trimming of barcodes from the sequences in the output files. If present, detected barcodes will be trimmed from the sequence. See [Barcode Trimming](#barcode-trimming) for more details and related options.
-   Disable filtering of barcodes based on the sample sheet in use (`--disable_barcode_sample_sheet_restricting`): By default if a sample sheet is provided then the barcodes will be filtered to only those in the sample sheet. To disable that behaviour use this flag.

#### Input/output

-   Quiet mode (`-z` or `--quiet`): This option prevents the `ont_barcoder` from outputting anything to stdout. Stdout is short for “standard output” and is the default location to which a running program sends its output. For a command line executable, stdout will typically be sent to the terminal window from which the program was run.
-   Verbose logging (`--verbose_logs`): Flag to enable verbose logging (outputting a verbose log file, in addition to the standard log files, which contains detailed information about the application). Off by default.
-   Recursive (`-r` or `--recursive`): search through all subfolders contained in the `--input_path` value, and perform barcode detection on any FASTQ or FASTA files found in them.
-   Configuration file (`-c` or `--config`): This option allows you to specify a configuration file, which contains details of the parameters used during barcode detection. The default cfg file supplied with `ont-dorado-server` should be sufficient for most users. There is an additional configuration_dual.cfg containing settings for using dual-barcode preparations.
-   Override default data path (`-d` or `--data_path`): Option to explicitly specify the path to use for loading any data files the application requires (for example, if you have created your own model files or config files).
-   Records per FASTQ (`-q` or `--records_per_fastq`): The maximum number of reads to put in a single FASTQ or FASTA file. Set this to zero to output all reads into one file (per run id, per batch). The default value is 4000. See also `--read_batch_size`.
-   Perform FASTQ compression (`--compress_fastq`): Flag to enable gzip compression of output FASTQ/FASTA files; this reduces file size to about 50% of the original.
-   BAM file output (`--bam_out`): This flag enables BAM file output. Default is for BAM file output to be disabled.
-   BAM file indexing (`--index`): This flag enables BAM file indexing.  If the flag is present, `ont_barcoder` sorts the BAM file output and generates the BAI index file. This flag requires that `--bam_out` is also set. Default is for indexing to be disabled.
-   FASTQ file output (`--fastq_out`): This flag enables FASTQ file output.  If neither `--bam_out` or `--fastq_out` is enabled, FASTQ output is enabled by default.
-   Input valid extensions (`--ext_in`): Only files with the specified extensions are processed (comma separated list). If this is not enabled all files with supported extension are processed. Supported extensions are: `.fastq`, `.fq`, `.fasta`, `.fa`, `.sam`, `.bam`. Sequences from a `.sam` or `.bam` file that have been stored as the reverse complement will be reverse complemented before barcoding.
-   Maximum number of reads in flight (`--max_reads_in_flight`): Maximum number of reads that will be held in memory in the barcoder, when this limit is reached no further reads will be input until reads have been output. This helps keep the memory usage to an acceptable level. The default value is 20,000 reads.

#### Optimisation

-   Worker thread count (`-t` or `--worker_threads`): The number of worker threads to spawn for the barcoder to use. Increasing this number will allow `ont_barcoder` to make better use of multi-core CPU systems, but may impact overall system performance.
-   GPU device (`-x` or `--device`): Specify the CUDA-enabled GPU to use to perform barcode alignment. Parameters are specified the same way as in the basecaller application.
-   Limit the kits to detect against (`--barcode_kits`): List of barcoding kit(s) or expansion kit(s) used to limit the number of barcodes to be detected against. This speeds up barcoding. Multiple kits must be a space-separated list in double quotes.
-   Number of parallel GPU barcoding buffers (`--num_barcoding_buffers`): Number of parallel memory buffers to supply to the GPU for barcode strand detection. Greater numbers will increase parallelism on the GPU at an increased memory cost. Default is 24.
-   Number of reads to process in parallel in each GPU barcoding buffer (`--num_reads_per_barcoding_buffer`): The number of reads to process in parallel in each GPU barcoding buffer. Greater numbers will increase parallelism on the GPU at an increased memory cost. Default is 4.
-   Number of parallel GPU mid barcode detection buffers (`--num_mid_barcoding_buffers`): Number of parallel memory buffers to supply to the GPU for barcode mid strand detection. Greater numbers will increase parallelism on the GPU at an increased memory cost. Default is 96.
-   Limit the barcodes to a subset of the kits (`--barcode_list`): Only the barcodes in this space-separated list will be considered when barcoding.
-   Progress stats reporting frequency (`--progress_stats_frequency`): Frequency in seconds in which to report progress statistics, if supplied will replace the default progress display.
-   Trace domains config (`--trace_domains_config`): Configuration file containing list of trace domains to include in verbose logging (if enabled)
-   Disable pings (`--disable_pings`): Flag to disable sending any telemetry information to Oxford Nanopore Technologies. See the "Ping information" section for a summary of what is included in the telemetry.
-   Telemetry URL (`--ping_url`): Override the default URL for sending telemetry pings.
-   Ping segment duration (`--ping_segment_duration`): Duration in minutes of each ping segment.

To see the supported barcoding kits, run the `--print_kits` argument with the barcoder:

```
ont_barcoder --print_kits
```

To limit the kits to detect against:

```
ont_barcoder --input_path <folder containing FASTQ and/or FASTA files> --save_path <output folder> --config configuration.cfg --barcode_kits SQK-RPB004
```

Or for multiple kits add a space-separated list in double quotes:

```
ont_barcoder --input_path <folder containing FASTQ and/or FASTA files> --save_path <output folder> --config configuration.cfg --barcode_kits "EXP-NBD104 EXP-NBD114"
```

Barcoding of dual-barcode arrangements is also supported.  To use dual-barcode arrangements, the correct configuration file must be specified:

```
ont_barcoder --input_path <folder containing FASTQ and/or FASTA files> --save_path <output folder> --config configuration_dual.cfg --barcode_kits "EXP-DUAL00"
```

Note that running barcode detection on dual- and single- barcode kits at the same time is not currently supported. New columns will be emitted into the `barcoding_summary.txt` or `sequencing_summary.txt` when performing demultiplexing of dual barcode kits: `barcode_front_id_inner`, `barcode_front_score_inner`, `barcode_rear_id_inner` and `barcode_rear_score_inner`.

### Barcoding during basecalling

It is also possible to perform barcode detection during the basecalling process. When invoking the `ont_basecall_client` executable, simply provide a valid set of kits to the `barcode_kits` argument to enable barcoding, for example:

```
ont_basecall_client --input_path <folder containing .fast5 or .pod5 files> --save_path <output folder> --config dna_r10.4.1_e8.2_400bps_fast.cfg --port 5555 --barcode_kits SQK-RBK001
```

Note that options such as barcode trimming and demultiplexing output FASTQ/FASTA files are all supported by the `ont_basecall_client` executable as well as `ont_barcoder`. If a barcoding configuration file other than the default configuration.cfg is required, the basecaller executable supports selecting a barcode config using `--barcoding_config_file` command-line option.

### Barcoding FASTQ output

The barcoding executable will output FASTQ/FASTA files into barcode-specific subdirectories in the output folder depending on the barcode that was detected. The FASTQ naming follows the same rules as for basecalling (see Features, settings and analysis – Input and output files). A barcode directory will only exist if the barcode was detected. The output structure will look like this:

```
output_folder/
    | barcoding_summary.txt
--- barcode01/
        | fastq_runid_777_0.fastq
        | fastq_runid_abc_0.fastq
        | fastq_runid_abc_1.fastq
--- barcode03/
        | fastq_runid_777_0.fastq
        | fasta_runid_xyz_0.fasta
--- unclassified/
        | fastq_runid_777_0.fastq
```

### Barcode trimming

The barcoding executable can automatically trim the detected barcodes from the sequence before being output to the FASTQ/FASTA file. This is off by default. To enable barcode trimming add the `--enable_trim_barcodes` argument.:

```
ont_barcoder --input_path <folder containing FASTQ and/or FASTA files> --save_path <output folder> --config configuration.cfg --enable_trim_barcodes
```

Two extra columns will be written into the `barcoding_summary.txt` output: `barcode_front_total_trimmed` and `barcode_rear_total_trimmed`. A barcode will only be trimmed if it is above the `min_score` threshold (default 60), and the aligned sequence that matches to the barcode will be removed from the front and/or rear of the sequence that is then written to the FASTQ/FASTA.

If you want to be more stringent with trimming, there is a `--num_extra_bases_trim` argument, which defaults to 0. Setting this to, for example, 2 would trim the detected barcode sequence plus an extra 2 bases. If you want to be more cautious, give this argument a negative number; for example, -3 would trim 3 fewer bases than was detected as the barcode sequence.

```
ont_barcoder --input_path <folder containing FASTQ and/or FASTA files> --save_path <output folder> --config configuration.cfg --num_extra_bases_trim 2
```

### Expert users - adjusting barcode classification thresholds

The classification threshold has been chosen to produce a low number of incorrect classifications while retaining an acceptable classification rate. You may override this, but note that small changes can have a significant effect on the false-positive rate, so it is important to always test any changes before using them.

To change the threshold used for both the front and rear barcode modify the `--min_score` argument. The following would increase the threshold for barcodes to be classified to 70, so that if either the front or rear barcode has a score of 70 or more the read will be classified:

```
ont_barcoder --input_path <folder containing FASTQ and/or FASTA files> --save_path <output folder> --config configuration.cfg --min_score 70
```

You may also have different front and rear thresholds by also supplying the `--min_score_rear_override` argument. If this is specified, `--min_score` will be used for the front barcode and `--min_score_rear_override` will be used for the rear barcode. For example, in the following a read will be classified if either the front barcode is above the default (which is currently 60), or the rear barcode 55 or more:

```
ont_barcoder --input_path <folder containing FASTQ and/or FASTA files> --save_path <output folder> --config configuration.cfg --min_score_rear_override 55
```

### How barcode demultiplexing works

This is a general outline of how the barcoder works and how you can adjust its classification thresholds.

### The regions of a barcode

A complete barcode arrangement comprises three sections:

-   The upstream flanking region, which comes between the barcode and the sequencing adapter
-   The barcode sequence
-   The downstream flanking region, which comes between the barcode and the sample sequence

A complete dual-barcode arrangement comprises five sections:

-   The upstream flanking region, which comes between the outer barcode and the sequencing adapter
-   The outer barcode sequence
-   The mid flanking region, which comes between the outer barcode and the inner barcode
-   The inner barcode sequence
-   The downstream flanking region, which comes between the inner barcode and the sample sequence

The barcode sequences remain constant across almost all of Oxford Nanopore Technologies' kits. For example, the flanking regions for barcode 10 in the Rapid Barcoding Kit (SQK-RBK114.24) are different from the flanking regions for barcode 10 in the Rapid PCR Barcoding Kit (SQK-RPB114.24), but the barcode sequence itself is the same.

While Native Barcoding kits use the same barcode sequences as other kits, barcodes 1-12 in the Native Barcoding kits are the reverse complement of the standard barcodes 1-12.

Barcode and barcode flanking sequences can be found in the [Chemistry technical document](https://community.nanoporetech.com/technical_documents/chemistry-technical-document/v/v/barcoding-kits) in the Nanopore Community.

### Different barcoding chemistries

While each barcoding chemistry type (e.g. native, rapid, or PCR) will produce barcodes with the pattern described in "The regions of a barcode", there can be variations in the flanking regions within a particular kit. These are referred to as either "forward" and "reverse" variations or "variation 1" and "variation 2" depending on the configuration. When these variations are present the full double-stranded sequence can look like this:

`<barcodeXX_var1---><sample sequence top strand---><barcodeXX_var2_rc>`

`<barcodeXX_var1_rc><sample sequence bottom strand><barcodeXX_var2--->`

The PCR Barcoding Expansion Kit (EXP-PBC001) produces barcodes like the example directly above.

Or like this:

`<barcodeXX_var1><sample sequence top strand---><barcodeXX_var2>`

`<barcodeXX_var2><sample sequence bottom strand><barcodeXX_var1>`

The Native Barcoding Kit 24 V14 (SQK-NBD114.24) produces barcodes like the second example, directly above.

### The barcoding algorithm

The barcoding algorithm uses a modified Needleman-Wunsch method. We modify the Needleman-Wunsch algorithm by adding "gap open" and "gap extension" penalties, as well as separate "start gap" and "end gap" penalties. These penalties and the match / mismatch scores for aligning a barcode to a sequence are detailed in two places:

1. Generic gap penalties are in the barcoding configuration file configuration.cfg, or configuration_dual.cfg for dual-barcode arrangements.
2. DNA-specific match/mismatch scores are stored in the file 4x4_mismatch_matrix.txt. Note that these scores are shifted such that the highest score is 100 – this means that the final barcode score will share the same maximum. There is also a 5x5_mismatch_matrix.txt file which includes the ability to match any cardinal base to a mask base 'N'.

Each barcode is aligned to a section of the basecall, usually the first and / or last 150 bases. This generates a grid of size 150 * < barcode_length >.

The barcoding score for a particular grid is calculated in a two-step process:

1. The score for only the section of the grid that corresponds to the barcode itself is considered. This corresponds to removing the initial gap row and discarding all scores past the alignment of the last base of the barcode, or removing those sections where the "start gap" and "end gap" penalties are applied.

![.](img/Guppy_BC_1.png)

2. The score is normalized by the total length of the barcode sequence. This ensures the final score is no more than the highest score in the mismatch table (which should be 100). Note that this potentially allows for negative scores when there are a relatively high number of gaps and/or mismatches.

### Measuring classification

The classification for a particular barcode is determined by comparing the barcoding score to a fixed classification threshold – scores that exceed the threshold are considered (successful) classifications. The current threshold is set to 60 for single barcode arrangements and 50 for dual barcode arrangements.

Classification for a read is determined by taking the single highest-scoring (successful) barcode classification. This includes both classifications made at the beginning of the sequence and (where applicable) the end. If no classification exists, then the read is considered "unclassified".

### Classification threshold criteria

The classification threshold has been chosen to produce a low number of incorrect classifications while retaining an acceptable classification rate. This means that when a read has been classified as having a particular barcode, that classification will be incorrect a low number of times. Ideally this false-positive rate is around 1 in 1000, though this can be dependent on how well individually-barcoded samples are purified before they are pooled together. Classification rates should be 90% or above for samples with barcodes on both ends.

It is important to note that the above evaluation criteria assume that only reads which pass the quality filters are used. This corresponds to reads which are placed in the "pass" folder after basecalling; generally these will be reads with a mean q-score value greater than 8 to 10, depending on the model used.

### Modifying classification thresholds

It is possible to increase the number of classifications at the cost of the false-positive rate. Small changes to this can have a significant effect on the false-positive rate, so it is important to test any changes to the thresholds before using them.

For example, here is a graph of the number of reads classified for particular binned values of the (best) barcoding score. The data set is a collection of around 200,000 reads barcoded with the Native Expansion kit (EXP-NBD114):

![.](img/Guppy_BC_2.png)

This graph shows that, for example, reads where the best barcode score is around 30 will have about ~95% incorrect classifications. In contrast, for those reads where the highest barcode score is around 95 there will be near 0% incorrect classifications, and we correctly classify around 22,000 reads.

By reducing the threshold by a few points additional correct classifications may be obtained, but the cost in false positive percentage can go up significantly.

The threshold may be changed by modifying the `--min_score` argument, which applies the threshold to both the front and rear barcode. To have different thresholds for the front and rear barcode modify the `--min_score_rear_override` argument to change the rear barcode threshold. In that case the `--min_score` argument will apply to only the front barcode.

### How classifications are reported

When barcodes are loaded into the barcoder for classification, they are loaded in arrangements. An arrangement consists of either:

-   One barcode, when searching for barcodes only at the front of a read.
-   A front barcode and a rear barcode, when searching for barcodes at both ends of a read.

Once the classification for a particular read has been determined (by choosing the single highest-scoring barcode alignment), there may be another barcode in the arrangement corresponding to the other end of the read. The score for this barcode is also retrieved and reported, regardless of its classification – this means the entire arrangement is always reported.

For example, if a barcode arrangement is loaded containing `barcode01_FWD + barcode01_REV` with `barcode01_FWD` matching the front of the read with a score of 90 and `barcode01_REV` matching the rear of the read with a score of 10, then the final reported result will be:

```
front_barcode: barcode01_FWD
front_score: 90
rear_barcode: barcode01_REV
rear_score: 10
```

### Masked barcodes

To improve the performance of barcoding, it is possible to specify a set of barcodes with a common "mask" or context, containing the invariant flanking regions, rather than a full sequence for every barcode.  For example, consider a set of barcodes as follows:

    >BC01
    AAAAGCTATTTT
    >BC02
    AAAACTTCTTTT
    >BC03
    AAAAGAGATTTT
    >BC04
    AAAACGTATTTT

This set can be more compactly be described as follows:

    >CONTEXT
    AAAANNNNTTTT
    >BC01
    GCTA
    >BC02
    CTTC
    >BC03
    GAGA
    >BC04
    CGTA

Here, 'N' is used to signify a masked-off base, which can align to anything.  Now, alignment of the barcode set to a read can be performed in two steps.  First, the single context is aligned against the read:

    >Context            AAAANNNNTTTT
    >Sequence GATTAGATACAAAAGAGATTTTAATAGGCGC

Once this alignment has been performed, the region of the sequence which corresponds to the masked-off barcode area of the context can be extracted.  In this case, that sequence is "GAGA".  This much shorter sequence can then be aligned to each barcode in turn.

By default, an overall score for the alignment is then calculated by taking the alignment score for the barcode and the flanking region, and combining them based upon their relative lengths.  This score is then used for classification.  However, it is possible to specify a `--min_score_mask` command line argument, which allows for the context component and the barcodes themselves to have separate scoring thresholds.  If `--min_score_mask` is used, the barcode context's alignment score must meet this threshold, and the barcode itself must meet the threshold specified by `min_score` in order to be accepted as a potential classification.


## Adding your own barcodes

`ont_barcoder` fully supports the use of custom barcode sequences. It is recommended that this is accomplished by copying one of the existing configuration files and modifying it elsewhere with a text editor.

### Barcoding data files

Barcoding data files are contained in ont-dorado-server's data folder in the "barcoding" subfolder. You can find this folder in the following locations:

On Linux:

- In `/opt/ont/dorado/data` if installing from deb.
- In the `data` folder in the main `ont-dorado-server` directory if installing from archive.

On OS X / macOS:

- In the `data` folder in the main `ont-dorado-server` directory.

On Windows:

- In the `data` folder in the main `ont-dorado-server` directory.

That folder contains the following subfolders and types of files:

    4x4_mismatch_matrix.txt                 the DNA mismatch matrix for aligning barcodes to sequences
    5x5_mismatch_matrix.txt                 the DNA mismatch matrix for aligning barcodes to sequences including a
                                            'N' mask base
    5x5_mismatch_matrix_simple.txt          the DNA mismatch matrix for use with dual barcodes.
    barcodes_masked.fasta                   the full list of all barcode and the flanking region mask sequences
    lamp_targets.fasta                      the full list of all LAMPore kit target sequences
    configuration.cfg                       the configuration file containing parameters used in barcode detection
    barcoding_arrangements/
        barcode_arrs_XXX.toml               the arrangement files for specific barcodes
    barcoding_dual_arrangements/
        barcode_arrs_dual_XXX.toml          the arrangement files for specific dual barcodes
    lamp_arrangements/
        barcode_arrs_lampXXX.toml           the arrangement files for specific LAMPore kit configurations

#### 4x4 mismatch_matrix.txt

A tab-delimited file containing the mismatch penalties for DNA.

#### 5x5 mismatch_matrix.txt

A tab-delimited file containing the mismatch penalties for DNA plus a masking base 'N', which matches against all bases with a score of 90.

#### 5x5 mismatch_matrix_simple.txt

A tab-delimited file containing the mismatch penalties for DNA plus a masking base 'N', which matches against all bases with a score of 90.
This version of the 5x5 mismatch matrix has been optimised for dual-barcoding arrangements.

#### barcoding_arrangements folder
Folder containing barcoding arrangement files

#### barcoding_dual_arrangements folder
Folder containing dual barcoding arrangement files

#### lamp_arrangements folder
Folder containing arrangement files for LAMPore kits

#### example_barcode_arrs_XXX.toml (and example_barcode_arrs_dual_XXX.toml)
A toml formatted arrangement file describing how a particular set of barcode arrangements is configured. It contains the following fields:

    [loading options]
    barcodes_filename = <filename>
    double_variants_frontrear = <true / false>

    [arrangement]
    name = <name of the barcoding arrangement>
    id_pattern = <barcode id pattern>
    compatible_kits = <array of kits>
    first_index = <first barcode number to load>
    last_index = <last barcode number to load>
    kit = <kit name>
    normalised_id_pattern = <"barcode_arrangement" summary file pattern>
    scoring_function = "MAX"
    barcode1_pattern = <pattern to look up front barcode in <barcodes_filename>>
    barcode2_pattern = <pattern to look up rear barcode in <barcodes_filename>>
    mask1 = <mask name to look up front barcode masking region in <barcodes_filename> (optional)>
    mask2 = <mask name to look up rear barcode masking region in <barcodes_filename> (optional)>
    barcode_inner1_pattern = <pattern to look up front inner barcode in <barcodes_filename> when dual barcoding (optional)>
    barcode_inner2_pattern = <pattern to look up rear inner barcode in <barcodes_filename> when dual barcoding (optional)>

#### barcode_arrs_lampXXX.toml

A toml formatted arrangement file describing how a LAMPore arrangement is configured. These are similar to barcoding arrangement files, but support a slightly different set of:

    [loading options]
    barcodes_filename = <filename>
    lamp_targets_filename = <filename containing sequences which should be used as LAMP targets>
    double_variants_frontrear = <true / false>

    [arrangement]
    name = <name of the lamp arrangement>
    id_pattern = <barcode id pattern>
    compatible_kits = <array of kits>
    first_index = <first barcode number to load>
    last_index = <last barcode number to load>
    kit = <kit name>
    normalised_id_pattern = <"barcode_arrangement" summary file pattern>
    scoring_function = "MAX"
    barcode1_pattern = <pattern to look up front barcode in <barcodes_filename>>
    lamp_masks = <An array of mask names look up barcode masking regions in <barcodes_filename>>

These sections are dealt with in reverse order.

##### arrangement

- **id_pattern** : The barcode ID pattern itself is what is used as the base name for each barcode arrangement. It may be modified later depending on what is present in the **loading_options** section (see below). This pattern should have `%0Ni` present somewhere in the name (where `N` is the number of digits to use in the barcode number), as that will be replaced with the barcode number for the arrangement. For example, the pattern `NB%03i` will be formatted to produce barcode arrangement names such as `NB001`, `NB384`, and so forth. The final arrangement name based on this pattern will be reported in the "barcode_full_arrangement" field in the barcoding_summary.txt file.
- **compatible_kits** : A list of kits this set of arrangements is compatible with. These may be selected from the command line to restrict the arrangements that barcodes are matched against.
- **first_index** : The first integer used when loading barcodes from **barcodes_filename**  (see **loading options** below). These integers are used to populate the `%0Ni` parts of the barcode name, normalised_id, barcode1, and barcode2 patterns.
- **last_index** : The last index used (inclusively) when loading barcodes from **barcodes_filename**.
- **kit** : The name reported in the "kit" column of the barcoding summary file.
- **normalised_id_pattern** : The name reported in the "barcoding_arrangement" column of the barcoding summary file. This should contain the %0Ni pattern within it so that the barcode number can be added. This is normally used to report the barcode number without the kit designation.
- **scoring_function** : The function used to score a barcode arrangement. There are two choices for this, though only "MAX" is currently used:
  - **MAX** : The barcode arrangement score is the larger of the front and rear scores.
  - **ADD** : The barcode arrangement score is the sum of the front and rear scores.
- **barcode1_pattern** : Optional pattern used to look up the front barcode sequences in **barcodes_filename**. If this field is not present then no front barcodes will be added during the initial barcode loading step (though it is still possible to obtain front barcodes depending on **loading options** below). Note that the suffix "_FWD" will be added to this barcode name in the arrangement.
- **barcode2_pattern** : Optional pattern used to look up the rear barcode sequences in **barcodes_filename**. Note that the suffix "_REV" will be added to this barcode name in the arrangement, and the barcode inserted into the arrangement will be the reverse complement of the named barcode specified in **barcodes_filename**.
- **mask1** : Optional. Used to look up the front barcode flanking region in **barcodes_filename**.  If this field is used, this masking region will be aligned first, then the **barcode1** sequence for each arrangement will be aligned to the section of the read which corresponds to the masked-off region of this sequence (i.e. the section of 'N' bases).
- **mask2** : Optional. Used to look up the rear barcode flanking region in **barcodes_filename**.  If this field is used, this masking region will be aligned first, then the **barcode2** sequence for each arrangement will be aligned to the section of the read which corresponds to the masked-off region of this sequence (i.e. the section of 'N' bases).
- **barcode_inner1_pattern** : Optional pattern used to look up the front inner barcode sequences in **barcodes_filename**. Note that the suffix "_FWD" will be added to this barcode name in the arrangement.
- **barcode_inner2_pattern** : Optional pattern used to look up the rear inner barcode sequences in **barcodes_filename**. Note that the suffix "_REV" will be added to this barcode name in the arrangement, and the barcode inserted into the arrangement will be the reverse complement of the named barcode specified in **barcodes_filename**.
- **lamp_masks** : A comma seperated list of patterns to look up barcode masking regions in **barcodes_filename**. Note that there can be several of these masks, as they may be different for each target.  The mask will be used to find a context in the sequence to inspect for FIP barcodes.

##### loading options

- **barcodes_filename** : the name of the FASTA file to load barcodes from. It should be in the data/barcoding folder, or the filename should include a relative path from the data/barcoding folder.
- **lamp_targets_filename** : the name of the FASTA file to load LAMPore targets from. It should be in the data/barcoding folder, or the filename should include a relative path from the data/barcoding folder. The targets should be named <target_id>:<specific_sequence_id>.  This allows multiple sequences to map to the same target ID.  Just the target_id will be reported by the detector.
- **double_variants_frontrear** : For each barcode arrangement, create "_var1" and "_var2" variants. The "_var1" variant will be **barcode1** at the front and **barcode2** at the rear, and "_var2" will be **barcode2** at the front and **barcode1** at the rear. This effectively adds a complement for each arrangement.

For example:

| **loading options** | **barcode names expected in barcodes_filename (assuming both barcode1 and barcode2 patterns are present)** | **barcode arrangements added to list to test against ("rc" denotes reverse complement)** <br> \<front_barcode> + \<rear_barcode> |
| --- | --- | --- |
| **double_variants_frontrear** : false | \<barcode1> <br> \<barcode2> | \<barcode1>_FWD + \<barcode2rc>_REV  |
| **double_variants_frontrear** : true | \<barcode1> <br> \<barcode2> | \<barcode1>_var1_FWD + \<barcode2rc>_var2_REV <br> \<barcode2>_var2_FWD + \<barcode1rc>_var1_REV |

###
Quick start

Assume we have created a set of custom barcodes structured like this:

    <barcodeXX---><sample sequence top strand---><barcodeXX_rc>
    <barcodeXX_rc><sample sequence bottom strand><barcodeXX--->

There is one type of barcode, it can be attached on both the top and bottom strand, and it has a reverse complement present on the opposite strand.

Furthermore, assume we have two different barcodes to add. We can call these two barcodes CUST01 and CUST02.

#### Step 1: Copy ont-dorado-server's data folder somewhere else

See "Barcoding data files" above. Assuming a Linux installation is used, this could look something like:

    cp -r /opt/ont/dorado/data ~/mydata

#### Step 2: Create a new arrangements file and a new FASTA file to store the custom barcodes.

Copy one of the arrangements in the barcoding data folder to store the new arrangement in.

    cp ~/mydata/barcoding/barcoding_arrangements/barcode_arrs_nb24.toml ~/mydata/barcoding/barcoding_arrangements/barcode_arrs_cust2.toml

And create a new FASTA file for the custom barcodes:

    touch ~/mydata/barcoding/custom_barcodes.fasta

#### Step 3: Edit the new arrangement file to include information on the new barcode

We have one type of barcode, and arrangements of that barcode will include the barcode at the front and the reverse complement of the barcode at the rear. We don't want to set **double_variants_frontrear** because we have only one variant of the barcode.

So our configuration file barcode_arrs_cust2.toml will look like this:

    [loading_options]
    barcodes_filename = "custom_barcodes.fasta"
    double_variants_frontrear = false

    # ############### My custom barcoding kit ###############

    [arrangement]
    name = "barcode_arrs_cust2"
    id_pattern = "CUST%02i"
    compatible_kits = ["MY-CUSTOM-BARCODES"]
    first_index = 1
    last_index = 2
    kit = "CUST"
    normalised_id_pattern = "barcode%02i"
    scoring_function = "MAX"
    barcode1_pattern = "CUST%02i"
    barcode2_pattern = "CUST%02i"

Note that we set both barcode1_pattern and barcode1_pattern to the same value. This means:

1. We are going to search for barcodes at the rear of the strand (because barcode2 is set).
2. The rear barcodes are based on the same barcodes used in the front.

N.B. If the range of barcode indices includes values greater than 99, ensure that sufficient digits are specified in each of the pattern fields. For example if we have barcodes from 1 to 384 the arrangements section would contain pattern fields containing `%03i`, like this:

    [arrangement]
    name = "barcode_arrs_cust2"
    id_pattern = "CUST%03i"
    compatible_kits = ["MY-CUSTOM-BARCODES"]
    first_index = 1
    last_index = 384
    kit = "CUST"
    normalised_id_pattern = "barcode%03i"
    scoring_function = "MAX"
    barcode1_pattern = "CUST%03i"
    barcode2_pattern = "CUST%03i"


#### Step 4: Add the new barcodes to our FASTA file

Open the "custom_barcodes.fasta" file created during step 2 and add your barcode sequences in with names matching the `CUST%02i` pattern used in the arrangement file:

    >CUST01
    AAAAAAAGCTCGCTCGCTCGAGATTTTTTT
    >CUST02
    AAAAAAACGGTAAATTGGCATTATTTTTTT

#### Step 5: Run ont_barcoder with our new barcodes

    ont_barcoder \
	--input_path <path_to_input_fastq_files> \
	--save_path <path_to_output_directory> \
	--data_path ~/mydata/barcoding \
	--barcode_kits MY-CUSTOM-BARCODES

### Context-specific barcode specification

When specifying a LAMP arrangement, context-specific barcodes are supported.  For example, consider a LAMP configuration file as follows:

    [loading_options]
    barcodes_filename = "barcodes_masked.fasta"
    lamp_targets_filename = "lamp_targets.fasta"
    double_variants_frontrear = true

    # ############### LAMP barcodes ###############

    [arrangement]
    name = "barcode_arrs_lamp_example"
    id_pattern = "LAMP%02i"
    compatible_kits = ["MY_CUSTOM_LAMP_KIT"]
    first_index = 1
    last_index = 8
    kit = "LAMP"
    normalised_id_pattern = "FIP%02i"
    barcode1_pattern = "LM%02i"
    lamp_masks = ["CONTEXT1","CONTEXT2","CONTEXT3"]

Normally, this kit would be expanded to use barcodes `LM01` to `LM08` from the barcodes_masked.fasta, no matter which context is being used.  However there are situations where having a context-specific barcode may be desirable.  If a specific barcode is required to replace `LM01` for `CONTEXT2`, it can be added to the barcodes_masked.fasta as follows:

    >LM01
    ACGTATCTCA
    >LM01:CONTEXT2
    TCGTCTATCT
    >LM02
    ATGCTGCAGA
    ...

When performing LamPORE analysis, FIP barcodes will be looked up as follows: First, if there is a barcode matching `barcode_name:context_name`, that barcode is selected.  Otherwise, selection falls back to `barcode_name`. In this example, `CONTEXT1` and `CONTEXT3` will continue to use the original `LM01` barcode, but `CONTEXT2` will use `LM01:CONTEXT2`.


## Alignment

### Alignment overview

The toolchain provides the `ont_aligner` executable to allow you to perform reference genome alignment on basecalled reads. Alignment is performed against the supplied reference via an integrated minimap2 aligner, full details of which can be found here: [https://github.com/lh3/minimap2](https://github.com/lh3/minimap2). To perform alignment, invoke the `ont_aligner` with the minimum required parameters:

```
ont_aligner --input_path <folder containing input files> --save_path <output folder> --align_ref <reference FASTA>
```

The input path will be searched for input FASTQ, FASTA, SAM and BAM files to perform alignment on. The `align_ref` is used to specify the reference genome. Sequences from a SAM or BAM file that have been stored as the reverse complement will be reverse complemented before alignment in order to ensure the same results are produced when realigning the output file with the same options. When performing alignment, `ont_aligner` creates the following files in the output folder:

-   `alignment_summary.txt`: Contains information about the best-quality alignment result for each read, such as alignment start, end, accuracy, etc. See the section "summary file contents" in the basecalling section above for details.
-   `read_processor_log-\<date and time\>.log`: A log file with information about the execution run.
-   `.sam` or `.bam`: A SAM or BAM file is produced for each corresponding input file located in the input folder. If a successful alignment is found which passes the coverage filter, the SAM/BAM file will contain a CIGAR string representing the alignment. The default alignment coverage required to consider a result successful is 60%. If BAM file output is enabled, BAM files will be sorted by reference ID and then the leftmost coordinate.

The aligner supports the following optional parameters:

-   Version (`--version`): Prints the version of `ont_aligner`.
-   Help (`-h` or `--help`): Print a help message describing usage and all the available parameters.
-   Quiet mode (`-z` or `--quiet`): This option prevents `ont_aligner` from outputting anything to stdout. Stdout is short for “standard output” and is the default location to which a running program sends its output. For a command line executable, stdout will typically be sent to the terminal window from which the program was run.
-   Verbose logging (`--verbose_logs`): Flag to enable verbose logging (outputting a verbose log file, in addition to the standard log files, which contains detailed information about the application). Off by default.
-   Worker thread count (`-t` or `--worker_threads`): The number of worker threads to spawn for the aligner to use. Increasing this number will allow `ont_aligner` to make better use of multi-core CPU systems, but may impact overall system performance.
-   Recursive (`-r` or `--recursive`): search through all subfolders contained in the `--input_path` value, and perform alignment on any .fastq, .fq, .fasta or .fa files found in them.
-   BAM file output (`--bam_out`): This flag enables BAM file output.  If the flag is not present, `ont_aligner` defaults to SAM output.
-   BAM file indexing (`--index`): This flag enables BAM file indexing.  If the flag is present, `ont_aligner` sorts the BAM file output and generates the BAI index file. This flag requires that `--bam_out` is also set. The default is for indexing to be disabled.
-   Minimap options (`--minimap_opt_string`): This flag allows to specify alignment options for the inner minimap2 alignment algorithm, using the same flags and format supported by the `minimap2` program. See [#supported-minimap2-options](Supported minimap2 options) for the list of supported flags.
-   Max records per output file (`-q` or `--records_per_file`): The maximum number of records to put in a single SAM or BAM file. Set this to zero to allow unlimited records per file. N.B. setting to zero will have a performance impact due to holding all the records in memory until writing to disk. The default value is 4000.
-   Perform read filtering based on alignment (`--alignment_filtering`): This flag allows reads to be filtered based on their alignment status.  Reads with alignment results will be written to the pass folder, and unaligned reads to the fail folder.
-   BED file (`--bed_file`): Path to .bed file containing areas of interest in reference genome.  The emitted alignment_summary file will contain a column of `alignment_bed_hits` for the regions of interest.
-   Alignment type (`--align_type`): Specify whether you want full or coarse alignment. Valid values are (auto/full/coarse).
-   Progress stats reporting frequency (`--progress_stats_frequency`): Frequency in seconds in which to report progress statistics, if supplied will replace the default progress display.
-   Trace domains config (`--trace_domains_config`): Configuration file containing list of trace domains to include in verbose logging (if enabled)
-   Disable pings (`--disable_pings`): Flag to disable sending any telemetry information to Oxford Nanopore Technologies. See the "Ping information" section for a summary of what is included in the telemetry.
-   Telemetry URL (`--ping_url`): Override the default URL for sending telemetry pings.
-   Ping segment duration (`--ping_segment_duration`): Duration in minutes of each ping segment.

If the aligner reports more than one possible alignment, only the best one is output. An alignment that covers less than 60% of the read or of the reference will be rejected.

Index files produced by the bwa aligner should also work as an  `align_ref` but are not explicitly supported.

The integrated minimap2 aligner is run with no additional arguments supplied to it - the default values are used for all alignments. It is not possible to modify the arguments at this time.

The minimap library integration Oxford Nanopore uses is available on our GitHub page here: [http://github.com/nanoporetech/ont_minimap2](http://github.com/nanoporetech/ont_minimap2)

### Supported minimap2 Options

The list of flags currently supported by the `--minimap_opt_string` it is possible to run:

```
ont_aligner --minimap_opt_string --help
```

In the list of flags below `NUM` represents an integer in human readable format, i.e. 4000 can be specified as 4k.
The default value for each option is reported in square bracket after its description

- Indexing flags:
  - `-H [ --hpc ]`                      use homopolymer-compressed k-mer (preferrable for PacBio)
  - `-k [ --kmer-size ] INT`            k-mer size (no larger than 28) [15]
  - `-w [ --window-size ] INT`          minimizer window size [10]
  - `-I [ --batch-size ] NUM`           split index for every ~NUM input bases [4G]

- Mapping flags:
  - `-f [ --mid-occ-frac ] FLOAT`       filter out top FLOAT fraction of repetitive minimizers [0.0002]
  - `-g [ --max-gap ] NUM`              stop chain enlongation if there are no minimizers in INT-bp [5000]
  - `-G [ --max-intron-len ] NUM`       max intron length (effective with -xsplice + changing -r) [200k]
  - `-F [ --max-frag-len ] NUM`         max fragment length (effective with -xsr or in the fragment mode) [0]
  - `-r [ --bandwidth ] NUM[,NUM]`      chaining/alignment bandwidth and long-join bandwidth [500,20000]
  - `-n [ --min-count ] INT`            minimal number of minimizers on a chain [3]
  - `-m [ --min-chain-score ] INT`      minimal chaining score (matching bases minus log gap penalty) [40]
  - `-X [ --skip-self-dual ]`           skip self and dual mappings (for the all-vs-all mode)
  - `-p [ --pri-ratio ] FLOAT`          min secondary-to-primary score ratio [0.8]
  - `-N [ --best-n ] INT`               retain at most INT secondary alignments [5]

- Alignment flags:
  - `-A [ --match ] INT`                matching score [2]
  - `-B [ --mismatch ] INT`             mismatch penalty (larger value for lower divergence) [4]
  - `-O [ --gap-open ] INT[,INT]`       gap open penalty [4,24]
  - `-E [ --gap-extension ] INT[,INT]`  gap extension penalty; a k-long gap costs min{O1+k*E1,O2+k*E2} [2,1]
  - `-z [ --z-drop ] INT[,INT]`         Z-drop score and inversion Z-drop score [400,200]
  - `-s [ --min-dp-score ] INT`         minimal peak DP alignment score [80]
  - `-u [ --gt-ag ] CHAR`               how to find GT-AG. f:transcript strand, b:both strands, n:don't match GT-AG [n]

- Input/Output flags:
  - `-L [ --long-cigar ]`               write CIGAR with >65535 ops at the CG tag
  - `-c [ --cg ]`                       output CIGAR in PAF
  - `--cs arg`                          output the cs tag; STR is 'short' (if absent) or 'long' [none]
  - `--MD`                              output the MD tag
  - `--eqx`                             write =/X CIGAR operators
  - `-Y [ --softclip ]`                 use soft clipping for supplementary alignments
  - `-t [ --threads ] INT`              number of threads [1]
  - `-K [ --mb-size ] NUM`              minibatch size for mapping [500M]
  - `-V [ --version ]`                  show version number

- Preset flags:
  - `-x [ --preset ] STR`               preset (always applied before other options; see `man minimap2.1` for details) []
    - `map-pb/map-ont`                  - PacBio CLR/Nanopore vs reference mapping
    - `map-hifi`                        - PacBio HiFi reads vs reference mapping
    - `ava-pb/ava-ont`                  - PacBio/Nanopore read overlap
    - `asm5/asm10/asm20`                - asm-to-ref mapping, for ~0.1/1/5%% sequence divergence
    - `splice/splice:hq`                - long-read/Pacbio-CCS spliced alignment
    - `sr`                              - genomic short-read mapping

- Unsupported flags:
  - `-d [ --dump-index ] FILE`          dump index to FILE []
  - `-a [ --sam ]`                      output in the SAM format (PAF by default)
  - `-o [ --output ] FILE`              output alignments to FILE [stdout]
  - `-R [ --rg ] STR`                   SAM read group line in a format like '@RG\tID:foo\tSM:bar' []


See `man minimap2.1` for detailed description of these and other advanced command-line options.



### Alignment index files

When aligning to large references (>~100Mb) it is recommended to prepare an index file in advance for performance (to avoid generating the index on the fly for each run).

To create a minimap2 index file:

1.  Download and install the minimap2 tool from: [https://github.com/lh3/minimap2](https://github.com/lh3/minimap2)
2.  Run the command:

```
minimap2 <input.fasta> <output.idx> -I 32G
```

`-I 32G` indicates the size of reference in bases before sharding occurs - this should be set to be larger than your reference length.

**Sharding:** In minimap2, by default, infers references greater than 4 Gb are split into 'shards' within the index in order to reduce RAM usage. The strand is then aligned separately against each reference shard which can lead to the aligner returning an incorrect alignment, if the strand aligns to a reference that is not within the first shard.

### File conversion
The toolchain provides the bam_convert executable to convert files between the SAM and BAM formats. To convert a file, invoke bam_convert with the minimum required parameters:

```
bam_convert --input <input file name> --save <output filename>
```

bam_convert can also be used to merge multiple files into one by specifying a directory containing one or more BAM files and using the `--merge` flag:

```
bam_convert --input <input file path> --save <output filename> --merge
```

The input directory will be searched for BAM files, and the contents merged into a single output file.

bam_convert also supports the following optional parameters:

-   Help (`-h` or `--help`): Print a help message describing usage and all the available parameters.
-   Sort (`--sort`): Sort the records in the exported file by reference ID and then the leftmost coordinate.
-   Recursive (`-r` or `--recursive`): When performing a merge, search the input directory recursively for input files.
-   Index (`--index`): Generate an index file for the output BAM file.
-   Merge header (`--merge_headers`): Regenerate IDs for program group and read group tags to prevent clashes. If this option is omitted, bam_convert will use only the headers from the first file to be merged. This option is only valid when `--merge` is also present.

## Calibration strand detection

### Calibration strand detection

The DNA calibration strand (DCS) is a 3.6 kb amplicon of the Lambda phage genome. The calibration strand is added to DNA samples during the DNA repair/end-prep stage of library preparation, and is processed and included in the sample library.

Detection of calibration strands by the basecaller can be used to assess how well basecalling has worked, and to confirm that the sample preparation was successful.

If `--calib_detect` is enabled, the basecaller will attempt to identify and analyse any calibration strands which have been basecalled. It does this by first checking to see if a basecalled strand is approximately the correct length (controlled by `--calib_min_sequence_length` and `--calib_max_sequence_length`). It then aligns the basecalled strand to the calibration strand reference. Successfully aligned reads are placed in the `calibration_strands` folder, and alignment accuracy and identity metrics are added to the `sequencing_summary.txt` file. This can be a useful way of evaluating the quality of a run.

## Modified base calling

It is possible to use the basecaller to identify certain types of modified bases. This requires the use of a specific basecalling model which is trained to identify one or more types of modification. Configuration files for these new models can generally be identified by the inclusion of "modbases" in their name (e.g. `dna_r9.4.1_450bps_modbases_5mc_cg_hac.cfg`). The tokens following "modbases" will generally provide information about the type of modifications that will
be looked for. For example, "_5mc_cg_" indicates that it will look for 5mC modifications in a CG context.

Modified base call results can currently be stored in BAM files. BAM file output (`--bam_out`) will automatically be enabled if a modified base call model is detected in the configuration. It is also possible to extract the raw modified base information from a called read via the client API in C++ or python. Note that to get back modified base information via the client API, move and trace data must be enabled (see the API documentation for more details).

### Raw modified base table format

The raw modified table (as available via the client API) is a two-dimensional array where each row of the table relates to the corresponding base in the associated canonical sequence. For example, the first row of the table (row 0) will correspond to the first base in the canonical basecall sequence.

Each row contains a number of columns equal to the number of canonical bases (four) plus the number of modifications present in the model. The columns list the bases in alphabetical order (ACGT for DNA, ACGU for RNA), and each base is immediately followed by columns corresponding to the modifications that apply to that particular base. For example, with a model that identified modifications for 6mA and 5mC, the column ordering would be A 6mA C 5mC G T.

Each table row describes the likelihood that, given that a particular base was called at that position, that that base is either a canonical one (i.e. a base that the model considers to be "unmodified"), or one of the modifications that is contained within the model. The contents of the table are integers in the range of 0-255, which represent likelihoods in the range of 0-100% (storing these values as integers allows us to reduce .fast5 file size). For example, a likelihood of 100% corresponds to a table entry of 255. Within a given row the table entries for a particular base will sum to 100%.

Following from our previous example with 6mA and 5mC, you might see a table with row entries like these:

```
[63, 192, 0, 0, 0, 0],
[0, 0, 255, 0, 0, 0],
[0, 0, 0, 0, 255, 0],
[0, 0, 0, 0, 0, 255],
```

This would mean that:

-   An A was called for the first base, and the likelihood that it is a canonical A is ~25% (63/192), and the likelihood that it is 6mA is ~75% (192 / 255).
-   A C was called for the second base, and the likelihood that it is a canonical C is 100% (255 / 255), with no chance (0 / 255) of it being a 5mC.
-   A G and then a T were called for the third and fourth bases. The likelihood that they are canonical bases is 100% (255 / 255 -- this should always be the case, as the model does not include any modification states for G or T).

Note that for the current modified base models, the likelihoods will all be 0 for the bases that were not called, since the modification detection is performed after determining the called sequence. This was not the case for previous versions of the software, which used a different method to determine the probabilities.

### BAM file modified base format

If a modified base call model is selected, the basecaller will emit BAM files as if the `--bam_out` flag had been set. Modified bases will be encoded into the BAM modified base format in the metadata tags `MM` and `ML`. For configurations that only look for modifications within a specific context (which is currently the case for all of our suppored modified base configurations), a ? will be used in the MM tag to indicate that the modification probability is unknown for any bases of the specified type that were skipped, and results will only be output for bases that match the context. If any context-free modification configurations are used, then the ? will not appear in the tag, and only instances of the base that exceed the specified threshold will be output. For more information on the BAM modified base format, see the "Base Modifications" section of the SAM optional fields specification here: https://samtools.github.io/hts-specs/SAMtags.pdf

# FAQ and Troubleshooting

## FAQ

### When I run the GPU version of the basecall server I get the message `error while loading shared libraries: libcuda.so.1: cannot open shared object file`.

> This will happen when NVIDIA GPU drivers have not been installed, or have been installed incorrectly. (Re)installing GPU driver packages should solve this.

### I get slightly different results when I run on different platforms or with different GPUs.

> The basecaller should provide completely deterministic and repeatable results for a given platform, operating system, GPU, and GPU driver, but its output may be slightly different if any of those things change. The overall basecall results should be very similar, and in most cases completely identical.

### Can I call short reads with the basecaller?

> Yes, it is possible to call reads as short as 50 bases. Most configurations use scaling algorithms based on the signal of the adapter sequence, and are robust to basecalling reads of any length.

## Troubleshooting

### Memory usage for the basecaller

If the memory requirements for the basecall server exceed available memory on the host machine, or if other computationally-intensive work is performed while the basecaller is running, then `dorado_basecall_server` may run out of memory and crash. If `dorado_basecall_server` fails for this reason the cause may not be directly apparent - the application may either simply crash or it may return a "segmentation fault" or "killed" error. In such cases, either the number of threads should be reduced or other computationally-intensive tasks should be stopped.

### Advanced troubleshooting for crashes

Despite our best efforts, the tools will occasionally crash due to bugs, and being able to diagnose and fix these is very important. This generally involves a two-step process:

1. Provide general configuration information
    This is just information about how you ran the tools. It should include:
    1.  Your software version (find this by running `dorado_basecall_server` with `--version`).
    2.  The full command used to call all executables.
    3.  Any relevant files, such as your configuration file (if a custom one was used), or read files if available.
    4.  Any other information you think is relevant, such as the hardware the basecaller was running on (GPU model, etc).
    5.  If possible, reproduce the crash with tracing enabled and provide these trace files along with any other log files. To do this follow these steps:
        1.  Create a file called trace_config.txt containing the following line:

            `* trace_file`
        2.  Pass the path to this file to the relevant application either using a command line parameter i.e.

            `--trace_domains_config /path/to/trace_config.txt`

            or using an environment variable, i.e.

            `ONT_GUPPY_TRACE_CONFIG=/path/to/trace_config.txt`
        3.  *If using an ont-dorado-server application, this step can be ignored.* If using the client lib as opposed to a `ont-dorado-server` application the save folder for output trace will need to be set using an environment variable, i.e.

            `ONT_GUPPY_TRACE_FOLDER=/folder/to/output/trace/files/`
        4.  Rerun the application to reproduce the error.
        5.  Any generated trace and logging files will be written to the save folder.
        6.  **N.B. Remove the trace_config.txt file the command line parameter and any environment variables.** This will prevent the application continuing to fill up the hard disk with unnecessary trace files.

2. Attempt to isolate the read which caused the crash
    Crashes may be due to a single read, and figuring out which read caused the crash will make it much easier to reproduce it. Do that like this:
    1.  If you're outputting reads to subfolders, check your `ont_basecall_client_\<timestamp\>.log` file to see which subfolder the client was writing to when it crashed. Any problem reads are likely in this folder.
    2.  Run the same command again (on just the affected subfolder if possible), enabling verbose logging
    3.  Wait for the crash to happen again.
    4.  Look in your log file for the last read which was sent to the basecaller (it will probably not have a "finished processing" message present in the log).
    5.  Run the basecaller again with **only** that one read, and see if it crashes. If it did, you've found the problem read and can send it to customer services.
    6.  If the basecaller did not crash, try again with the last few reads listed in the log file, as the basecaller may be processing several reads in parallel (especially while running on GPU).
