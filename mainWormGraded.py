'''

Specifying functions for whole connectome

'''

def infoG(G, sim_no):
    mainInfoGraded={'activitydata':{}, 'consecutiveAct': {}, 'deactivated': {}}
    for sim in range(sim_no):
        mainInfoGraded['activitydata'][sim]={}
        mainInfoGraded['consecutiveAct'][sim]={}
        mainInfoGraded['deactivated'][sim]='None'       
    return mainInfoGraded
        


def mainWormGraded(G, sim, timesteps, initActivity, activityDic, activity, mainInfoGraded, c, hpTest, Psens, envActivation, att):
    
    from envInput import randomSensInput
    
         ### assign initial activity to nodes as attribute   
    for i in range(302):
        G.node['n'+str(i)]['mV']=initActivity[sim]['n'+str(i)]
        mainInfoGraded['consecutiveAct'][sim]['n'+str(i)]=[]
            
        
        ### run specific simulation for timesteps
    for i in range(timesteps):
        chemtime = i-4          ## Define temporal difference between electrical and chemical synapses
        if chemtime>=0:    
            chemdata = []
            for a in range(302):
                chemdata.append(mainInfoGraded['activitydata'][sim][chemtime]['n'+str(a)])
            if sum(activity)/302 == -70:
                if sum(chemdata)/302 == -70:
                    mainInfoGraded['deactivated'][sim]= i
                    print('Main network deactivation at: simulation ' + str(sim) + ', time ' + str(i) +'.')
                    break
                
        mainInfoGraded['activitydata'][sim][i] = activityDic
        hpTest[sim][i]=[]
        hpTest[sim][i]=single_time_step(G, sim, i, mainInfoGraded, chemtime, c, hpTest[sim][i], att)
        
        if (i+1)%4==0:  ##If remainder of timesteps/4 is 0, run environmental input. Oscillatory input.
            envActivation=randomSensInput(G, Psens, sim, envActivation, i)
            
        activity, activityDic = getActivity(G)
    
    ##removing last row of hpTest=='inRRP' 
    for a in range(302):
        if mainInfoGraded['deactivated'][sim]=='None':
            for i in range(len(hpTest[sim][timesteps-1])):
                if hpTest[sim][timesteps-1][i]=='inRRP':
                    hpTest[sim][timesteps-1].remove('inRRP')
                    break
    
        else: 
            timeplt=mainInfoGraded['deactivated'][sim]-1
            for i in range(len(hpTest[sim][timeplt])):
                if hpTest[sim][timeplt][i]=='inRRP':
                    hpTest[sim][timeplt].remove('inRRP')
                    break

    return mainInfoGraded, hpTest, envActivation



def getActivity(G):
    activity = []
    activityDic={}
    for n,nbrs in G.adj.items():
        activity.append(G.node[n]['mV'])
    for i in range(302):
        activityDic['n'+str(i)]=G.node['n'+str(i)]['mV']
    return activity, activityDic



def single_time_step(G, sim, timestep, mainInfoGraded, chemtime, c, hpTest, att):  
    
    integral= [0] * G.number_of_nodes()
    m = 0
    
    for n,nbrs in G.adj.items():
        if G.node[n]['mV'] == -30: 		
            G.node[n]['mV'] = -65
            
        elif G.node[n]['mV'] == -65: 		
            G.node[n]['mV'] = -69
            hpTest.append('inATT')        
		
		#determine input from neighbours and decide if the integral is sufficient for firing	
            ## first for nodes that were active last oscillation and are sensory, compute adaptation process
        elif G.node[n]['mV']==-69 :
            for nbr,eattr in nbrs.items():
                if chemtime >= 0: 
                    if eattr['Esyn']=='True' and eattr['Csyn']=='True':
                        if mainInfoGraded['activitydata'][sim][timestep][nbr]==-30 and mainInfoGraded['activitydata'][sim][chemtime][nbr] == -30:
                            integral[m] +=  G.node[nbr]['exin'] * abs(mainInfoGraded['activitydata'][sim][timestep][nbr])*c * eattr['EnormWeight'] * (att**G.node[n]['consecutiveAct'])
                            integral[m] +=  G.node[nbr]['exin'] * abs(mainInfoGraded['activitydata'][sim][chemtime][nbr])*c * eattr['CnormWeight'] * (att**G.node[n]['consecutiveAct'])
                            
                        if mainInfoGraded['activitydata'][sim][timestep][nbr]==-30:
                            integral[m] +=  G.node[nbr]['exin'] * abs(mainInfoGraded['activitydata'][sim][timestep][nbr])*c * eattr['EnormWeight'] * (att**G.node[n]['consecutiveAct'])
                            
                        if mainInfoGraded['activitydata'][sim][chemtime][nbr] == -30:
                            integral[m] +=  G.node[nbr]['exin'] * abs(mainInfoGraded['activitydata'][sim][chemtime][nbr])*c * eattr['CnormWeight'] * (att**G.node[n]['consecutiveAct'])
                            
    
                    elif eattr['Esyn'] == 'True' and mainInfoGraded['activitydata'][sim][timestep][nbr]==-30:
                        integral[m] +=  G.node[nbr]['exin'] * abs(mainInfoGraded['activitydata'][sim][timestep][nbr])*c * eattr['EnormWeight'] * (att**G.node[n]['consecutiveAct'])
                    
                    elif eattr['Csyn'] == 'True' and mainInfoGraded['activitydata'][sim][chemtime][nbr] == -30:
                        integral[m] +=  G.node[nbr]['exin'] * abs(mainInfoGraded['activitydata'][sim][chemtime][nbr])*c * eattr['CnormWeight'] * (att**G.node[n]['consecutiveAct'])
                        
                        
                else: 
                    if eattr['Esyn'] == 'True' and mainInfoGraded['activitydata'][sim][timestep][nbr]==-30:
                        integral[m] +=  G.node[nbr]['exin'] * abs(mainInfoGraded['activitydata'][sim][timestep][nbr])*c * eattr['EnormWeight'] * (att**G.node[n]['consecutiveAct'])
              
                    
            if integral[m]+G.node[n]['mV'] > -60:
                G.node[n]['mV'] = -30
                G.node[n]['consecutiveAct']+=1
              #  print(G.node[n]['consecutiveAct'])
                mainInfoGraded['consecutiveAct'][sim][n].append(timestep)
                
            
            elif timestep <= 3 or (mainInfoGraded['activitydata'][sim][timestep-3][n]==-69 and mainInfoGraded['activitydata'][sim][timestep-2][n]==-69 and mainInfoGraded['activitydata'][sim][timestep-1][n]==-69):       ## mantain adaptation period during 4 timesteps
                G.node[n]['mV']=-70         ## from attenuation period to rest
                hpTest.append('rrp2rest')
                G.node[n]['consecutiveAct']=0
                
             ## now for nodes that were not active last ocillation and active but not sensory ones.
        elif G.node[n]['mV']==-70 :
            for nbr,eattr in nbrs.items():
                if chemtime >= 0: 
                    if eattr['Esyn']=='True' and eattr['Csyn']=='True':
                        if mainInfoGraded['activitydata'][sim][timestep][nbr]==-30 and mainInfoGraded['activitydata'][sim][chemtime][nbr] == -30:
                            integral[m] +=  G.node[nbr]['exin'] * abs(mainInfoGraded['activitydata'][sim][timestep][nbr])*c * eattr['EnormWeight']
                            integral[m] +=  G.node[nbr]['exin'] * abs(mainInfoGraded['activitydata'][sim][chemtime][nbr])*c * eattr['CnormWeight']
                            
                        if mainInfoGraded['activitydata'][sim][timestep][nbr]==-30:
                            integral[m] +=  G.node[nbr]['exin'] * abs(mainInfoGraded['activitydata'][sim][timestep][nbr])*c * eattr['EnormWeight']
                            
                        if mainInfoGraded['activitydata'][sim][chemtime][nbr] == -30:
                            integral[m] +=  G.node[nbr]['exin'] * abs(mainInfoGraded['activitydata'][sim][chemtime][nbr])*c * eattr['CnormWeight']
                            
    
                    elif eattr['Esyn'] == 'True' and mainInfoGraded['activitydata'][sim][timestep][nbr]==-30:
                        integral[m] +=  G.node[nbr]['exin'] * abs(mainInfoGraded['activitydata'][sim][timestep][nbr])*c * eattr['EnormWeight']
                    
                    elif eattr['Csyn'] == 'True' and mainInfoGraded['activitydata'][sim][chemtime][nbr] == -30:
                        integral[m] +=  G.node[nbr]['exin'] * abs(mainInfoGraded['activitydata'][sim][chemtime][nbr])*c * eattr['CnormWeight']
                        
                        
                else: 
                    if eattr['Esyn'] == 'True' and mainInfoGraded['activitydata'][sim][timestep][nbr]==-30:
                        integral[m] +=  G.node[nbr]['exin'] * abs(mainInfoGraded['activitydata'][sim][timestep][nbr])*c * eattr['EnormWeight']
              
            
            if integral[m]+G.node[n]['mV'] > -60:
                G.node[n]['mV'] = -30
            
            elif G.node[n]['mV']==-69:
                G.node[n]['mV']=-70
                
                
		#for tracking the integral list		
        m += 1
       
    return hpTest

