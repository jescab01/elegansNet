'''

Specifying functions for whole connectome

'''

def infoM(G, sim_no):
    mainInfo={'activitydata':{}, 'fireCount': {}, 'deactivated': {}}
    for sim in range(sim_no):
        mainInfo['activitydata'][sim]={}
        mainInfo['fireCount'][sim]={}
        mainInfo['deactivated'][sim]='None'
        for n,nbrs in G.adj.items():
            mainInfo['fireCount'][sim][n] = 0            
    return mainInfo
        


def mainWorm(G, sim, timesteps, initActivity, activityDic, activity, mainInfo, hpV, c, hpTest):
    
  
    
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
            if sum(activity)/302 == -70:
                if sum(chemdata)/302 == -70:
                    mainInfo['deactivated'][sim]= i
                    print('Main network deactivation at: simulation ' + str(sim) + ', time ' + str(i) +'.')
                    break
        mainInfo['activitydata'][sim][i] = activityDic
        hpTest[sim][i]=[]
        hpTest[sim][i]=single_time_step(G, sim, mainInfo, chemtime, hpV, c, hpTest[sim][i])
        activity, activityDic = getActivity(G)
    
    ##removing last row of hpTest=='inRRP' 
    for a in range(302):
        if mainInfo['deactivated'][sim]=='None':
            for i in range(len(hpTest[sim][timesteps-1])):
                if hpTest[sim][timesteps-1][i]=='inRRP':
                    hpTest[sim][timesteps-1].remove('inRRP')
                    break
    
        else: 
            timeplt=mainInfo['deactivated'][sim]-1
            for i in range(len(hpTest[sim][timeplt])):
                if hpTest[sim][timeplt][i]=='inRRP':
                    hpTest[sim][timeplt].remove('inRRP')
                    break
                

            
            
    return mainInfo, hpTest

def getActivity(G):
    activity = []
    activityDic={}
    for n,nbrs in G.adj.items():
        activity.append(G.node[n]['activity'])
    for i in range(302):
        activityDic['n'+str(i)]=G.node['n'+str(i)]['activity']
    return activity, activityDic

    


def single_time_step(G, sim, mainInfo, chemtime, hpV, c, hpTest):  
    
    integral= [0] * G.number_of_nodes()
    m = 0
    
    for n,nbrs in G.adj.items():
        if G.node[n]['activity'] == 40: 		
            G.node[n]['activity'] = hpV
            hpTest.append('inRRP')
		
		#determine input from neighbours and decide if the integral is sufficient for firing	
        elif G.node[n]['activity']!=40:
            for nbr,eattr in nbrs.items():
                if chemtime >= 0: 
                    if eattr['Esyn']=='True' and eattr['Csyn']=='True':
                        if G.node[nbr]['activity']==40 and mainInfo['activitydata'][sim][chemtime][nbr] == 40:
                            integral[m] +=  G.node[nbr]['exin'] * G.node[nbr]['activity']*c * eattr['EnormWeight']
                            integral[m] +=  G.node[nbr]['exin'] * mainInfo['activitydata'][sim][chemtime][nbr]*c * eattr['CnormWeight']
                            
                        if G.node[nbr]['activity']==40:
                            integral[m] +=  G.node[nbr]['exin'] * G.node[nbr]['activity']*c * eattr['EnormWeight']
                            
                        if mainInfo['activitydata'][sim][chemtime][nbr] == 40:
                            integral[m] +=  G.node[nbr]['exin'] * mainInfo['activitydata'][sim][chemtime][nbr]*c * eattr['CnormWeight']
                            
    
                    elif eattr['Esyn'] == 'True' and G.node[nbr]['activity']==40:
                        integral[m] +=  G.node[nbr]['exin'] * G.node[nbr]['activity']*c * eattr['EnormWeight']
                    
                    elif eattr['Csyn'] == 'True' and mainInfo['activitydata'][sim][chemtime][nbr] == 40:
                        integral[m] +=  G.node[nbr]['exin'] * G.node[nbr]['activity']*c * eattr['CnormWeight']
                        
                        
                else: 
                    if eattr['Esyn'] == 'True' and G.node[nbr]['activity']==40:
                        integral[m] +=  G.node[nbr]['exin'] * G.node[nbr]['activity']*c * eattr['EnormWeight']
              
                    
            if integral[m]+G.node[n]['activity'] > -55:
                G.node[n]['activity'] = 40
                mainInfo['fireCount'][sim][n] += 1 
                
                
            elif G.node[n]['activity'] == hpV: 		#relative refractory period in one timestep
                G.node[n]['activity'] = -70
                hpTest.append('rrp2rest')
                
		#for tracking the integral list		
        m += 1
       
    return hpTest

