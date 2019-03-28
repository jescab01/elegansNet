'''

Specifying functions for 'electrical' connectome

'''

def infoE(G, sim_no):
    electricalInfo={'activitydata':{}, 'fireCount': {}, 'deactivated': {}}
    for sim in range(sim_no):
        electricalInfo['activitydata'][sim]={}
        electricalInfo['fireCount'][sim]={}
        electricalInfo['deactivated'][sim]='None'
        for n,nbrs in G.adj.items():
            electricalInfo['fireCount'][sim][n] = 0
    return electricalInfo
        


def electricalWorm(G, sim, timesteps, initActivity, activityDic, activity, electricalInfo, hpV, c):
    
         ### assign initial activity to nodes as attribute   
    for i in range(302):
        G.node['n'+str(i)]['activity']=initActivity[sim]['n'+str(i)]
        
        ### run specific simulation for timesteps
    for i in range(timesteps):
        if sum(activity)/302 == -70:
            electricalInfo['deactivated'][sim] = i
            print('Electrical network deactivation at: simulation ' + str(sim) + ', time ' + str(i) +'.')
            break
        electricalInfo['activitydata'][sim][i] = activityDic
        single_time_step(G, sim, electricalInfo, hpV, c)
        activity, activityDic = getActivity(G)
    
    return electricalInfo

def getActivity(G):
    activity = []
    activityDic={}
    for n,nbrs in G.adj.items():
        activity.append(G.node[n]['activity'])
    for i in range(302):
        activityDic['n'+str(i)]=G.node['n'+str(i)]['activity']
    return activity, activityDic

    


def single_time_step(G, sim, electricalInfo, hpV, c):
    integral= [0] * G.number_of_nodes()
    m = 0
    for n,nbrs in G.adj.items():
        if G.node[n]['activity'] == 40:       #decay of activity in 1 time steps as absolute refractory period
            G.node[n]['activity'] = hpV
		
        
		#determine input from neighbours and decide if the integral is sufficient for firing
        elif G.node[n]['activity']!=40:
            for nbr,eattr in nbrs.items():
                if eattr['Esyn'] == 'True':
                    integral[m] +=  G.node[nbr]['exin'] * G.node[nbr]['activity'] * c * eattr['EnormWeight']
		
            if integral[m]+G.node[n]['activity'] > -55:
                G.node[n]['activity'] = 40
                electricalInfo['fireCount'][sim][n] += 1
            
            elif G.node[n]['activity']==hpV:
                G.node[n]['activity']= -70

                
		#for tracking the integral list		
        m += 1
       