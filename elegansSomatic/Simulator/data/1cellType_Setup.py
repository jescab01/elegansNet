#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 11:00:21 2019

@author: jescab01
"""

import networkx as nx
import pandas

G = nx.read_graphml("networkSetup/1.0elegans.hermSomatic_nodesPos.graphml")


'''
Sensory neurons' attributes setup. 
'''

## Generate a list of nodes from connectome
nsNAME=list(range(G.number_of_nodes()))

for i in range(len(nsNAME)):
    nsNAME[i]=G.node['n'+str(i)]['cell_name']


## Charge connectome connections for testing later
edges={}
data=pandas.read_csv('networkSetup/2.0herm_full_edgelist.csv')
source=data.Source.tolist()
target=data.Target.tolist()

for i in range(len(source)):
    source[i]=source[i].strip()
    target[i]=target[i].strip()


edges['source']=source
edges['target']=target

del source, target

   

##import sensory neurons
data=pandas.read_csv('networkSetup/1.1sensoryNeurons.csv')
chemo=data.Chemosensors.tolist()
odor=data.Odorsensors.tolist()
oxygen=data.OxygenSensors.tolist()
noci=data.Nociceptors.tolist()
osmo=data.Osmoceptors.tolist()
thermo=data.Thermosensors.tolist()
mechano=data.Mechanosensors.tolist()
propioSomatic=data.PropioSomatic.tolist()
propioHead=data.PropioHead.tolist()
propioTail=data.PropioTail.tolist()
propioPharynx=data.PropioPharynx.tolist()


lista=[chemo,odor,oxygen,noci, osmo, thermo, mechano, propioSomatic, propioHead, propioTail, propioPharynx]
    
### removing 'nan' items in each group looping the deletion in range propioceptors
### which have the higer number or cells.

for i in range(100):
    for lis in lista:
        for i in range(len(lis)):
            if lis[i]!=lis[i]:
                del lis[i]
                break
            
### Generate a list with all sensory cells     
sensorycells=[]
for lis in lista:
    for i in range(len(lis)):
        sensorycells.append(lis[i])

sensorycellsdic={'chemo':chemo,'odor':odor,'oxygen':oxygen,'noci':noci,
              'osmo':osmo, 'thermo':thermo, 'mechano':mechano, 'propioHead':propioHead,
              'propioSomatic':propioSomatic,'propioTail':propioTail,'propioPharynx':propioPharynx}


del lis, lista, i, data
del chemo,odor,oxygen,noci, osmo, thermo, mechano
del propioSomatic, propioHead, propioTail, propioPharynx


#Some cells are multi modality sensors, as example: AFD
for i in range(len(sensorycells)):
    if 'AFD' in sensorycells[i]:
        print('ok')


## clean duplicated cells from sensorycells
cleansensorycells=[]

for i in range(len(sensorycells)):
    if sensorycells[i] not in cleansensorycells:
        cleansensorycells.append(sensorycells[i])

del sensorycells

# From cleansensorycells, separate in two lists: ready, notready
ready=[]
notready=[]
for i in range(len(cleansensorycells)):
    if cleansensorycells[i] in nsNAME:
        ready.append(cleansensorycells[i])
    else: notready.append(cleansensorycells[i])

del cleansensorycells

### Each notready cell lacks info: L/R
    
notreadyLR=[]
for i in range(len(notready)):
    notreadyLR.append(notready[i]+'R')
    notreadyLR.append(notready[i]+'L')
    
## control every sensory neuron is recognized as having edges
notrecognized=[]
recognized=[]

for i in range(len(notreadyLR)):
    if notreadyLR[i] not in edges['target'] or notreadyLR[i] not in edges['source']:
        notrecognized.append(notreadyLR[i])
    else: recognized.append(notreadyLR[i])


sensorycells=[]
for i in range(len(ready)):
    sensorycells.append(ready[i])
    
for i in range(len(notreadyLR)):
    sensorycells.append(notreadyLR[i])
    
sensorycells=pandas.DataFrame(sensorycells)
## We exported this data to get a list of sensory neurons updated and ready to use. 
## This excel sheet was manually updated with attributes sensor, area and LRb.

## Clean variables
del i, notrecognized, recognized, edges
del sensorycellsdic, notready, notreadyLR, ready


#%% Once manually updated '1.2sensorycells.csv' with attributes 'sensor', 'area' and 'LRb'
''' Add attributes 'sensor', 'area' and 'LRb' to nodes '''

sensoryUpdate=pandas.read_csv('networkSetup/1.1sensorycellsSomatic.csv')

sensory_cell_name=sensoryUpdate.cell_name.tolist()
sensor=sensoryUpdate.sensor.tolist()
area=sensoryUpdate.area.tolist()
LRb=sensoryUpdate.LR.tolist()


for a in range(len(nsNAME)):
    for b in range(len(sensory_cell_name)):
        if G.node['n'+str(a)]['cell_name']==sensory_cell_name[b]:
            G.node['n'+str(a)]['sensor']=sensor[b]
            G.node['n'+str(a)]['area']=area[b]
            G.node['n'+str(a)]['LRb']=LRb[b]
            break
        else: G.node['n'+str(a)]['sensor']='None'


#Clear variables
del a,b,area,sensory_cell_name,sensor, LRb


#%% Cell types

'''
Cell type setup
'''

types=pandas.read_csv('networkSetup/1.2cell_typesSomatic.csv')
cell_name=types.cell_name.tolist()
cell_type=types.cell_type.tolist()

for a in range(len(nsNAME)):
    for b in range(len(cell_name)):
        if G.node['n'+str(a)]['cell_name']==cell_name[b]:
            G.node['n'+str(a)]['cell_type']=cell_type[b]


## Clear variables
            
del a,b,nsNAME,cell_type,cell_name


'''
Rewrite .graphml implementing all new changes 
'''
    
nx.write_graphml(G, 'networkSetup/1.3elegans.herm_Nodestypes.graphml')






    















