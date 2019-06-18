#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 18:27:28 2019

@author: jescab01
"""
import networkx as nx
import pandas

G = nx.read_graphml("data/elegans.herm_connectome.graphml")

EnormWeights=[]
CnormWeights=[]
for source, target in G.edges():
    if 'EnormWeight' in G[source][target] and 'CnormWeight' in G[source][target]:
        EnormWeights.append(G[source][target]['EnormWeight'])
        CnormWeights.append(G[source][target]['CnormWeight'])
    
    elif 'EnormWeight' in G[source][target]:
        EnormWeights.append(G[source][target]['EnormWeight'])
        
    elif 'CnormWeight' in G[source][target]:
        CnormWeights.append(G[source][target]['CnormWeight'])
    
CnormWeights=pandas.DataFrame(CnormWeights)
EnormWeights=pandas.DataFrame(EnormWeights)

CnormWeights.to_csv('data/parameterTesting/Cw.csv', index=False)
EnormWeights.to_csv('data/parameterTesting/Ew.csv', index=False)
