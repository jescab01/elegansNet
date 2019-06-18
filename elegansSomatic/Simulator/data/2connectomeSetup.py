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
import math

##### Load .graphml
G = nx.read_graphml("networkSetup/1.3elegans.hermSomatic_Nodestypes.graphml")
nbr=G.number_of_nodes()


##### Generate a list of cell names

nsNAME=list(range(nbr))

for i in range(nbr):
    nsNAME[i]=G.node['n'+str(i)]['cell_name']


##### Read csv and extract lists
    
#colnames=['source','target','weight','syn']
data = pandas.read_csv('networkSetup/2.0herm_full_edgelist.csv')
source=data.Source.tolist()
target=data.Target.tolist()
weight=data.Weight.tolist()
syn=data.Type.tolist()

##### Remove space before and after str

for i in range(len(source)):
    source[i]=source[i].strip()
    target[i]=target[i].strip()
    syn[i]=syn[i].strip()


##### Write lists with connections only beteween neurons
####  Thus, removing connections from/to non-neuron cells (muscles)
    
cleandic={}
cleansource=[]
cleantarget=[]
cleanweight=[]
cleansyn=[]

for a in range(len(source)):
    if source[a] in nsNAME and target[a] in nsNAME:
        cleansource.append(source[a])
        cleantarget.append(target[a])
        cleanweight.append(weight[a])
        cleansyn.append(syn[a])


### Transforming weights to counter kurtosis
        ## Original weights based on number of layers where the synapse was found (Jarrel et al., 2012)
        ## But synapse size and weight doesnt seem to be highly correlated, so:
        
logWeight=[math.log(x)+1 for x in cleanweight]



##### Lists to .csv. First, generate a dictionary with keys:column names, values:column content.
            
cleandic={'Source':cleansource,'Target':cleantarget,
          'Weight':cleanweight, 'logWeight': logWeight, 'Syn':cleansyn}

##### Write new .csv

connectome=pandas.DataFrame(cleandic, columns=['Source','Target','Weight','logWeight','Syn'])
connectome.to_csv('networkSetup/2.1herm_connections.csv', index=False)


## Translate cleansource and cleantarget to 'nx' names
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


#%%
############## Now we actually can add edges to our G networkx

for i in range(len(n_cleansource)):
    if cleansyn[i]=='chemical':
        G.add_edge(n_cleansource[i],n_cleantarget[i], Csyn='True', Cweight=logWeight[i])
    else: G.add_edge(n_cleansource[i],n_cleantarget[i],Esyn='True', Eweight=logWeight[i])
    
    
##### Complete edge attributes with Csyn/Esyn=False where necessary.
    
for a,b in G.adj.items():
    for c,d in b.items():
        if 'Csyn' not in d:
            d['Csyn']='False'
        elif 'Esyn' not in d:
            d['Esyn']='False'
            

#### Normalize synaptic weights
max_e_weight = 1
max_c_weight = 1

for n,nbrs in G.adj.items():
	for nbr,attrs in nbrs.items():
			if attrs['Esyn'] == 'True':
				if attrs['Eweight'] > max_e_weight:
					max_e_weight = attrs['Eweight']
			if attrs['Csyn'] == 'True':	
				if attrs['Cweight'] > max_c_weight:
					max_c_weight = attrs['Cweight']


for n,nbrs in G.adj.items():
	for nbr,attrs in nbrs.items():
			if attrs['Esyn'] == 'True':
				attrs['EnormWeight'] = attrs['Eweight'] / max_e_weight
			if attrs['Csyn'] == 'True':
				attrs['CnormWeight'] = attrs['Cweight'] / max_c_weight


##### Add characteristic neurotransmitter to nodes as attribute

colnames = ['Neuron_class', 'Neuron', 'Neurotransmitter']
data = pandas.read_csv('networkSetup/2.2NeurotransmitterMap.csv', names=colnames)
neuron = data.Neuron.tolist()
nttr = data.Neurotransmitter.tolist()



for a in range(len(nsNAME)):
    for b in range(len(nsNAME)):
        if G.node['n'+str(a)]['cell_name'] == neuron[b]:
            G.node['n'+str(a)]['neurotransmitters']=nttr[b]


##### From neurotransmitter attribute, decide if the neuron is excitatory or inhibitory
            
NT_types = ['Ach', 'DA', '5HT', 'Glu', 'Ach-5HT', 'Octopamine','Glu-5HT', 'Glu-Tyramine', 'GABA', 'Unknown']
inh_t=0


for i in range(len(nsNAME)):
    if G.node['n'+str(i)]['neurotransmitters'] in NT_types[:8]:
        G.node['n'+str(i)]['exin']=1
    elif G.node['n'+str(i)]['neurotransmitters']==NT_types[8]:
        G.node['n'+str(i)]['exin'] = -1
    elif G.node['n'+str(i)]['neurotransmitters']==NT_types[9]:
        G.node['n'+str(i)]['exin'] = 1

### Calculate ratio of inhibitory neurons

for i in range(len(nsNAME)):
   if G.node['n'+str(i)]['exin']==-1:
        inh_t = inh_t + 1
inh_ratio = inh_t / 302	


## For those cells whose neurotransmitter is unknown, assign ex/inh by ratio

for i in range(len(nsNAME)):
    if G.node['n'+str(i)]['exin']==0:
        if numpy.random.random()>inh_ratio:
            G.node['n'+str(i)]['exin'] = 1
        else:
            G.node['n'+str(i)]['exin'] = -1


##### Prepare attribute for refractory online update of refractory period

for n,nbrs in G.adj.items():
	G.node[n]['consecutiveAct'] = 0


##### Clear variables

del a,b,c,d,i,colnames,data,source,syn,target,weight,nsNAME,connectome,cleansource,cleantarget
del n_cleantarget, n_cleansource, cleanweight, cleansyn, neuron, nttr, NT_types, inh_t
del n, nbr
            
            

##### Rewrite Graphml

nx.write_graphml(G, 'elegans.hermSomatic_connectome.graphml')


