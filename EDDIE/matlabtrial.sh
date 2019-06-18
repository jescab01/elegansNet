#!/bin/sh
# Grid Engine options (lines prefixed with #$)
#$ -N trial            
#$ -cwd                  
#$ -l h_rt=02:00:00 
#$ -l h_vmem=15G
#  These options are:
#  job name: -N
#  use the current working directory: -cwd
#  runtime limit of 5 minutes: -l h_rt
#  memory limit of 1 Gbyte: -l h_vmem

# Initialise the environment modules
. /etc/profile.d/modules.sh
 
# Load matlab
module load matlab

# Run the program
./demo_sim
