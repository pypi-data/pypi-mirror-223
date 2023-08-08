- [detecting Translation Error Landscape: deTEL](#detecting-translation-error-landscape-detel)
  - [deTEL Python package](#detel_python_package) 
- [empirical Translation Error Landscape: eTEL](#empirical-translation-error-landscape-etel)
  - [Requirements](#requirements)
  - [Build ```eTEL```  docker container](#build-etel--docker-container)
  - [Build ```eTEL``` singularity file](#build-etel-singularity-file)
  - [Run ```eTEL``` docker](#run-etel-docker)
    - [open_search](#open_search)
    - [detect_substitutions](#detect_substitutions)
    - [create_dataset_report](#create_dataset_report)
    - [create_report](#create_report)
  - [Run ```eTEL``` singularity](#run-etel-singularity)
    - [Changing Singularity default directories](#changing-singularity-default-directories)
- [multinomial Translation Error Landscape: mTEL](#multinomial-translation-error-landscape-mtel)
  - [Command line options](#command-line-options)
  - [Examples](#examples)
    - [Normal run](#normal-run)
    - [Bootstrapping datasets](#bootstrapping-datasets)

# detecting Translation Error Landscape: deTEL 
deTEL is a simple pipeline that allows for the exploration of translation errors in mass-spectrometry data.
deTEL consists of two components:
eTEL detects translation errors in mass-spectrometry data and explores the empirical translation error landscape.
mTEL is a model fitted to the translation errors detected by eTEL and describes the multinomial translation error landscape and extends the empirical translation error landscape.

## deTEL Python package
```bash
pip install deTELpy

python -m deTEL mTEL # To run mTEL

python -m deTEL eTEL # To run eTEL
```

# empirical Translation Error Landscape: eTEL 
![empirical Translation Error Landscape (eTEL)](img/eTEL.png)
eTEL detects the empirical translation error landscape by first performing an open search using MSFragger [(see: Perform open search)](#perform-open-search-with-fragger_open_search).
The second step is to extract translation errors using custom pythons scripts packaged [(see: detect_substitutions)](#detect_substitutions).
The output of eTEL can directly be used to fit the mTEL model [(see: multinomial Translation Error Landscape: mTEL)](#multinomial-translation-error-landscape-mtel).

## Building eTEL

### Requirements
eTEL requires fragpipe, philosopher, and MSFragger. 
- Download and copy fragpipe into the eTEL folder
within the fragpipe folder, philosopher and MSFragger are expected to be placed into the fragpipe/tools folder:
- Download and copy philosopher into fragpipe/tools folder
- Download and copy MSFragger into fragpipe/tools folder

### Build ```eTEL```  docker container

You can use a [build script](eTEL/build_docker.sh) for building the docker container.
You can push the completed container to your own docker hub repository if desired.
The repoitory can be set by modifying the [build script](eTEL/build_docker.sh).
The build script uses an ```env``` file in order to check all the dependencies. All the dependencies have to be defined before building a container.

```bash
eTEL $ chmod u+x build_docker.sh
eTEL $ ./build_docker.sh
```

This script then generates a docker container in the '''eTEL''' folder and optionally pushes the container to the specified repository. 


### Build ```eTEL``` singularity file

Many computer clusters do not support docker containers, but instead use singularity. You can create a singularity file from the ```eTEL``` docker container.

> Singularity does not use ```root``` for running the process. Changing permission is necessary.

We provide a [build script](eTEL/build_singularity.sh) to create a singularity file. The build script uses the same ```env``` file for checking all the dependencies.
The [build script](eTEL/build_singularity.sh) generates a docker archive file ```etel.tar``` which is then used for generating the singularity file. This script generates ```eTEL.sif```.

```bash
eTEL $ chmod u+x build_singularity.sh
eTEL $ ./build_singularity.sh
```

## Run ```eTEL``` docker
Docker containers require you to `mount` input and output folders into the docker container in order to interact with local data. 
In order to specify a folder to be mounted e.g. the output folder we want to write any results to, we use the `-v` option.

```bash
$ docker run --rm -v output_on_machine:/output
```

```eTEL``` expects to find an `\input` and a `\output` folder

```eTEL``` performes multiple operations.
- [open_search](#open_search) (Required) Detecting mass-shifts in mass-spectrometry data which are either associated with post translational modifications or amino acid substitutions.
- [detect_substitutions](#detect_substitutions) (Required) Remove mass-shifts associated with post translational modifications and retain mass-shifts that can only be explained by amino acid substitutions.
- [create_dataset_report](#create_dataset_report) (Optional) create data set-specific report of detected amino acid substitutions.
- [create_report](#create_report) (Optional) Summarize multiple reports created by [create_dataset_report](#create_dataset_report) into a global report.

### open_search

* -d: Fasta file of protein sequences located in /input (sub)folder
* -c: The number of threads
* -r: Input folder containing multiple raw files.
* -p: output folder name (created within the input folder)

For example, to process all raw files found in '/input/data/PXD000161' and store the results in the same directory in a subfolder 'open_search':
```bash
$ docker run --rm -v local_output:/output -v local_input:/input etel open_search -d /input/fasta/species_cds_aa_decoys.fasta -r /input/data/PXD000161/ -p open_search
```

The memory size and the number of cores can be changed according to the system:
* --memory=32g:   32GB memory
* --cpus=10:      10 cores
```bash
$ docker run --rm --memory=32g --cpus=10 -v local_output:/output -v local_input:/input etel open_search -d /input/fasta/species_cds_aa_decoys.fasta -c 10 -r /input/data/PXD000161/ -p open_search
```

### detect_substitutions

* -d: Fasta file of coding sequences located in /input folder.
* -r: Input folder containing multiple raw files.
* -s: Result folder within the input folder, e.g. as specified by -p in open_search step
* -o: Output folder name, e.g. results

For example, this will look for open-search results in '/input/data/PXD000161/open_search' and store the substitution detection results in 'results':
```bash
$ docker run --rm -v local_output:/output -v local_input:/input etel detect_substitutions -d /input/fasta/species_cds.fasta -s open_search -r /input/data/PXD000161/ -o results
```

### create_dataset_report

* -r: Input folder containing multiple raw files
* -s: Result folder within the input folder, e.g. as specified by -p in open_search step
* -o: Output folder name, e.g. results

```bash
$ docker run --rm -v local_output:/output -v local_input:/input etel create_dataset_report -s open_search -r /input/data/PXD000161/ -o results
```

### create_report
* -d: Fasta file with coding sequences
* -s: Output folder of the substitution tasks. e.g. results

```bash
$ docker run --rm -v local_output:/output -v local_input:/input etel create_report -d /input/fasta/species_cds.fasta -s results
```

## Run ```eTEL``` singularity
The singularity file can be used in a similar manner to the docker container. Important to note is that the `mounting` of local data is using the `--bind` option.

```bash
$ singularity run --writable-tmpfs --bind local_output:/output --bind local_input:/input eTEL.sif open_search -d /input/fasta/species_cds_aa_decoys.fasta -r /input/data/PXD000161/ -p open_search
```

```bash
$ singularity run --writable-tmpfs --bind local_output:/output --bind local_input:/input eTEL.sif detect_substitutions -d /input/fasta/species_cds.fasta -s open_search_ionquant -r /input/data/PXD000161/ -o results
```

```bash
$ singularity run --writable-tmpfs --bind local_output:/output --bind local_input:/input eTEL.sif create_dataset_report -s open_search_ionquant -r /input/data/PXD000161/ -o results
```

```bash
$ singularity run --writable-tmpfs --bind local_output:/output --bind local_input:/input eTEL.sif create_report -d /input/fasta/species_cds.fasta -s /output/results
```

### Changing Singularity default directories
You can override Singularity's default temporary and cache directories by setting these environment variables before running singularity:

 * ```SINGULARITY_CACHEDIR```: the directory where singularity will download (and cache) files
 * ```SINGULARITY_TMPDIR```: the directory where singularity will write temporary files including when building (squashfs) images

For example, to tell singularity to use your scratch space for its cache and temporary files, one might run:

```bash
$ mkdir -p /scratch/$USER/singularity/{cache,tmp}
$ export SINGULARITY_CACHEDIR="/scratch/$USER/singularity/cache"
$ export SINGULARITY_TMPDIR="/scratch/$USER/singularity/tmp"
```

before running singularity. 

# multinomial Translation Error Landscape: mTEL
![<multinomial Translation Error Landscape (mTEL)](img/mTEL.png)
mTEL uses observed translation errors to estimate a multinomial translation error landscape.
mTEL is based on the competition of tRNAs and estimates affinity parameters between codon/anticodon pairs.

## Command line options
* -f: Folder with codon_count and error files.
* -r: tRNA count file.
* -o: Output folder.
* -s: Number of samples of the chain.
* -p: Number of posterior samples.
* -c: Cell volume assumed (in cubic micrometers), Default: 4.2e-17 (approximate size of a yeast cell).
* -t: Number to thin out chain by.
* -b: Number of burn-in steps.
* -nb: Number of sub-samplings performed.
* -os: suffix added to output files (default: date).
* -a: aggregate all datasets by summation (y,n) Default: No (n).

## Examples

### Normal run
We assume that the folder ```ecoli``` contains all needed pairs of ```*_codon_counts.csv``` and ```*_substitution_errors.csv``` files.
A cell volume of 0.6e-18 is assumed for E. coli. We will collect 1000 samples after disgarding 1000 burn-in samples. 
In total, this run will perform (1000 + 1000) * 10 = 20000 steps. The last 200 samples will be used to estimate the posterior distributions of the indivisual parameters.
```bash
$ python3 mTEL/mTEL.py -f ecoli -r tRNA_count/ecoli_tRNA_count.csv -c 0.6e-18 -o output/ecoli/ -s 1000 -p 200 -t 10 -b 1000
```

### Bootstrapping datasets
We can bootstrap datasets as they can show a high variability. This allows us to explore parameter sensitivity and robustness.
This run perfomes 20 resamplings with replacement of the datasets found in the folder ```yeast```, keeping the number of datasets constant.
For each resampling, the model will collect 250 samples after 10 burn-in steps and perform a total of (250 + 10) * 20 = 5200. The last 100 samples of each run will be used to estimate the posterior mean.
```bash
$ python3 mTEL/mTEL.py -f yeast -r tRNA_count/yeast_tRNA_count.csv -c 4.2e-17 -o output/yeast/ -s 250 -p 100 -t 20 -b 10 -nb 20
```

