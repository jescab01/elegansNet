#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 17:33:34 2019

@author: jescab01
"""

def standardInit():
    from _simulation_ import simulation, representation
    ### Define simulation variables
    timesteps = 25
    sim_no = 2
    hpV=-80
    ratioRandomInit=0.1  # ratio of active nodes from random function (e.g. if random() < 0.2 --> activate node).
    c=1.5  # free parameter influence of weights [exin*(100*c)*weight]
    ##### Sensor stimulation parameters. (Go to data/sensoryNeuronTable1.jpg to choose rational combinations)
    area=[] ## Area: 'head', 'body', 'tail'. 
    LRb=[] ## LRb: 'L' (left), 'R' (right), 'b' (body).
    sensor=[] ## Sensor: 'oxygen', 'mechanosensor', 'propioSomatic', 'propioTail', 'propioPharynx',
             ## 'propioHead', 'chemosensor', 'osmoceptor', 'nociceptor', 'thermosensor', 'thermonociceptive'. 
    
    G, masterInfo, simInitActivity,  pathLength, hpTest = simulation(timesteps, sim_no, hpV, ratioRandomInit, c, area, LRb, sensor)
    representation(G, masterInfo, sim_no, timesteps, simInitActivity)
    return masterInfo, simInitActivity, pathLength
    


    
def paramTestInit():
    from _simulation_ import simulation
    ### Define simulation variables
    timesteps = 50
    sim_no = 100
    hpV=-80   
    ##### Sensor stimulation parameters. (Go to data/sensoryNeuronTable1.jpg to choose rational combinations)
    area=[] ## Area: 'head', 'body', 'tail'. 
    LRb=[] ## LRb: 'L' (left), 'R' (right), 'b' (body).
    sensor=[] ## Sensor: 'oxygen', 'mechanosensor', 'propioSomatic', 'propioTail', 'propioPharynx',
             ## 'propioHead', 'chemosensor', 'osmoceptor', 'nociceptor', 'thermosensor', 'thermonociceptive'. 
             
    ## Independent variables (RI, c)
    ratioRandomInit=[0.05, 0.1, 0.15, 0.2]  # ratio of active nodes from random function (e.g. if random() < 0.2 --> activate node).
    
#    lis=list(range(60,160,2))  
#    lista=[x/100 for x in lis]    
    
#    c=[0.05,0.1,0.11,0.12,0.13,0.14,0.15,0.16,0.17,0.18,0.19,0.2,0.21,0.22,
#       0.23,0.24,0.25,0.255,0.26,0.265,0.27,0.275,0.28,0.285,0.29,0.295,
#       0.3,0.305,0.31,0.315,0.32,0.325,0.33,0.335,0.34,0.345,0.35,0.355,
#       0.36,0.37,0.38,0.39,0.4,0.41,0.42,0.43,0.44,0.45,0.46,0.47,0.48,0.49,
#       0.5,0.525,0.55,0.6,0.7,0.8,0.9]
    
    c=[0.1,0.2,0.3,0.4,0.5,0.55,0.6, 0.62, 0.64, 0.66, 0.68, 0.7, 0.72, 0.74,       # free parameter influence of weights [exin*(100*c)*weight]
       0.76, 0.78, 0.8, 0.82, 0.84, 0.86, 0.88, 0.9, 0.92, 0.94, 0.96, 0.98, 
       1.0, 1.02, 1.04, 1.06, 1.08, 1.1, 1.12, 1.14, 1.16, 1.18, 1.2, 1.22, 1.24,
       1.26, 1.28, 1.3, 1.32, 1.34, 1.36, 1.38, 1.4, 1.42, 1.44, 1.46, 1.48, 
       1.5, 1.52, 1.54, 1.56, 1.58,1.6,1.7,1.8,1.9]
    
    
    paramTest={}
    for a in ratioRandomInit:
        paramTest[a]={}
        for b in c:
            G, masterInfo, simInitActivity, pathLength, hpTest = simulation(timesteps, sim_no, hpV, a, b, area, LRb, sensor)
            paramTest[a][b]=masterInfo['mainInfo']['deactivated']  
    return paramTest






def hpTest():      ## Describing behaviour of hiperpolarization parameter.
    from _simulation_ import simulation
    ### Define simulation variables
    timesteps = 50
    sim_no = 100
    ratioRandomInit=0.2  # ratio of active nodes from random function (e.g. if random() < 0.2 --> activate node).
    c=1.5  # free parameter influence of weights [exin*(100*c)*weight]
    ##### Sensor stimulation parameters. (Go to data/sensoryNeuronTable1.jpg to choose rational combinations)
    area=[] ## Area: 'head', 'body', 'tail'. 
    LRb=[] ## LRb: 'L' (left), 'R' (right), 'b' (body).
    sensor=[] ## Sensor: 'oxygen', 'mechanosensor', 'propioSomatic', 'propioTail', 'propioPharynx',
             ## 'propioHead', 'chemosensor', 'osmoceptor', 'nociceptor', 'thermosensor', 'thermonociceptive'. 
    
    ## Independent variable (hpV)
#    lis=list(range(-70,-90,-1))
    hps=[-70, -71, -72, -73, -74, -75, -76, -77, -78, -79, -80, -81, -82, -83, -84, -85, -86, -87, -88, -89]


    hpTests={}
    
    for hpV in hps:
        G, masterInfo, simInitActivity, pathLength, hpTest = simulation (timesteps, sim_no, hpV, ratioRandomInit, c, area, LRb, sensor)
        hpTests[hpV]=hpTest
    return hpTests, masterInfo    
    
    
    


'''

Launcher

'''

## standard simulation Launcher

#masterInfo, simInitActivity, pathLength = standardInit()



## paramTest Launcher

from exports import exportParamTest, clearParamTestfolders

paramTestDic={}

for i in range(2):
    paramTest=paramTestInit()
    name='paramTest'+str(i)
    paramTestDic[name]=paramTest

clearParamTestfolders()
exportParamTest(paramTestDic)
            


## hpTest Launcher     

hpTests, masterInfo=hpTest()



            