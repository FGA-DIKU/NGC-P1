#!/bin/bash
#PBS -A MyName
#PBS -N TestJob
#PBS -l nodes=1:ppn=6:gpus=1
#PBS -l mem=5gb
#PBS -l walltime=3:00:00
#PBS -o /users/people/YOURNAMEHERE/$PBS_JOBID.log
#PBS -j oe

cd $PBS_O_WORKDIR

module load cmake/3.22.2
module load miniconda3/4.12.0
conda activate MyEnv

python3 myscript.py
