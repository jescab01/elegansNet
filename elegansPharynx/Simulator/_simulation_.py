"""
Created on Fri Feb 22 19:58:17 2019

@author: jescab01

"""

'Defining auxiliary functions'

## Generate common initial activity
def initCommonActivity(G, sim, nodesNumber, ratioRandomInit):
    import random
    nodesRandomActive=0
    initActivity={}
    initActivity[sim]={}
    
    auxiliar_types=['Sensory', 'Motor, Sensory', 'Interneuron, Sensory',
                    'Interneuron, Sensory, Motor']    
    
    for a in range(nodesNumber):
        if G.node['n'+str(a)]['cell_type'] in auxiliar_types and random.random() < ratioRandomInit:
            initActivity[sim]['n'+str(a)] = -30
            nodesRandomActive= nodesRandomActive + 1
        else:
            initActivity[sim]['n'+str(a)] =-70
    
    ### assign initial activity to nodes as attribute 
    for b in range(nodesNumber):
        G.node['n'+str(b)]['mV']=initActivity[sim]['n'+str(b)]
    
    return initActivity, nodesRandomActive


## Generate activity stimulating sensors   
def stimulateSensors(G, sensor, area, LRb, nodesNumber):
    nodesSensorActive=0
    for i in range(nodesNumber):
            if G.node['n'+str(i)]['sensor'] in sensor and G.node['n'+str(i)]['area'] in area and G.node['n'+str(i)]['LRb'] in LRb:
                G.node['n'+str(i)]['mV']=40
                nodesSensorActive = nodesSensorActive + 1
           
    return nodesSensorActive

    
def getActivity(G, nodesRandomActive, nodesSensorActive, simInitActivity, nodesNumber):
    activity = []
    activityDic={}
    for n,nbrs in G.adj.items():
        activity.append(G.node[n]['mV'])
    for i in range(nodesNumber):
        activityDic['n'+str(i)]=G.node['n'+str(i)]['mV']
    
    rInitActivity=(nodesRandomActive+nodesSensorActive)/G.number_of_nodes()
    print(rInitActivity)
    simInitActivity.append(rInitActivity)
        
    return activity, activityDic, simInitActivity


'''

                         Simulation

'''

def simulation(timesteps, sim_no, ratioRandomInit, c, area, LRb, sensor, Psens, att):
    
    import networkx as nx
#    from chemicalWorm import infoC, chemicalWorm
#    from electricalWorm import infoE, electricalWorm
 #   from mainWorm import infoM, mainWorm
    from mainWormGraded import infoG, mainWormGraded
    
    
    ## Load network prepared by prepareNetwork.py, inhibitory ratio=0.08609271523178808.
    G = nx.read_graphml("data/elegans.hermPharynx_connectome.graphml")
    nodesNumber = G.number_of_nodes()
    pathLength=dict(nx.all_pairs_shortest_path_length(G))  #define path lengths
    
    
    '''
    Start simulations
    '''
#    chemicalInfo=infoC(G, sim_no)
#    electricalInfo=infoE(G,sim_no)
#    mainInfo=infoM(G, sim_no)
    mainInfoGraded=infoG(G, sim_no)
    
    hpTest={}
    envActivation={}

    simInitActivity=[]
    
    for sim in range(sim_no):
        initActivity, nodesRandomActive = initCommonActivity(G, sim, nodesNumber, ratioRandomInit)
        nodesSensorActive = stimulateSensors(G, sensor, area, LRb, nodesNumber)
        activity, activityDic, simInitActivity = getActivity(G, nodesRandomActive, nodesSensorActive, simInitActivity, nodesNumber)
        
        hpTest[sim]={}
        envActivation[sim]={'active':[], 'activeG':[], 'activeSG':[], 'activeNode':[]}
        
        
          
#        chemicalInfo=chemicalWorm(G, sim, timesteps, initActivity, activityDic, activity, chemicalInfo, c)
#        electricalInfo=electricalWorm(G, sim, timesteps, initActivity, activityDic, activity, electricalInfo, c)
#        mainInfo, hpTest, envActivation = mainWorm(G, sim, timesteps, initActivity, activityDic, activity, mainInfo, c, hpTest, Psens, envActivation)
        mainInfoGraded, hpTest, envActivation = mainWormGraded(G, sim, timesteps, initActivity, activityDic, activity, mainInfoGraded, c, hpTest, Psens, envActivation, att)
    
    masterInfo={}
#    masterInfo['chemicalInfo']=chemicalInfo
#    masterInfo['electricalInfo']=electricalInfo
#    masterInfo['mainInfo']=mainInfo
    masterInfo['mainInfoGraded']=mainInfoGraded
    
    
    return G, masterInfo, simInitActivity, pathLength, hpTest, envActivation
    #del activity, activityDic, #chemicalInfo, #electricalInfo, mainInfo, initActivity, 


'''
Representations: 2D, 3D images and videos
'''

def representation(G, masterInfo, sim_no, timesteps, simInitActivity):
    
    import os
    from plotting2D import plotting2D
    from plotting3D import plotting3D, plotting3Dhtml
    from videoWriter import videoWriter
    
    ## Clean plots' folders
    folders=['nx2D', 'plotly3D']
    
    for infos in masterInfo:
        for folder in folders:
            dirPath= 'output/'+str(infos)+'Plots/'+str(folder)
            fileList = os.listdir(dirPath)
            for fileName in fileList:
                os.remove(dirPath+"/"+fileName)
    
    del dirPath, fileList, #fileName
    
    
    ## 2D/3D/3Dhtml representations
    for infos, datasets in masterInfo.items():
        for sim in range(sim_no):
            if datasets['deactivated'][sim]=='None':
                plotting2D(G, sim, timesteps, datasets['activitydata'][sim], simInitActivity[sim], infos)
                plotting3D(G, sim, timesteps, datasets['activitydata'][sim], simInitActivity[sim], infos)
    
            else:
                timeplt=datasets['deactivated'][sim]
                plotting2D(G, sim, timeplt, datasets['activitydata'][sim], simInitActivity[sim], infos)
                plotting3D(G, sim, timeplt, datasets['activitydata'][sim], simInitActivity[sim], infos)
    
    
    ## Ad-hoc 3Dhtml representation to deepen
                
#    htmlsim=0
#    htmltimestep=4
#    htmlinfos='mainInfo'    ## 'chemicalInfo', 'electricalInfo' or 'mainInfo'.
#    
#    plotting3Dhtml(G, htmlsim, htmltimestep, masterInfo[htmlinfos]['activitydata'][htmlsim][htmltimestep], 
#                   simInitActivity[htmlsim], htmlinfos, nodesNumber)
#        
#    del datasets, sim
        
        
    ## Video generator
                
    for infos in masterInfo:
        for folder in folders:
            videoWriter(infos, folder)
            
    del folder, folders, infos
    
