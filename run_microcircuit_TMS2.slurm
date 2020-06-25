#!/bin/bash
#
#SBATCH -p wmglab
#SBATCH -o run3.out
#SBATCH -e run3.err
#SBATCH --job-name=run
#SBATCH --nodes=1
#SBATCH -n 36
#SBATCH --mem=50G
#SBATCH --mail-type=END,FAIL

module load Anaconda3/3-2019
#module load Anaconda2/2.7.13
module load OpenMPI/2.0.3
module load Neuron/7.7-python3 # uses anaconda3/python3 for nrnpython
#module load Neuron/7.7 # uses anaconda2/python2.7 for nrnpython

mpiexec -n 36 nrniv -python -mpi run_esser_TMS.py
