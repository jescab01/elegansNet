#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 17:33:34 2019

@author: jescab01
"""

def standardInit():
    
    from _simulation_ import simulation, representation
    
    
    ### Define simulation variables
    
    timesteps = 2
    sim_no = 2
    refractoryPeriod=1
    
    ratioRandomInit=0.15  # ratio of active nodes from random function (e.g. if random() < 0.2 --> activate node).
    c=0.45  # free parameter influence of weights [exin*(100*c)*weight]
    
    ##### Sensor stimulation parameters. (Go to data/sensoryNeuronTable1.jpg to choose rational combinations)
    area=[] ## Area: 'head', 'body', 'tail'. 
    LRb=[] ## LRb: 'L' (left), 'R' (right), 'b' (body).
    sensor=[] ## Sensor: 'oxygen', 'mechanosensor', 'propioSomatic', 'propioTail', 'propioPharynx',
             ## 'propioHead', 'chemosensor', 'osmoceptor', 'nociceptor', 'thermosensor', 'thermonociceptive'. 
    
    
    
    G, masterInfo, simInitActivity, hopcountdata = simulation(timesteps, sim_no, refractoryPeriod, 
                                                                                 ratioRandomInit, c, area, LRb, sensor)
    representation(G, masterInfo, sim_no, timesteps, simInitActivity, hopcountdata)
    
    return masterInfo, simInitActivity, hopcountdata
    
    
def paramTestInit():
    
    from _simulation_ import simulation
    
    
    ### Define simulation variables
    timesteps = 50
    sim_no = 100
    refractoryPeriod=1
        
    ##### Sensor stimulation parameters. (Go to data/sensoryNeuronTable1.jpg to choose rational combinations)
    area=[] ## Area: 'head', 'body', 'tail'. 
    LRb=[] ## LRb: 'L' (left), 'R' (right), 'b' (body).
    sensor=[] ## Sensor: 'oxygen', 'mechanosensor', 'propioSomatic', 'propioTail', 'propioPharynx',
             ## 'propioHead', 'chemosensor', 'osmoceptor', 'nociceptor', 'thermosensor', 'thermonociceptive'. 
             
             
    ratioRandomInit=[0.05, 0.1, 0.15, 0.2]  # ratio of active nodes from random function (e.g. if random() < 0.2 --> activate node).
    
#    lista=list(range(0,100,5))  # free parameter influence of weights [exin*(100*c)*weight]
#    c=[x/100 for x in lista]    ## c=[0.05, 0.1, 0.15 ..... 0.9, 0.95]
    c=[0.05,0.1,0.11,0.12,0.13,0,14,0.15,0.16,0.17,0.18,0.19,0.2,0.21,0.22,
       0.23,0.24,0.25,0.255,0.26,0.265,0.27,0.275,0.28,0.285,0.29,0.295,
       0.3,0.305,0.31,0.315,0.32,0.325,0.33,0.335,0.34,0.345,0.35,0.355,
       0.36,0.37,0.38,0.39,0.4,0.41,0.42,0.43,0.44,0.45,0.46,0.47,0.48,0.49,
       0.5,0.525,0.55,0.6,0.7,0.8,0.9]
    
    paramTest={}
    
    for a in ratioRandomInit:
        paramTest[a]={}
        for b in c:
            G, masterInfo, simInitActivity, hopcountdata=simulation(timesteps, sim_no, 
                                                                    refractoryPeriod, a, b, area, LRb, sensor)
            paramTest[a][b]=masterInfo['mainInfo']['deactivated']
            
            
    return paramTest


'''

Launcher

'''

## standard simulation Launcher

#masterInfo, simInitActivity, hopcountdata = standardInit()

## paramTest Launcher
from exports import exportParamTest, clearParamTestfolders

paramTestDic={}

for i in range(10):
    paramTest=paramTestInit()
    name='paramTest'+str(i)
    paramTestDic[name]=paramTest

clearParamTestfolders()
exportParamTest(paramTestDic)
            
            
            