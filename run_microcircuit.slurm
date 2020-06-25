#!/bin/bash
#
#SBATCH -p wmglab
#SBATCH -o run.out
#SBATCH -e run.err
#SBATCH --job-name=run
#SBATCH -c 36
#SBATCH --mem=50G
#SBATCH --mail-type=END,FAIL

module load Anaconda3/3-2019
#module load Anaconda2/2.7.13
module load OpenMPI/2.0.3
module load Neuron/7.7-python3 # uses anaconda3/python3 for nrnpython
#module load Neuron/7.7 # uses anaconda2/python2.7 for nrnpython

mpiexec -n 36 nrniv -python -mpi esser_microcircuit_inonly.py
