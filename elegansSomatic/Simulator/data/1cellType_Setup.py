#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 11:00:21 2019

@author: jescab01
"""

import networkx as nx
import pandas

G = nx.read_graphml("networkSetup/1.0elegans.hermSomatic_nodesPos.graphml")
nbr=G.number_of_nodes()


'''
Sensory neurons' attributes setup. 
'''

## Generate a list of nodes from connectome
nsNAME=list(range(nbr))

for i in range(nbr):
    nsNAME[i]=G.node['n'+str(i)]['cell_name']


## Manually updated '1.1Sensorycells.csv' with attributes 'sensor', 'area' and 'LRb'
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


## Clear variables
del a,b,area,sensory_cell_name,sensor, LRb


#%% Cell types

'''
Cell type setup
'''

types=pandas.read_csv('networkSetup/1.2cell_typesSomatic.csv')
cell_name=types.cell_name.tolist()
cell_type=types.cell_type.tolist()
group=types.group.tolist()

for a in range(len(nsNAME)):
    for b in range(len(cell_name)):
        if G.node['n'+str(a)]['cell_name']==cell_name[b]:
            G.node['n'+str(a)]['cell_type']=cell_type[b]
            G.node['n'+str(a)]['cellType_group']=group[b]


## Clear variables
            
del a,b,nsNAME,cell_type,cell_name


'''
Rewrite .graphml implementing all new changes 
'''
    
nx.write_graphml(G, 'networkSetup/1.3elegans.hermSomatic_Nodestypes.graphml')


group=[]
for n in range(G.number_of_nodes()):
    group.append(G.node['n'+str(n)]['cellType_group'])


    















