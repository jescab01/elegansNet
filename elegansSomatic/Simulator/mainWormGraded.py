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
    for i in range(G.number_of_nodes()):
        G.node['n'+str(i)]['mV']=initActivity[sim]['n'+str(i)]
        mainInfoGraded['consecutiveAct'][sim]['n'+str(i)]=[]
            
        
        ### run specific simulation for timesteps
    for i in range(timesteps):
        chemtime = i-3          ## Define temporal difference between electrical and chemical synapses
        if chemtime>=0:    
            chemdata = []
            for a in range(G.number_of_nodes()):
                chemdata.append(mainInfoGraded['activitydata'][sim][chemtime]['n'+str(a)])
            if sum(activity)/G.number_of_nodes() == -70:
                if sum(chemdata)/G.number_of_nodes() == -70:
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
    for a in range(G.number_of_nodes()):
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
    for n in G.nodes():
        activity.append(G.node[n]['mV'])
    for i in range(G.number_of_nodes()):
        activityDic['n'+str(i)]=G.node['n'+str(i)]['mV']
    return activity, activityDic



def single_time_step(G, sim, timestep, mainInfoGraded, chemtime, c, hpTest, att):  
    
    integral= [0] * G.number_of_nodes()
    m = 0
    
    for n in G.nodes():
        if G.node[n]['mV'] == -30: 		
            G.node[n]['mV'] = -65
            
        elif G.node[n]['mV'] == -65: 		
            G.node[n]['mV'] = -69
            hpTest.append('inATT')        
		
		#determine input from neighbours and decide if the integral is sufficient for firing	
            ## first for nodes that were active last oscillation and are sensory, compute adaptation process
        elif G.node[n]['mV']==-69 :
            for p in G.predecessors(n):
                if chemtime >= 0: 
                    if G[p][n]['Esyn']=='True' and G[p][n]['Csyn']=='True':
                        if mainInfoGraded['activitydata'][sim][timestep][p]==-30 and mainInfoGraded['activitydata'][sim][chemtime][p] == -30:
                            integral[m] +=  G.node[p]['exin'] * abs(mainInfoGraded['activitydata'][sim][timestep][p])*c * G[p][n]['EnormWeight'] * (att**G.node[n]['consecutiveAct'])
                            integral[m] +=  G.node[p]['exin'] * abs(mainInfoGraded['activitydata'][sim][chemtime][p])*c * G[p][n]['CnormWeight'] * (att**G.node[n]['consecutiveAct'])
                            
                        if mainInfoGraded['activitydata'][sim][timestep][p]==-30:
                            integral[m] +=  G.node[p]['exin'] * abs(mainInfoGraded['activitydata'][sim][timestep][p])*c * G[p][n]['EnormWeight'] * (att**G.node[n]['consecutiveAct'])
                            
                        if mainInfoGraded['activitydata'][sim][chemtime][p] == -30:
                            integral[m] +=  G.node[p]['exin'] * abs(mainInfoGraded['activitydata'][sim][chemtime][p])*c * G[p][n]['CnormWeight'] * (att**G.node[n]['consecutiveAct'])
                            
    
                    elif G[p][n]['Esyn'] == 'True' and mainInfoGraded['activitydata'][sim][timestep][p]==-30:
                        integral[m] +=  G.node[p]['exin'] * abs(mainInfoGraded['activitydata'][sim][timestep][p])*c * G[p][n]['EnormWeight'] * (att**G.node[n]['consecutiveAct'])
                    
                    elif G[p][n]['Csyn'] == 'True' and mainInfoGraded['activitydata'][sim][chemtime][p] == -30:
                        integral[m] +=  G.node[p]['exin'] * abs(mainInfoGraded['activitydata'][sim][chemtime][p])*c * G[p][n]['CnormWeight'] * (att**G.node[n]['consecutiveAct'])
                        
                        
                else: 
                    if G[p][n]['Esyn'] == 'True' and mainInfoGraded['activitydata'][sim][timestep][p]==-30:
                        integral[m] +=  G.node[p]['exin'] * abs(mainInfoGraded['activitydata'][sim][timestep][p])*c * G[p][n]['EnormWeight'] * (att**G.node[n]['consecutiveAct'])
              
                    
            if integral[m]+G.node[n]['mV'] > -60:
                G.node[n]['mV'] = -30
                G.node[n]['consecutiveAct']+=1
                mainInfoGraded['consecutiveAct'][sim][n].append(timestep)
                
            
            elif timestep <= 3 or (mainInfoGraded['activitydata'][sim][timestep-3][n]==-69 and mainInfoGraded['activitydata'][sim][timestep-2][n]==-69 and mainInfoGraded['activitydata'][sim][timestep-1][n]==-69):       ## mantain adaptation period during 4 timesteps
                G.node[n]['mV']=-70         ## from attenuation period to rest
                hpTest.append('rrp2rest')
                G.node[n]['consecutiveAct']=0
                
             ## now for nodes that were not active last ocillation and active but not sensory ones.
        elif G.node[n]['mV']==-70 :           
            for p in G.predecessors(n):
                if chemtime >= 0: 
                    if G[p][n]['Esyn']=='True' and G[p][n]['Csyn']=='True':
                        if mainInfoGraded['activitydata'][sim][timestep][p]==-30 and mainInfoGraded['activitydata'][sim][chemtime][p] == -30:
                            integral[m] +=  G.node[p]['exin'] * abs(mainInfoGraded['activitydata'][sim][timestep][p])*c * G[p][n]['EnormWeight']
                            integral[m] +=  G.node[p]['exin'] * abs(mainInfoGraded['activitydata'][sim][chemtime][p])*c * G[p][n]['CnormWeight']
                            
                        if mainInfoGraded['activitydata'][sim][timestep][p]==-30:
                            integral[m] +=  G.node[p]['exin'] * abs(mainInfoGraded['activitydata'][sim][timestep][p])*c * G[p][n]['EnormWeight']
                            
                        if mainInfoGraded['activitydata'][sim][chemtime][p] == -30:
                            integral[m] +=  G.node[p]['exin'] * abs(mainInfoGraded['activitydata'][sim][chemtime][p])*c * G[p][n]['CnormWeight']
                            
    
                    elif G[p][n]['Esyn'] == 'True' and mainInfoGraded['activitydata'][sim][timestep][p]==-30:
                        integral[m] +=  G.node[p]['exin'] * abs(mainInfoGraded['activitydata'][sim][timestep][p])*c * G[p][n]['EnormWeight']

                    
                    
                    elif G[p][n]['Csyn'] == 'True' and mainInfoGraded['activitydata'][sim][chemtime][p] == -30:
                        integral[m] +=  G.node[p]['exin'] * abs(mainInfoGraded['activitydata'][sim][chemtime][p])*c * G[p][n]['CnormWeight']
                        
                        
                else: 
                    if G[p][n]['Esyn'] == 'True' and mainInfoGraded['activitydata'][sim][timestep][p]==-30:
                        integral[m] +=  G.node[p]['exin'] * abs(mainInfoGraded['activitydata'][sim][timestep][p])*c * G[p][n]['EnormWeight']
            
            
            if integral[m]+G.node[n]['mV'] > -60:
                G.node[n]['mV'] = -30
            
            elif G.node[n]['mV']==-69:
                G.node[n]['mV']=-70

                
		#for tracking the integral list		
        m += 1
       
    return hpTest