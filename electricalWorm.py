'''

Specifying functions for 'electrical' connectome

'''

def infoE(G, sim_no):
    electricalInfo={'activitydata':{}, 'fireCount': {}, 'deactivated': {}}
    for sim in range(sim_no):
        electricalInfo['activitydata'][sim]={}
        electricalInfo['fireCount'][sim]={}
        electricalInfo['deactivated'][sim]='None'
        for n,nbrs in G.adjacency_iter():
            electricalInfo['fireCount'][sim][n] = 0
    return electricalInfo
        


def electricalWorm(G, sim, timesteps, refractoryPeriod, initActivity, activityDic, activity, electricalInfo):
    
         ### assign initial activity to nodes as attribute   
    for i in range(302):
        G.node['n'+str(i)]['activity']=initActivity[sim]['n'+str(i)]
        
        ### run specific simulation for timesteps
    for i in range(timesteps):
        if sum(activity) == 0:
            electricalInfo['deactivated'][sim] = i
            print('Electrical network deactivation at: simulation ' + str(sim) + ', time ' + str(i) +'.')
            break
        electricalInfo['activitydata'][sim][i] = activityDic
        single_time_step(G, sim, refractoryPeriod, electricalInfo)
        activity, activityDic = getActivity(G)
    
    return electricalInfo

def getActivity(G):
    activity = []
    activityDic={}
    for n,nbrs in G.adjacency_iter():
        activity.append(G.node[n]['activity'])
    for i in range(302):
        activityDic['n'+str(i)]=G.node['n'+str(i)]['activity']
    return activity, activityDic

    


def single_time_step(G, iteration, refractory, electricalInfo):
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
					if eattr['Esyn'] == 'True':
						#summing the activity input into a node and store integral into a list
						integral[m] +=  G.node[nbr]['exin'] * G.node[nbr]['activity'] * eattr['EnormWeight']
			#this threshold activation limit is chosen based on the proportion of neuron action potential			
			if integral[m] > 2:
				G.node[n]['activity'] = 100
				electricalInfo['fireCount'][iteration][n] += 1 
		#for tracking the integral list		
		m += 1
       