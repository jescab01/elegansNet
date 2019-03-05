#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 12:19:56 2019

@author: jescab01
"""

def plotting2D(G, sim, timesteps, activitydata, simInitActivity, infos, hopcountdata):
    
    import networkx as nx
    from networkx.drawing.nx_agraph import graphviz_layout
    import matplotlib.pyplot as plt
    
    
    #G = nx.read_graphml("elegansNet/data/elegans.herm_connectome.graphml")
    pos = graphviz_layout(G, prog='sfdp', args='')
    
    ### Determine node size by node degree
    node_sizes = [0] * G.number_of_nodes()
    i = 0
    for n,nbrs in G.adjacency_iter():
        node_sizes[i] = G.degree(n) * 5
        i += 1
    
    
    ### Loop for plotting each timestep in one simulation
        

    for a in range(timesteps):
        color=[]
        for b in range(len(hopcountdata)):
            color.append(activitydata[a]['n'+str(b)])
            
        plt.figure(figsize=(7,7))
        nx.draw(G, pos, node_color = color, node_size=node_sizes, width=1,
                style='dotted', arrows=False, cmap=plt.cm.Blues)


        font = {'fontname'   : 'DejaVu Sans',
	            'color'      : 'k',
	            'fontweight' : 'bold',
	            'fontsize'   : 11}

        plt.title("C.Elegans Neural Activity", font)

	    # change font and write text (using data coordinates)
        font = {'fontname'   : 'Helvetica',
	    'color'      : 'r',
	    'fontweight' : 'bold',
	    'fontsize'   : 11}

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

