elegansNet is a simulator for C. elegans whole neural network (302 neurons). Whole code structure and single scripts function can be checked in the outline of "simulator.jpg". Two scripts are not implemented in the simulator but they could be used in the future: chemicalWorm.py, electricalWorm.py. They should be updated and be like mainWormGraded.py but forcing the algorithm just to use chemical or electrical connections respectively. Another script is implemented but not explained in outline is rasterPlot.py, this allow us to have a quick picture of how the simulation worked and is implemented directly in the initial script (__init__.py) once the simulation has finished. 

If we want to run the code, we will need python 3.7.1. The first script we need to check is __Init__.py, here we have different types of simulation to run:
- "activity simulation" for standard simulations.
- "activity compose" to gather simulated activity to export to Granger Causality pipelines.
- "parameter testing" to gather specific variables measures that allowed us to characterize the simulators dynamics. 
To choose between them comment/uncomment the code.

For each simulation type there are several parameters to set:
- RI: random initial activity, determines the percentage of sensors that will be activated at the start of the simulation
- c: synaptic efficacy coefficient, determines the strength of connections between neurons. 
- att: attenuation coefficient, determines the amount of attenuation in terms of synaptic adaptation.
- Psens: probability of sensor stimulation, determines the probability of sensory inputs each 4 timesteps.
To get more information about why each of the parameters are implemented, go to check the dissertation in main directory elegansProject. 

If we run a standard simulation, once executed we will obtain a representation of the simulation in 2D and 3D, in the folder "output". By default this representations should be colour coded by activity and cell type, but this can be changed commenting/uncommenting specific parts of plotting2D.py and potting3D.py scripts. 



FOLDERS.

- "output" include simulations' representations.
- "data" include all the information needed to set up the network before simulating. 
