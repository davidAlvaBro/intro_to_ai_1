#!/bin/sh
#BSUB -J geneate_stats_turning_king
#BSUB -R "rusage[mem=2GB]"
#BSUB -n 2
#BSUB -R "span[hosts=1]" 
#BSUB -o generate_stats_turning_king%J.out
#BSUB -e generate_stats_turning_king%J.err
#BSUB -W 23:00
# -- end of LSF options --

source env/bin/activate

python game_engine/generate_stats.py
