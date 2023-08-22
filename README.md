# RenSeq association mapping pipeline

This is a small pipeline that simplifies the RenSeq association mapping protocol.

## Prerequisites 

This pipeline utilises [snakemake](https://snakemake.readthedocs.io/en/stable/) to handle all the data analysis.
To easily handle this, a base environment `snakemake-env.yaml` has been provided with all required dependencies.
To create this, run the following command:

```
conda env create -f snakemake-env.yaml
```

*If you are running this on a shared resource e.g., the Crop Diversity HPC, please do this in a `srsh` job. It can take >16GB memory to build this environment*

This will create an environment `snakemake` which should have everything you need installed.
It is automatically activated in the run_snakemake.sh script.
This pipeline was designed to run in a [SLURM environment](https://slurm.schedmd.com/documentation.html).
To allow snakemake to interact with the SLURM job manager to submit jobs, you'll need to use [cookiecutter](https://github.com/cookiecutter/cookiecutter).
This will allow you to build a job template which snakemake will use to wrap around each rule allowing it to be submitted as a SLURM job.
To build a profile suitable for SLURM, run the following commands:

```
# Activate the snakemake environment
conda activate snakemake

# Create a snakemake directory in user config
mkdir -p ~/.config/snakemake

cd ~/.config/snakemake

# This will run the setup for the profile - the default settings should be fine, they can always be changed later if necessary!
cookiecutter https://github.com/Snakemake-Profiles/slurm.git
```

## Configuration

To run the pipeline, you will first need to create an experiment `.yaml` template.
This is just a text file with the desired parameters.
Here is an example:

```
experiment_name: myexperiment
parent:
  resistant:
    name: cool_resistant_plant
    R1: path/to/cool_resistant_plant_R1_001.fastq.gz
    R2: path/to/cool_resistant_plant_R1_002.fastq.gz
  susceptible:
    name: ugly_susceptible_plant
    R1: path/to/ugly_susceptible_plant_R1_001.fastq.gz
    R2: path/to/ugly_susceptible_plant_R2_001.fastq.gz
bulk:
  resistant:
    R1: path/to/bulk_resistant_R1_001.fastq.gz
    R2: path/to/bulk_resistant_R2_001.fastq.gz
  susceptible:
    R1: path/to/bulk_susceptible_R1_001.fastq.gz
    R2: path/to/bulk_susceptible_R2_001.fastq.gz
reference:
  name: nice_reference
  fasta: path/to/reference.fa
allele_frequency:
  parent:
    susceptible:
      min: 95
      max: 100
    resistant:
      min: 0
      max: 5
  bulk:
    susceptible:
      min: 95
      max: 100
    resistant:
      min: 40
      max: 60
bowtie2_args: "--score-min L,-0.18,-0.18 --phred33 --fr --maxins 1000 --very-sensitive --no-unal --no-discordant"
```

I recommend that you provide full paths rather than relative paths.
The allele frequencies can be adjusted as desired - the reciprocal allele frequencies are handled automatically.
You can either leave the `bowtie2_args` as is or modify them.
The arguments above are suitable for analysis at a 3% mismatch rate.

## Running the pipeline

To run the pipeline:

`sbatch run_pipeline <experiment.yaml>`

This will submit the job to the SLURM system.
To monitor the status of your analysis, check out the `.err` and `.out` files produced by the `sbatch` job.
It should take <6 hours to run.
Results will be under the `results/` directory!