#!/bin/bash

#SBATCH -J renseq_mapping
#SBATCH -p long
#SBATCH -c 1
#SBATCH --mem=8G
#SBATCH --export=ALL
#SBATCH -o renseq_mapping.%j.out
#SBATCH -e renseq_mapping.%j.err

# Check if exactly one argument is provided
if [ "$#" -ne 1 ]; then
    echo "Oopsie-doodle! It seems you forgot to provide the 'experiment-yaml' file."
    exit 1
fi

# Check if the provided file exists
if [ ! -f "$1" ]; then
    echo "Oh snap! The file '$1' seems to have gone for a walk. Can't find it anywhere."
    exit 1
fi

# Check if the provided file has a .yaml extension
if [[ ! "$1" =~ \.yaml$ ]]; then
    echo "Huh, really? The file extension should be '.yaml'. I'm picky like that."
    exit 1
fi

micromamba run -n snakemake snakemake --profile ~/.config/snakemake/slurm --configfile $1

echo """
   _____  ____   ____  _____  ______     ________ 
  / ____|/ __ \ / __ \|  __ \|  _ \ \   / /  ____|
 | |  __| |  | | |  | | |  | | |_) \ \_/ /| |__   
 | | |_ | |  | | |  | | |  | |  _ < \   / |  __|  
 | |__| | |__| | |__| | |__| | |_) | | |  | |____ 
  \_____|\____/ \____/|_____/|____/  |_|  |______|
   
"""