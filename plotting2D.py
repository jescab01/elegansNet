#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 12:19:56 2019

@author: jescab01
"""

def plotting2D(G, sim, timesteps, activitydata, simInitActivity, infos, hpV):
    
    import networkx as nx
    import matplotlib.pyplot as plt
    
    
    #pos = nx.nx_agraph.graphviz_layout(G)
    pos=nx.kamada_kawai_layout(G)
    ### Determine node size by node degree
    node_sizes = [0] * G.number_of_nodes()
    i = 0
    for n,nbrs in G.adj.items():
        node_sizes[i] = G.degree(n) * 5
        i += 1
    
    
    ### Loop for plotting each simulation's timestep

    for a in range(timesteps):
        color=[]
        for b in range(302):
            color.append(activitydata[a]['n'+str(b)])
            
        plt.figure(figsize=(11,11))
        nx.draw(G, pos, node_color = color, node_size=node_sizes, width=1,
                style='dotted', arrows=False, cmap=plt.cm.Blues, vmax=40, vmin=hpV)


        font = {'fontname'   : 'DejaVu Sans',
	            'color'      : 'k',
	            'fontweight' : 'bold',
	            'fontsize'   : 16}

        plt.title("C.Elegans Neural Activity", font)

	    # change font and write text (using data coordinates)
        font = {'fontname'   : 'Helvetica',
	    'color'      : 'r',
	    'fontweight' : 'bold',
	    'fontsize'   : 15}

	    #type of activation
        plt.figtext(0.97, 0.97, str(infos) + ' - InitMethod: Random',
	             horizontalalignment='right',
	             transform=plt.gca().transAxes)
        	    
        #percentage of initial activation
        plt.figtext(0.97, 0.94,  "Initial activity = " + str(simInitActivity), 
	             horizontalalignment='right',
	             transform=plt.gca().transAxes)

	    #iteration
        plt.figtext(0.97, 0.91,  "Simulation = " + str(sim),
	             horizontalalignment='right',
	             transform=plt.gca().transAxes)
	    #time
        plt.figtext(0.97, 0.88,  "t = " + str(a),
	             horizontalalignment='right',
	             transform=plt.gca().transAxes)

        plt.savefig("output/"+str(infos)+"Plots/nx2D/2Dsim"+str(sim)+"step"+str(a)+".jpg")
        plt.close()

