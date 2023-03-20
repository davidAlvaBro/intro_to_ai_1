#!/bin/sh
#BSUB -J geneate_stats_2_
#BSUB -R "rusage[mem=4GB]"
#BSUB -n 2
#BSUB -R "span[hosts=1]" 
#BSUB -o geneate_stats_2_%J.out
#BSUB -e geneate_stats_2_%J.err
#BSUB -W 07:00
# -- end of LSF options --

source env/bin/activate
# module load python3/3.10.7
# module load numpy/1.23.3-python-3.10.7-openblas-0.3.21

python game_engine/generate_stats.py
