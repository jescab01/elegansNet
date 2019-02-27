"""
Created on Fri Feb 22 19:58:17 2019

@author: jescab01

"""

import networkx as nx
import random
import os
from chemicalWorm import infoC, chemicalWorm
from electricalWorm import infoE, electricalWorm
from mainWorm import infoM, mainWorm
from plotting2D import plotting2D
from plotting3D import plotting3D
from videoWriter import videoWriter


## Load network prepared by prepareNetwork.py, inhibitory ratio=0.08609271523178808.
G = nx.read_graphml("data/elegans.herm_connectome.graphml")
hopcountdata = nx.all_pairs_shortest_path_length(G)   #define path lengths

## Define simulation variables
timesteps = 100
sim_no = 2
refractoryPeriod=1


## Generate common initial activity

def initCommonActivity(sim):
    nodesActive=0
    initActivity={}
    initActivity[sim]={}
    
    
    for a in range(302):
        if random.random() > 0.20:
            initActivity[sim]['n'+str(a)] = 0
        else:
            initActivity[sim]['n'+str(a)] = 100
            nodesActive= nodesActive + 1
        
    rInitActivity=float(nodesActive)/G.number_of_nodes()
    print(rInitActivity)
    simInitActivity.append(rInitActivity)
    
    ### assign initial activity to nodes as attribute 
    for b in range(302):
        G.node['n'+str(b)]['activity']=initActivity[sim]['n'+str(b)]
    
    return initActivity, simInitActivity

    
def getActivity():
    activity = []
    activityDic={}
    for n,nbrs in G.adjacency_iter():
        activity.append(G.node[n]['activity'])
    for i in range(302):
        activityDic['n'+str(i)]=G.node['n'+str(i)]['activity']
    return activity, activityDic


'''

Start simulations

'''

simInitActivity=[]
chemicalInfo=infoC(G, sim_no)
electricalInfo=infoE(G,sim_no)
mainInfo=infoM(G, sim_no)


for sim in range(sim_no):
    initActivity, simInitActivity = initCommonActivity(sim)
    activity, activityDic = getActivity()
    if sum(activity) == 0:
        print('Initially deactivated for: simulation ' + str(sim))
        break
    
      
    chemicalInfo=chemicalWorm(G, sim, timesteps, refractoryPeriod, initActivity, activityDic, activity, chemicalInfo)
    electricalInfo=electricalWorm(G, sim, timesteps, refractoryPeriod, initActivity, activityDic, activity, electricalInfo)
    mainInfo=mainWorm(G, sim, timesteps, refractoryPeriod, initActivity, activityDic, activity, mainInfo)
    
    
masterInfo={'chemicalInfo':chemicalInfo,'electricalInfo':electricalInfo,'mainInfo':mainInfo}

del activity, activityDic, chemicalInfo, electricalInfo, mainInfo, initActivity, 

'''
Representations: 2D, 3D images and videos
'''

### Clean plots' folders

folders=['nx2D', 'plotly3D']

for infos in masterInfo:
    for folder in folders:
        dirPath= 'output/'+str(infos)+'Plots/'+str(folder)
        fileList = os.listdir(dirPath)
        for fileName in fileList:
            os.remove(dirPath+"/"+fileName)

del dirPath, fileList, #fileName

### 2D/3D representation
for infos, datasets in masterInfo.items():
    for sim in range(sim_no):
        if datasets['deactivated'][sim]=='None':
            plotting2D(G, sim, timesteps, datasets['activitydata'][sim], simInitActivity[sim], infos)
            plotting3D(G, sim, timesteps, datasets['activitydata'][sim], simInitActivity[sim], infos)
            
        else:
            timeplt=datasets['deactivated'][sim]
            plotting2D(G, sim, timeplt, datasets['activitydata'][sim], simInitActivity[sim], infos)
            plotting3D(G, sim, timeplt, datasets['activitydata'][sim], simInitActivity[sim], infos)

del datasets, sim
    
### Video generator
            
for infos in masterInfo:
    for folder in folders:
        videoWriter(infos, folder)
        
del folder, folders, infos
        
    

