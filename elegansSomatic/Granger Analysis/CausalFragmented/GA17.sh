#!/bin/sh
# Grid Engine options (lines prefixed with #$)
#$ -N GA17          
#$ -cwd                  
#$ -l h_rt=150:00:00 
#$ -l h_vmem=16G
#  These options are:
#  job name: -N
#  use the current working directory: -cwd
#  runtime limit of 5 minutes: -l h_rt
#  memory limit of 1 Gbyte: -l h_vmem

# Initialise the environment modules
. /etc/profile.d/modules.sh
 
# Load matlab
module load matlab/R2018a

# Run the program
./CausalTest17A
