#!/bin/bash
#SBATCH --job-name=collocations
#SBATCH --account=project_2003685
#SBATCH --partition=medium
#SBATCH --time=01:00:00
#SBATCH --nodes=18

srun python3 corpus_parser.py