#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 18:11:03 2019

@author: jescab01
"""

## Mantain network activity by randomly activating sensors  
def randomSensInput(G, Psens, sim, envActivation, timestep):
    import random
    
    sens={'propioPharynx':{'L':['n0','n2','n11','n15','n18'],
                           'R':['n1','n3','n12','n16','n19'],
                           'b':['n4','n6','n7']}}
          
    
    if random.random() < 0.3:
        envActivation[sim]['active'].append(timestep)
        for group, subG in sens.items():            ### Define dictionary to use   
            if random.random() < 0.3:
                envActivation[sim]['activeG'].append(str(timestep)+group)
                for subgroup, nodes in subG.items():
                    if random.random() < 0.6:
                        envActivation[sim]['activeSG'].append(str(timestep)+group+subgroup)
                        for node in nodes:
                            if random.random() < 0.8:
                                G.node[node]['mV']=-30
                                envActivation[sim]['activeNode'].append(str(timestep)+group+subgroup+node)
                                
    return envActivation