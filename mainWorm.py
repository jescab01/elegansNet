'''

Specifying functions for whole connectome

'''

def infoM(G, sim_no):
    mainInfo={'activitydata':{}, 'fireCount': {}, 'deactivated': {}}
    for sim in range(sim_no):
        mainInfo['activitydata'][sim]={}
        mainInfo['fireCount'][sim]={}
        mainInfo['deactivated'][sim]='None'
        for n,nbrs in G.adjacency_iter():
            mainInfo['fireCount'][sim][n] = 0
    return mainInfo
        


def mainWorm(G, sim, timesteps, initActivity, activityDic, activity, mainInfo, c):
    
         ### assign initial activity to nodes as attribute   
    for i in range(302):
        G.node['n'+str(i)]['activity']=initActivity[sim]['n'+str(i)]
        
        ### run specific simulation for timesteps
    for i in range(timesteps):
        chemtime = i-2
        if chemtime>=0:
            chemdata = []
            for a in range(302):
                chemdata.append(mainInfo['activitydata'][sim][chemtime]['n'+str(a)])
            if sum(activity)==0:
                if sum(chemdata) == 0:
                    mainInfo['deactivated'][sim]= i
                    print('Main network deactivation at: simulation ' + str(sim) + ', time ' + str(i) +'.')
                    break
        mainInfo['activitydata'][sim][i] = activityDic
        single_time_step(G, sim, mainInfo, sim, chemtime, c)
        activity, activityDic = getActivity(G)
    
    return mainInfo

def getActivity(G):
    activity = []
    activityDic={}
    for n,nbrs in G.adjacency_iter():
        activity.append(G.node[n]['activity'])
    for i in range(302):
        activityDic['n'+str(i)]=G.node['n'+str(i)]['activity']
    return activity, activityDic

    


def single_time_step(G, iteration, mainInfo, sim, chemtime, c):
    integral= [0] * G.number_of_nodes()
    m = 0
    for n,nbrs in G.adjacency_iter():
        if G.node[n]['activity'] == 100: 		#decay of activity in 1 time steps as absolute refractory period
            G.node[n]['activity'] -= 115
            
		
		#determine input from neighbours and decide if the integral is sufficient for firing	
        elif G.node[n]['activity']!=100:
            for nbr,eattr in nbrs.items():
                if chemtime >= 0: 
                    if eattr['Esyn']=='True' and eattr['Csyn']=='True':
                        if G.node[nbr]['activity']==100 and mainInfo['activitydata'][sim][chemtime][nbr] == 100:
                            integral[m] +=  G.node[nbr]['exin'] * G.node[nbr]['activity']*c * eattr['EnormWeight']
                            integral[m] +=  G.node[nbr]['exin'] * mainInfo['activitydata'][sim][chemtime][nbr]*c * eattr['CnormWeight']
                            
                        if G.node[nbr]['activity']==100:
                            integral[m] +=  G.node[nbr]['exin'] * G.node[nbr]['activity']*c * eattr['EnormWeight']
                            
                        if mainInfo['activitydata'][sim][chemtime][nbr] == 100:
                            integral[m] +=  G.node[nbr]['exin'] * mainInfo['activitydata'][sim][chemtime][nbr]*c * eattr['CnormWeight']
                            
    
                    elif eattr['Esyn'] == 'True' and G.node[nbr]['activity']==100:
                        integral[m] +=  G.node[nbr]['exin'] * G.node[nbr]['activity']*c * eattr['EnormWeight']
                    
                    elif eattr['Csyn'] == 'True' and mainInfo['activitydata'][sim][chemtime][nbr] == 100:
                        integral[m] +=  G.node[nbr]['exin'] * G.node[nbr]['activity']*c * eattr['CnormWeight']
                        
                        
                else: 
                    if eattr['Esyn'] == 'True' and G.node[nbr]['activity']==100:
                        integral[m] +=  G.node[nbr]['exin'] * G.node[nbr]['activity']*c * eattr['EnormWeight']
              
                    
            if integral[m] > 13:
                G.node[n]['activity'] = 100
                mainInfo['fireCount'][iteration][n] += 1 
                
            elif G.node[n]['activity'] == -15: 		#relative refractory period in one timestep
                G.node[n]['activity'] = 0
                
		#for tracking the integral list		
        m += 1
       


