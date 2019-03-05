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
        


def mainWorm(G, sim, timesteps, refractoryPeriod, initActivity, activityDic, activity, mainInfo):
    
         ### assign initial activity to nodes as attribute   
    for i in range(302):
        G.node['n'+str(i)]['activity']=initActivity[sim]['n'+str(i)]
        
        ### run specific simulation for timesteps
    for i in range(timesteps):
        if sum(activity) == 0:
            mainInfo['deactivated'][sim]= i
            print('Main network deactivation at: simulation ' + str(sim) + ', time ' + str(i) +'.')
            break
        mainInfo['activitydata'][sim][i] = activityDic
        single_time_step(G, sim, refractoryPeriod, mainInfo)
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

    


def single_time_step(G, iteration, refractory, mainInfo):
    integral= [0] * G.number_of_nodes()
    m = 0
    for n,nbrs in G.adjacency_iter():
        if G.node[n]['activity'] in [50,100]: 		#decay of activity in 2 time steps
            G.node[n]['activity'] -= 50
            
            
            current_activity = G.node[n]['activity']         #set refractory period if activity of the node just ended
            if current_activity == 0:
                G.node[n]['refractory'] = refractory

		#if the node is in the refractory period reduce its count	
        elif G.node[n]['refractory'] > 0:
            G.node[n]['refractory'] -= 1
        
        elif G.node[n]['activity'] in [33,66]:
            if G.node[n]['activity']==33:
                G.node[n]['activity']+=33
            elif G.node[n]['activity']==66:
                G.node[n]['activity']+=34

            
		
		#determine input from neighbours  and decide if the integral is sufficient for firing	
        else:
			#initialize integral
            for nbr,eattr in nbrs.items():
                if eattr['Esyn'] == 'True' and eattr['Csyn']=='True':
					#summing the activity input into a node and store integral into a list
                    integral[m] +=  G.node[nbr]['exin'] * G.node[nbr]['activity'] * eattr['EnormWeight']
                    integral[m] +=  G.node[nbr]['exin'] * G.node[nbr]['activity'] * eattr['CnormWeight']
                    
                    if integral[m] > 2:
                        G.node[n]['activity'] = 100
                        mainInfo['fireCount'][iteration][n] += 1 
                    
                    
                if eattr['Csyn'] == 'True':
                    integral[m] +=  G.node[nbr]['exin'] * G.node[nbr]['activity'] * eattr['CnormWeight']
                    
                    if integral[m] > 2:
                        G.node[n]['activity'] = 33
                        mainInfo['fireCount'][iteration][n] += 1 
                                        
                else: 
                    integral[m] +=  G.node[nbr]['exin'] * G.node[nbr]['activity'] * eattr['EnormWeight']
                    
                    if integral[m] > 2:
                        G.node[n]['activity'] = 100
                        mainInfo['fireCount'][iteration][n] += 1 
                
		#for tracking the integral list		
        m += 1
       


