#!/bin/sh
# Grid Engine options (lines prefixed with #$)
#$ -N Models          
#$ -cwd                  
#$ -l h_rt=24:00:00 
#$ -l h_vmem=10G
#  These options are:
#  job name: -N
#  use the current working directory: -cwd
#  runtime limit : -l h_rt
#  memory limit of 1 Gbyte: -l h_vmem

# Initialise the environment modules
. /etc/profile.d/modules.sh
 
# Load matlab
module load matlab/R2018a

# Run the program
./demo_sim
