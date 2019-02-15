#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 10:14:54 2019

@author: jescab01
"""

import networkx as nx
import pandas

##### Load .graphml
G = nx.read_graphml("elegans.herm_onlynodes.graphml")


#####Generate a list of nodes names (two ways)

#ns=list(range(303))
#for i in range(303):
#    ns[i]='n'+str(i)

nsNAME=list(range(303))

for i in range(303):
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
    #### Removing connections from/to non neuron cells
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


##### Lists to .csv
            
cleandic={'Source':cleansource,'Target':cleantarget,
          'Weight':cleanweight,'Syn':cleansyn}

##### Write new .csv

connectome=pandas.DataFrame(cleandic, columns=['Source','Target',
          'Weight','Syn'])
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


##### Clear variables

del a,b,c,i,colnames,data,source,syn,target,weight,nsNAME,connectome,cleansource,cleantarget


############## Now we actually can add edges to our G networkx

for i in range(len(n_cleansource)):
    if cleansyn[i]=='chemical':
        G.add_edge(n_cleansource[i],n_cleantarget[i],
                   attr_dict={'Csyn':'True', 'Cweight':cleanweight[i]})
        
    else: G.add_edge(n_cleansource[i],n_cleantarget[i],
                     attr_dict={'Esyn':'True', 'Eweight':cleanweight[i]})








