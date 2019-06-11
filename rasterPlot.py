#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 31 12:35:29 2019

@author: jescab01

Rasterplot
"""

def rasterPlot(Activity, envActivation):
    
    import matplotlib.pyplot as plot
    import numpy as np
    
    timesteps, neurons = Activity.shape
    neuraldata=Activity.transpose()
    neuraldata=neuraldata.values
    
    dataRaster=neuraldata[:,1]*0
    
    for col in range(1,timesteps):
        a=neuraldata[:,col]*col/timesteps
        dataRaster=np.c_[dataRaster, a]

#    # Set different colors for each neuron
#    
#    colorCodes = np.array([[0, 0, 0],
#    
#                            [1, 0, 0],
#    
#                            [0, 1, 0],
#    
#                            [0, 0, 1],
#    
#                            [1, 1, 0],
#    
#                            [1, 0, 1],
#    
#                            [0, 1, 1],
#    
#                            [1, 0, 1]])
#    
#                           
#    
#    # Set spike colors for each neuron
#    
#    lineSize = [0.4, 0.3, 0.2, 0.8, 0.5, 0.6, 0.7, 0.9]  
    
    plot.eventplot(dataRaster)
    plot.xlabel('Spike')
    plot.ylabel('Neuron')
    plot.show()