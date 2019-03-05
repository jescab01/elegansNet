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
from plotting3D import plotting3D, plotting3Dhtml
from videoWriter import videoWriter


## Load network prepared by prepareNetwork.py, inhibitory ratio=0.08609271523178808.
G = nx.read_graphml("data/elegans.herm_connectome.graphml")
hopcountdata = nx.all_pairs_shortest_path_length(G)   #define path lengths


'''
Define simulation variables
'''

timesteps = 30
sim_no = 1
refractoryPeriod=1
ratioRandomInit=0.2  ## ratio of active nodes from random function (if random < 0.2 --> activate node).

timehtml=7  ## Time for html graph to deepen


##### Sensor stimulation parameters. 
##Go to data/sensoryNeuronTable1.jpg to choose rational combinations
   
area=['head', 'tail', 'body'] ## Area: 'head', 'body', 'tail'.
    
LRb=['b'] ## LRb: 'L' (left), 'R' (right), 'b' (body).
   
sensor=['mechanosensor'] ## Sensor: 'oxygen', 'mechanosensor', 'propioSomatic', 'propioTail', 'propioPharynx',
 ##   'propioHead', 'chemosensor', 'osmoceptor', 'nociceptor', 'thermosensor', 'thermonociceptive'. 



## Generate common initial activity
def initCommonActivity(sim):
    nodesRandomActive=0
    initActivity={}
    initActivity[sim]={}
    
    
    for a in range(len(hopcountdata)):
        if random.random() > ratioRandomInit:
            initActivity[sim]['n'+str(a)] = 0
        else:
            initActivity[sim]['n'+str(a)] = 100
            nodesRandomActive= nodesRandomActive + 1
    
    ### assign initial activity to nodes as attribute 
    for b in range(len(hopcountdata)):
        G.node['n'+str(b)]['activity']=initActivity[sim]['n'+str(b)]
    
    return initActivity, nodesRandomActive


## Generate activity stimulating sensors   
def stimulateSensors(sensor, area, LRb):
    nodesSensorActive=0
    for i in range(len(hopcountdata)):
            if G.node['n'+str(i)]['sensor'] in sensor and G.node['n'+str(i)]['area'] in area and G.node['n'+str(i)]['LRb'] in LRb:
                G.node['n'+str(i)]['activity']=100
                nodesSensorActive = nodesSensorActive + 1
           
    return nodesSensorActive

    
def getActivity(nodesRandomActive,nodesSensorActive):
    activity = []
    activityDic={}
    simInitActivity=[]
    for n,nbrs in G.adjacency_iter():
        activity.append(G.node[n]['activity'])
    for i in range(len(hopcountdata)):
        activityDic['n'+str(i)]=G.node['n'+str(i)]['activity']
    
    rInitActivity=(nodesRandomActive+nodesSensorActive)/G.number_of_nodes()
    print(rInitActivity)
    simInitActivity.append(rInitActivity)
        
    return activity, activityDic, simInitActivity


'''

Start simulations

'''


chemicalInfo=infoC(G, sim_no)
electricalInfo=infoE(G,sim_no)
mainInfo=infoM(G, sim_no)


for sim in range(sim_no):
    initActivity, nodesRandomActive = initCommonActivity(sim)
    nodesSensorActive = stimulateSensors(sensor, area, LRb)
    activity, activityDic, simInitActivity = getActivity(nodesRandomActive,nodesSensorActive)
    if sum(activity) == 0:
        print('Initially deactivated for: simulation ' + str(sim))
        break
    
      
    chemicalInfo=chemicalWorm(G, sim, timesteps, refractoryPeriod, initActivity, activityDic, activity, chemicalInfo)
    electricalInfo=electricalWorm(G, sim, timesteps, refractoryPeriod, initActivity, activityDic, activity, electricalInfo)
    mainInfo=mainWorm(G, sim, timesteps, refractoryPeriod, initActivity, activityDic, activity, mainInfo)
    

masterInfo={}
masterInfo['chemicalInfo']=chemicalInfo
masterInfo['electricalInfo']=electricalInfo
masterInfo['mainInfo']=mainInfo



del activity, activityDic, chemicalInfo, #electricalInfo, mainInfo, initActivity, 

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

### 2D/3D/3Dhtml representations
for infos, datasets in masterInfo.items():
    for sim in range(sim_no):
        if datasets['deactivated'][sim]=='None':
            plotting2D(G, sim, timesteps, datasets['activitydata'][sim], simInitActivity[sim], infos, hopcountdata)
            plotting3D(G, sim, timesteps, datasets['activitydata'][sim], simInitActivity[sim], infos, hopcountdata)

        else:
            timeplt=datasets['deactivated'][sim]
            plotting2D(G, sim, timeplt, datasets['activitydata'][sim], simInitActivity[sim], infos, hopcountdata)
            plotting3D(G, sim, timeplt, datasets['activitydata'][sim], simInitActivity[sim], infos, hopcountdata)


### Ad-hoc 3Dhtml representation to deepen
            
#htmlsim=0
#htmltimestep=4
#htmlinfos='chemicalInfo'    ## 'chemicalInfo', 'electricalInfo' or 'mainInfo'.
#
#plotting3Dhtml(G, htmlsim, htmltimestep, masterInfo[htmlinfos]['activitydata'][htmlsim][htmltimestep], 
#               simInitActivity[htmlsim], htmlinfos, hopcountdata)
    


#del datasets, sim
    
### Video generator
            
for infos in masterInfo:
    for folder in folders:
        videoWriter(infos, folder)
        
del folder, folders, infos, fileName
#        
    

