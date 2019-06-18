'''

Specifying functions for 'Chemical' connectome

'''


###prepare chemicalInfo for storage
def infoC(G, sim_no):
    chemicalInfo={'activitydata':{}, 'fireCount': {}, 'deactivated': {}}
    for sim in range(sim_no):
        chemicalInfo['activitydata'][sim]={}
        chemicalInfo['fireCount'][sim]={}
        chemicalInfo['deactivated'][sim]='None'
        for n,nbrs in G.adj.items():
            chemicalInfo['fireCount'][sim][n] = 0
    return chemicalInfo
        

    ### Start simulation    
def chemicalWorm(G, sim, timesteps, initActivity, activityDic, activity, chemicalInfo, hpV, c):
    
         ### assign initial activity to nodes as attribute   
    for i in range(302):
        G.node['n'+str(i)]['activity']=initActivity[sim]['n'+str(i)]
        
        ### run specific simulation for timesteps
    for i in range(timesteps):
        chemtime=i-2
        if chemtime>=0:
            chemdata=[]
            for a in range(302):
                chemdata.append(chemicalInfo['activitydata'][sim][chemtime]['n'+str(a)])
            if sum(chemdata)/302 == -70:
                if sum(activity)/302==-70:
                    chemicalInfo['deactivated'][sim] = i
                    print('Chemical network deactivation at: simulation ' + str(sim) + ', time ' + str(i) +'.')
                    break
            
        chemicalInfo['activitydata'][sim][i] = activityDic
        single_time_step(G, sim, chemicalInfo, chemtime, hpV, c)
        activity, activityDic = getActivity(G)
    
    return chemicalInfo
    


def getActivity(G):
    activity = []
    activityDic={}
    for n,nbrs in G.adj.items():
        activity.append(G.node[n]['activity'])
    for i in range(302):
        activityDic['n'+str(i)]=G.node['n'+str(i)]['activity']
    return activity, activityDic
        

def single_time_step(G, sim, chemicalInfo, chemtime, hpV, c):
    integral= [0] * G.number_of_nodes()
    m = 0
    for n,nbrs in G.adj.items():
        if G.node[n]['activity'] == 40:       #decay of activity in 1 time steps as absolute refractory period
            G.node[n]['activity'] = hpV
             
        elif G.node[n]['activity'] != 40:
            for nbr,eattr in nbrs.items():
                if eattr['Csyn'] == 'True' and chemtime>=0:
                    integral[m] +=  G.node[nbr]['exin'] * chemicalInfo['activitydata'][sim][chemtime][nbr] * c * eattr['CnormWeight']
            
            if integral[m]+G.node[n]['activity'] > -55:
                G.node[n]['activity'] = 40
                chemicalInfo['fireCount'][sim][n] += 1
                
            elif G.node[n]['activity']==hpV:
                G.node[n]['activity']= -70
                
        
        m += 1
       
        




