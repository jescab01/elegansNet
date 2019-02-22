import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import csv
import pandas
import random
import pickle
import analysis as al
from math import log
try:
    import pygraphviz
    from networkx.drawing.nx_agraph import graphviz_layout
except ImportError:
    try:
        import pydotplus
        from networkx.drawing.nx_pydot import graphviz_layout
    except ImportError:
        raise ImportError("This example needs Graphviz and either "
                          "PyGraphviz or PyDotPlus")

#import Graph Data and set layout position
G = nx.read_graphml("data/elegans.herm_connectome.graphml")
pos = graphviz_layout(G, prog='sfdp', args='')


#initialise all perimeter nodes to have the parameter activity
def init_activity_perimeter():
	init_active_nodes = 0
	for n,nbrs in G.adjacency_iter():
		#node is inactive when degree of node is smaller than 12 (~19% node activation)
		if len(nbrs) < 12:
			G.node[n]['activity'] = 100
			init_active_nodes += 1
		#node is set to initialise as active when the degree of node is greater or equals to 10	
		else:
			G.node[n]['activity'] = 0
			
		#calculate the percentage of active nodes	
	percentage_init_active = float(init_active_nodes) / G.number_of_nodes()
	print(percentage_init_active)
	return percentage_init_active

#initialise all hub nodes to have the parameter activity
def init_activity_hub():
	init_active_nodes = 0
	for n,nbrs in G.adjacency_iter():
		#node is inactive when degree of node is larger than 30 (~18.6 percent node activation)
		if len(nbrs) > 30:
			G.node[n]['activity'] = 100
			init_active_nodes += 1
		#node is set to initialise as active when the degree of node is greater or equals to 10	
		else:
			G.node[n]['activity'] = 0
		#calculate the percentage of active nodes	
	percentage_init_active = float(init_active_nodes) / G.number_of_nodes()
	print(percentage_init_active)		
	return percentage_init_active

#initialise all nodes to have the parameter activity
def init_activity_random():
	init_active_nodes = 0
	for n,nbrs in G.adjacency_iter():
		#randomly activate roughly 20% of nodes
		if random.random() > 0.20:
			G.node[n]['activity'] = 0
		else:
			G.node[n]['activity'] = 100
			init_active_nodes += 1
		#calculate the percentage of active nodes	
	percentage_init_active = float(init_active_nodes) / G.number_of_nodes()
	print(percentage_init_active)
	return percentage_init_active

#initialize refractory period, all 
def init_refractory():
	init_active_nodes = 0
	for n,nbrs in G.adjacency_iter():
		G.node[n]['refractory'] = 0

def init_activationCount(iterations,activationData):
	for i in range(iterations):
		activationData[i] = {}
		for n,nbrs in G.adjacency_iter():
			activationData[i][n] = 0

#pull function to get the current activity of nodes used to visualize color of nodes in graph
def get_activity():
	activity_array = {}
	for n,nbrs in G.adjacency_iter():
		activity_array[n] = G.node[n]['activity']
	#print activity_array
	return activity_array

def get_activity_int():
	activity_array = [0] * G.number_of_nodes()
	i = 0
	for n,nbrs in G.adjacency_iter():
		activity_array[i] = G.node[n]['activity']
		i += 1
	return activity_array

def null_activity_int():
	activity_array = [0] * G.number_of_nodes()
	i = 0
	for n,nbrs in G.adjacency_iter():
		activity_array[i] = 0
		i += 1
	return activity_array

#create an array of the degree of each node which can be used in visualization for node size
def node_size_map():
	size_array = [0] * G.number_of_nodes()
	i = 0
	for n,nbrs in G.adjacency_iter():
		size_array[i] = G.degree(n) * 5
		i += 1
	return size_array


#interate over all nodes to propogate neural activity
def single_time_step(node_sizes,iteration,refractory):
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
			for nbr,attrs in nbrs.items():
					#'E' for electrical synapse
					if attrs['Csyn'] == 'True':
						#summing the activity input into a node and store integral into a list
						integral[m] +=  G.node[nbr]['exin'] * G.node[nbr]['activity'] * attrs['CnormWeight']
			#this threshold activation limit is chosen based on the proportion of neuron action potential			
			if integral[m] > 2:
				G.node[n]['activity'] = 100
				activationData[iteration][n] += 1 
		#for tracking the integral list		
		m += 1

	"""
	#print current activities and integral
	print get_activity()
	print integral
	"""

#main function for time iteration that contain all smaller functions
def time_itr(time,iteration,refractory):
    percentageActivation = init_activity_random()
    initActivity.append(percentageActivation)
    init_refractory()
    node_sizes = node_size_map()
    activations = {}
    for i in range(time):
        if sum(get_activity_int()) == 0:
            dieDownTime[iteration] = i
            died[iteration] = 1
            
            break
        
        activitydata[iteration][i] = get_activity()
        
        single_time_step(node_sizes, iteration, refractory)
        
    return activations
	
		

#importing the wormNet data from graphml file

#if __name__ == "__main__":

#a list that stores all the data from 
timesteps = 25
simulation_no = 2
activitydata = {}
dieDownTime = {}
activationData = {}
died = {}
initActivity=[]

#initialize activation data and set all nodes to 0
init_activationCount(simulation_no, activationData)
#define path lengths
hopcountdata = nx.all_pairs_shortest_path_length(G)

#inputing range for refractory
r = 1
for i in range(simulation_no):
	activitydata[i] = {}
	time_itr(timesteps,i,r)
'''
#save data in file
with open('data/randomResults/dieDownTime_chem.txt', 'wb') as f:
	pickle.dump(dieDownTime, f)
with open('data/randomResults/died_chem.txt', 'wb') as f:
	pickle.dump(died, f)
with open('data/randomResults/activityData_chem.txt', 'wb') as f:
	pickle.dump(activitydata, f)	
with open('data/randomResults/hopcountData_chem.txt', 'wb') as f:
	pickle.dump(hopcountdata, f)
'''

def frequencyCalcuation(G,timesteps, iteration, activations):
	frequency = {}
	for i in range(iteration):
		activationTotal = 0
		activeNodes = 0
		for n,nbrs in G.adjacency_iter():
			if activations[i][n] > 5:
				activationTotal += activations[i][n]
				activeNodes += 1
		if 	activeNodes > 0 and activationTotal > 0:
			frequency[i] = float(1)/(float(activationTotal)/float(activeNodes)/float(timesteps))		
	print (frequency)	
	return frequency	

frequencies = frequencyCalcuation(G,timesteps, simulation_no, activationData)
print (frequencies)
'''
with open('data/randomResults/frequencies.txt', 'wb') as f:
	pickle.dump(frequencies, f)	

with open('data/randomResults/frequencies.txt', 'rb') as f:
	pickle.load(f)	
'''
#load list from pickle		
"""
	with open('data/randomResults/test', 'rb') as f:
		mylist = pickle.load(f)
"""

	# figure setup
	#time iterate through the network
	#time_itr(5)

"""
def node_activity_map():
	activity_array = range(G.number_of_nodes())
	i = 0
	for n,nbrs in G.adjacency_iter():
		size_array[i] = G.degree(n) * 5
		i += 1
	return size_array
"""


"""
G=nx.star_graph(4)
pos=nx.spring_layout(G)
colors=range(4)
nx.draw(G,pos,node_color=['#A0CBE2',#EE1BE2',#EE1BE2',#EE1BE2'])


plt.figure(figsize=(12,12))
#pos=nx.spring_layout(G,iterations=100,scale=2.0)
n_colors=range(279)
e_colors=range(3225)
pos = graphviz_layout(G, prog='sfdp', args='')
nx.draw(G,pos,node_color=n_colors, node_cmap=plt.cm.Blues, edge_color=e_colors, edge_cmap=plt.cm.Reds, width=1, style='solid')
#nx.draw_spectral(G)
plt.savefig("test.png")
plt.show()

"""
			
"""
#test
for n,nbrs in G.adjacency_iter():
	#check if the node is active
	for nbr,eattr in nbrs.items():
			for attr, data in eattr.items():
				weight = data['weight']
				synapse = data['synapse_type']
				if synapse == 'E':
					print ('(%s, %s, %s, %d)' %(n, nbr, synapse, weight))
"""
"""
with open("data/neurogroup.csv") as f:
	c = csv.reader(f, delimiter=' ', skipinitialspace=True)
	for line in c:
		print line[0]
"""
"""
for i in G.nodes(data=True):
	data = i[1]
	NT_types = ['Ach', 'DA', 'GABA', '5-HT']

	if data['neurotransmitters'] == 'Ach':
	 G.
	elif 
"""


