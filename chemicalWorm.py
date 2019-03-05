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
        for n,nbrs in G.adjacency_iter():
            chemicalInfo['fireCount'][sim][n] = 0
    return chemicalInfo
        

    ### Start simulation    
def chemicalWorm(G, sim, timesteps, refractoryPeriod, initActivity, activityDic, activity, chemicalInfo):
    
         ### assign initial activity to nodes as attribute   
    for i in range(302):
        G.node['n'+str(i)]['activity']=initActivity[sim]['n'+str(i)]
        
        ### run specific simulation for timesteps
    for i in range(timesteps):
        if sum(activity) == 0:
            chemicalInfo['deactivated'][sim] = i
            print('Chemical network deactivation at: simulation ' + str(sim) + ', time ' + str(i) +'.')
            break
        chemicalInfo['activitydata'][sim][i] = activityDic
        single_time_step(G, sim, refractoryPeriod, chemicalInfo)
        activity, activityDic = getActivity(G)
    
    return chemicalInfo
    


def getActivity(G):
    activity = []
    activityDic={}
    for n,nbrs in G.adjacency_iter():
        activity.append(G.node[n]['activity'])
    for i in range(302):
        activityDic['n'+str(i)]=G.node['n'+str(i)]['activity']
    return activity, activityDic
        

def single_time_step(G, iteration, refractory, chemicalInfo):
	integral= [0] * G.number_of_nodes()
	m = 0
	for n,nbrs in G.adjacency_iter():
		#check if the node is active
		#decay of activity of activated neuron in 2 time steps
		if G.node[n]['activity'] > 0:
			#an activated node will be activated for 2 timesteps
			G.node[n]['activity'] -= 50

			current_activity = G.node[n]['activity']
			#set refractory period if activity of the node just ended
			if current_activity == 0:
				#refractory period takes 3 time steps to end
				G.node[n]['refractory'] = refractory

		#if the node is in the refractory period reduce its count	
		elif G.node[n]['refractory'] > 0:
			G.node[n]['refractory'] -= 1
		
		#else determine the sum of all activities of its neighbouring nodes and decide if the integral is sufficient for firing	
		
		else:
			#initialize integral
			for nbr,eattr in nbrs.items():
				#for attr, data in eattr.items():
					#'E' for electrical synapse
					if eattr['Csyn'] == 'True':
						#summing the activity input into a node and store integral into a list
						integral[m] +=  G.node[nbr]['exin'] * G.node[nbr]['activity'] * eattr['CnormWeight']
			#this threshold activation limit is chosen based on the proportion of neuron action potential			
			if integral[m] > 2:
				G.node[n]['activity'] = 100
				chemicalInfo['fireCount'][iteration][n] += 1 
		#for tracking the integral list		
		m += 1
       
        




