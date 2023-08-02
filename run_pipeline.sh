#!/bin/bash

#SBATCH -J renseq_mapping
#SBATCH -p long
#SBATCH -c 1
#SBATCH --mem=8G
#SBATCH --export=ALL
#SBATCH -o renseq_mapping.%j.out
#SBATCH -e renseq_mapping.%j.err

source activate snakemake

snakemake --conda-frontend conda --profile ~/.config/snakemake/slurm