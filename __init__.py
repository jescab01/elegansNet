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


    
def paramTest():
    from _simulation_ import simulation
    import pandas
    
    ### Define simulation variables
    timesteps = 50
    sim_no = 100

    ##### Sensor stimulation parameters. (Go to data/sensoryNeuronTable1.jpg to choose rational combinations)
    area=[] ## Area: 'head', 'body', 'tail'. 
    LRb=[] ## LRb: 'L' (left), 'R' (right), 'b' (body).
    sensor=[] ## Sensor: 'oxygen', 'mechanosensor', 'propioSomatic', 'propioTail', 'propioPharynx',
             ## 'propioHead', 'chemosensor', 'osmoceptor', 'nociceptor', 'thermosensor', 'thermonociceptive'. 
             
    ##Independent Variable 1 (RI)
    ratioRandomInit=[0.05, 0.1, 0.15, 0.2, 0.25] 
    
    
    ## Independent Variable 2 (c): free parameter influence of weights [exin*(100*c)*weight]
    clist=[0.1, 0.2, 0.3, 0.4, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75,       # free parameter influence of weights [exin*(100*c)*weight]
       0.76, 0.78, 0.8, 0.82, 0.84, 0.86, 0.88, 0.9, 0.92, 0.94, 0.96, 0.98, 
       1.0, 1.02, 1.04, 1.06, 1.08, 1.1, 1.12, 1.14, 1.15, 1.2, 1.25,
       1.3, 1.35, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2, 2.3, 2.6]

    
   
    ## Independent variable 3(hpV)
#    lis=list(range(-71,-80,-0.5))
    hps=[-71, -71.5, -72, -72.5, -73, -73.5, -74, -74.5, -75, -75.5,
         -76, -76.5, -77, -77.5, -78, -78.5, -79, -79.5, -80, -81, -82,
         -83, -84, -85, -86, -87, -88, -89, -90, -91, -92, -93, -94, -95,
         -96, -97, -98, -99,-100,-102,-104,-106,-108,-110]

    surviveBinary={}  
    rrp2spike={}
    rrp2rest={}
    
    for ri in ratioRandomInit:
        surviveBinary[ri]={}
        rrp2spike[ri]={}
        rrp2rest[ri]={}

        
        for c in clist:
            surviveBinary[ri][c]=pandas.DataFrame()
            rrp2spike[ri][c]=pandas.DataFrame()
            rrp2rest[ri][c]=pandas.DataFrame()

            
            for hpV in hps:
                G, masterInfo, simInitActivity, pathLength, hpTest = simulation (timesteps, sim_no, ri, c, hpV, area, LRb, sensor)
                
                surviveBinary[ri][c][hpV]=masterInfo['mainInfo']['deactivated'].values()
                surviveBinary[ri][c][hpV]=surviveBinary[ri][c][hpV].replace(list(range(1,50)), 0)
                surviveBinary[ri][c][hpV]=surviveBinary[ri][c][hpV].replace('None', 1)
                
            ### manipulate data to obtain probability of rrp to spike
                rrp2spikeList=[]
                rrp2restList=[]
                for sim in range(sim_no):
                    inRRPcount=0
                    rrp2restCount=0
                    if masterInfo['mainInfo']['deactivated'][sim]=='None':
                        for timestep in range(timesteps):
                            inRRPcount+=hpTest[sim][timestep].count('inRRP')
                            rrp2restCount+=hpTest[sim][timestep].count('rrp2rest')
                        ## compute probability of using the refractory period and add it to a list. 
                        rrp2spikeList.append(inRRPcount-rrp2restCount)
                        rrp2restList.append(rrp2restCount)
                    
                    else:
                        for timestep in range(masterInfo['mainInfo']['deactivated'][sim]):
                            inRRPcount+=hpTest[sim][timestep].count('inRRP')
                            rrp2restCount+=hpTest[sim][timestep].count('rrp2rest')
                        ## compute probability of using the refractory period and add it to a list. 
                        rrp2spikeList.append(inRRPcount-rrp2restCount)
                        rrp2restList.append(rrp2restCount)
                
                rrp2spike[ri][c][hpV]=rrp2spikeList
                rrp2rest[ri][c][hpV]=rrp2restList


    return masterInfo, surviveBinary, rrp2spike, rrp2rest  



'''

Launcher

'''

'''## standard simulation Launcher'''

#masterInfo, simInitActivity, pathLength = standardInit()




''' ## parameter Testing Launcher'''
import pandas
import time

paramTestData=pandas.DataFrame()

## Run simulations
masterInfo, surviveBinary, rrp2spike, rrp2rest = paramTest()

## Gather data from simulations
for ri, cs in surviveBinary.items():
    for c, hpVs in cs.items():
        for hpV in list(surviveBinary[ri][c]):
            for i in list(surviveBinary[ri][c].index):
                dic={'RI':ri,'c':c,'hpV':hpV,'surviveBinary':surviveBinary[ri][c][hpV][i],
                     'rrp2spike':rrp2spike[ri][c][hpV][i], 'rrp2rest':rrp2rest[ri][c][hpV][i]}
                paramTestData=paramTestData.append(dic, ignore_index=True)

## Export data to .csv
localtime = time.asctime(time.localtime(time.time()))
paramTestData.to_csv('data/parameterTesting/data_'+localtime+'.csv', index=False)

## Clear variables
del c, cs, hpV, hpVs, ri, dic, i, localtime, rrp2rest, rrp2spike, surviveBinary


            