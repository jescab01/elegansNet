#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 10:14:54 2019

@author: jescab01

This code will process raw data from different sources (go to readme.txt)
and define a basic banch of nodes with defined topology, connections 
and neurotransmitter type.

Also prepare fixed attributes as ex/inh and normalized weight.

"""

import networkx as nx
import pandas
import numpy.random

##### Load .graphml
G = nx.read_graphml("elegans.herm_nodesPos.graphml")


##### Generate a list of cell names

nsNAME=list(range(302))

for i in range(302):
    nsNAME[i]=G.node['n'+str(i)]['cell_name']


##### Read csv and extract lists
    
colnames=['source','target','weight','syn']
data = pandas.read_csv('herm_full_edgelist_MODIFIED.csv', names=colnames)
source=data.source.tolist()
target=data.target.tolist()
weight=data.weight.tolist()
syn=data.syn.tolist()

##### Remove space before and after str

for i in range(len(source)):
    source[i]=source[i].strip()
    target[i]=target[i].strip()
    syn[i]=syn[i].strip()


##### Write lists with connections only beteween neurons
####  Thus, removing connections from/to non-neuron cells (sensory/muscles)
    
cleandic={}
cleansource=[]
cleantarget=[]
cleanweight=[]
cleansyn=[]

for a in range(len(source)):
    for b in range(len(nsNAME)):
        if source[a]==nsNAME[b]:
            for c in range(len(nsNAME)):
                if target[a]==nsNAME[c]:
                    cleansource.append(source[a])
                    cleantarget.append(target[a])
                    cleanweight.append(weight[a])
                    cleansyn.append(syn[a])


##### Lists to .csv. First, generate a dictionary with keys:column names, values:column content.
            
cleandic={'Source':cleansource,'Target':cleantarget,
          'Weight':cleanweight,'Syn':cleansyn}

##### Write new .csv

connectome=pandas.DataFrame(cleandic, columns=['Source','Target','Weight','Syn'])
connectome.to_csv('/home/jescab01/elegansProject/elegansNet/data/herm_connectome.csv')


##### Translate cleansource and cleantarget to 'nx' names

n_cleansource=[]
n_cleantarget=[]

for a in range(len(cleansource)):
    for b in range(len(nsNAME)):
        if cleansource[a]==G.node['n'+str(b)]['cell_name']:
            n_cleansource.append('n'+str(b))
        
for a in range(len(cleansource)):
    for b in range(len(nsNAME)):
        if cleantarget[a]==G.node['n'+str(b)]['cell_name']:
            n_cleantarget.append('n'+str(b))



############## Now we actually can add edges to our G networkx

for i in range(len(n_cleansource)):
    if cleansyn[i]=='chemical':
        G.add_edge(n_cleansource[i],n_cleantarget[i],
                   attr_dict={'Csyn':'True', 'Cweight':cleanweight[i]})
        
    else: G.add_edge(n_cleansource[i],n_cleantarget[i],
                     attr_dict={'Esyn':'True', 'Eweight':cleanweight[i]})
    
    
##### Complete edge attributes with Csyn/Esyn=False where necessary.
    
for a,b in G.adjacency_iter():
    for c,d in b.items():
        if 'Csyn' not in d:
            d['Csyn']='False'
        elif 'Esyn' not in d:
            d['Esyn']='False'
            
            
#### Normalize synaptic weights
max_e_weight = 1
max_c_weight = 1

for n,nbrs in G.adjacency_iter():
	for nbr,attrs in nbrs.items():
			if attrs['Esyn'] == 'True':
				if attrs['Eweight'] > max_e_weight:
					max_e_weight = attrs['Eweight']
			if attrs['Csyn'] == 'True':	
				if attrs['Cweight'] > max_c_weight:
					max_c_weight = attrs['Cweight']


for n,nbrs in G.adjacency_iter():
	for nbr,attrs in nbrs.items():
			if attrs['Esyn'] == 'True':
				attrs['EnormWeight'] = attrs['Eweight'] / max_e_weight
			if attrs['Csyn'] == 'True':
				attrs['CnormWeight'] = attrs['Cweight'] / max_c_weight


##### Add characteristic neurotransmitter to nodes as attribute

colnames = ['Neuron_class', 'Neuron', 'Neurotransmitter']
data = pandas.read_csv('NeurotransmitterMap.csv', names=colnames)
neuron = data.Neuron.tolist()
nttr = data.Neurotransmitter.tolist()



for a in range(302):
    for b in range(302):
        if G.node['n'+str(a)]['cell_name'] == neuron[b]:
            G.node['n'+str(a)]['neurotransmitters']=nttr[b]


##### From neurotransmitter attribute, decide if the neuron is excitatory or inhibitory
            
NT_types = ['Ach', 'DA', '5HT', 'Glu', 'Ach-5HT', 'Octopamine','Glu-5HT', 'Glu-Tyramine', 'GABA', 'Unknown']
inh_t=0


for i in range(302):
    if G.node['n'+str(i)]['neurotransmitters'] in NT_types[:8]:
        G.node['n'+str(i)]['exin']=1
    elif G.node['n'+str(i)]['neurotransmitters']==NT_types[8]:
        G.node['n'+str(i)]['exin'] = -1
    elif G.node['n'+str(i)]['neurotransmitters']==NT_types[9]:
        G.node['n'+str(i)]['exin'] = 0

### Calculate ratio of inhibitory neurons

for i in range(302):
   if G.node['n'+str(i)]['exin']==-1:
        inh_t = inh_t + 1
inh_ratio = inh_t / 302	


## For those cells whose neurotransmitter is unknown, assign ex/inh by ratio

for i in range(302):
    if G.node['n'+str(i)]['exin']==0:
        if numpy.random.random()>inh_ratio:
            G.node['n'+str(i)]['exin'] = 1
        else:
            G.node['n'+str(i)]['exin'] = -1




##### Clear variables

del a,b,c,d,i,colnames,data,source,syn,target,weight,nsNAME,connectome,cleansource,cleantarget
del n_cleantarget, n_cleansource, cleanweight, cleansyn, neuron, nttr, NT_types, inh_t
del attrs, max_c_weight, max_e_weight, n, nbrs, nbr
            
            

##### Rewrite Graphml

nx.write_graphml(G, 'elegans.herm_connectome.graphml')


