#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 17:33:34 2019

@author: jescab01
"""

def standardInit():
    from _simulation_ import simulation, representation
    ### Define simulation variables
    timesteps = 100
    sim_no = 1
    Psens=0.15   # Parameter for sensory neurons being excited by environment
    
    hpV=-90
    ratioRandomInit=0.2  # ratio of active nodes from random function (e.g. if random() < 0.2 --> activate node).
    c=0.2  # free parameter influence of weights [exin*(100*c)*weight]
    ##### Sensor stimulation parameters. (Go to data/sensoryNeuronTable1.jpg to choose rational combinations)
    area=[] ## Area: 'head', 'body', 'tail'. 
    LRb=[] ## LRb: 'L' (left), 'R' (right), 'b' (body).
    sensor=[] ## Sensor: 'oxygen', 'mechanosensor', 'propioSomatic', 'propioTail', 'propioPharynx',
             ## 'propioHead', 'chemosensor', 'osmoceptor', 'nociceptor', 'thermosensor', 'thermonociceptive'. 
    
    G, masterInfo, simInitActivity,  pathLength, hpTest, envActivation = simulation(timesteps, sim_no, ratioRandomInit, c, hpV, area, LRb, sensor, Psens)
    representation(G, masterInfo, sim_no, timesteps, simInitActivity, hpV)
    return masterInfo, simInitActivity, pathLength, envActivation


    
def paramTest():
    from _simulation_ import simulation
    import pandas
    
    ### Define simulation variables
    timesteps = 50
    sim_no = 50
    Psenss=[0,0.1,0.2]   # Probability of sensory neurons being excited by environment

    ##### Sensor stimulation parameters. (Go to data/sensoryNeuronTable1.jpg to choose rational combinations)
    area=[] ## Area: 'head', 'body', 'tail'. 
    LRb=[] ## LRb: 'L' (left), 'R' (right), 'b' (body).
    sensor=[] ## Sensor: 'oxygen', 'mechanosensor', 'propioSomatic', 'propioTail', 'propioPharynx', 'odorsensor',
             ## 'propioHead', 'chemosensor', 'osmoceptor', 'nociceptor', 'thermosensor', 'thermonociceptive'. 
             
    ##Independent Variable 1 (RI)
    ratioRandomInit=[0.05, 0.1, 0.15, 0.2, 0.25] 
    
    
    ## Independent Variable 2 (c): free parameter influence of weights [exin*(100*c)*weight]
    clist=[0.05,0.075,0.1,0.12,0.14,0.15,
           0.16,0.17,0.18,0.19,0.2,0.21,
           0.22,0.23,0.24,0.25,0.275,0.3,
           0.325,0.35,0.375,0.4,0.45,0.5]
    


    
   
    ## Independent variable 3(hpV)
#    lis=list(range(-71,-80,-0.5))
    hps=[-76, -78, -80, -82, -84, -85, -86, 
         -87, -88, -89, -90, -91, -92, -93,
         -94, -96, -98, -100, -104]

    surviveTime={}  
    rrp2spike={}
    rrp2rest={}
    envActiv={}
    
    for Psens in Psenss:
        surviveTime[Psens]={}
        rrp2spike[Psens]={}
        rrp2rest[Psens]={} 
        envActiv[Psens]={}
        for ri in ratioRandomInit:
            surviveTime[Psens][ri]={}
            rrp2spike[Psens][ri]={}
            rrp2rest[Psens][ri]={}
            envActiv[Psens][ri]={}
    
            
            for c in clist:
                surviveTime[Psens][ri][c]=pandas.DataFrame()
                rrp2spike[Psens][ri][c]=pandas.DataFrame()
                rrp2rest[Psens][ri][c]=pandas.DataFrame()
                envActiv[Psens][ri][c]={}
    
                
                for hpV in hps:
                    G, masterInfo, simInitActivity, pathLength, hpTest, envActivation = simulation (timesteps, sim_no, ri, c, hpV, area, LRb, sensor, Psens)
                    
                    surviveTime[Psens][ri][c][hpV]=masterInfo['mainInfo']['deactivated'].values()
                    surviveTime[Psens][ri][c][hpV]=surviveTime[Psens][ri][c][hpV].replace('None', timesteps)
                    
                    envActiv[Psens][ri][c][hpV]=envActivation
                    
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
                    
                    rrp2spike[Psens][ri][c][hpV]=rrp2spikeList
                    rrp2rest[Psens][ri][c][hpV]=rrp2restList


    return masterInfo, surviveTime, rrp2spike, rrp2rest, envActiv



'''

Launcher

'''

'''## standard simulation Launcher'''

masterInfo, simInitActivity, pathLength, envActivation = standardInit()



''' ## parameter Testing Launcher'''
#import pandas
#import time
#
#paramTestData=pandas.DataFrame()
#
### Run simulations
#masterInfo, surviveTime, rrp2spike, rrp2rest, envActiv= paramTest()
#
### Gather data from simulations
#for Psens, ris in surviveTime.items():
#    for ri, cs in ris.items():
#        for c, hpVs in cs.items():
#            for hpV in list(surviveTime[Psens][ri][c]):
#                for i in list(surviveTime[Psens][ri][c].index):
#                    dic={'Psens':Psens,'RI':ri,'c':c,'hpV':hpV,'surviveTime':surviveTime[Psens][ri][c][hpV][i],
#                         'rrp2spike':rrp2spike[Psens][ri][c][hpV][i], 'rrp2rest':rrp2rest[Psens][ri][c][hpV][i],
#                         'active':len(envActiv[Psens][ri][c][hpV][i]['active']),'activeG':len(envActiv[Psens][ri][c][hpV][i]['activeG']),
#                         'activeSG':len(envActiv[Psens][ri][c][hpV][i]['activeSG']),'activeNode':len(envActiv[Psens][ri][c][hpV][i]['activeNode'])}
#                    
#                    paramTestData=paramTestData.append(dic, ignore_index=True)
#
### Export data to .csv
#localtime = time.asctime(time.localtime(time.time()))
#paramTestData.to_csv('data/parameterTesting/dataN_'+localtime+'.csv', index=False)
#
### Clear variables
#del c, cs, hpV, hpVs, ri, dic, i, localtime, surviveTime, Psens
#del envActiv, rrp2spike, rrp2rest, ris


            