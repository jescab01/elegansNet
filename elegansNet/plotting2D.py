#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 12:19:56 2019

@author: jescab01
"""

def plotting2D(G, sim, timesteps, activitydata, simInitActivity, infos):
    
    import networkx as nx
    import matplotlib.pyplot as plt
    
    
    #pos = nx.nx_agraph.graphviz_layout(G)
    pos=nx.kamada_kawai_layout(G)
    ### Determine node size by node degree
    node_sizes = [0] * G.number_of_nodes()
    i = 0
    for n in G.nodes():
        node_sizes[i] = G.degree(n) * 5
        i += 1
    
    
    
    ### Loop for plotting each simulation's timestep

    for a in range(timesteps):
        color=[]
        for b in range(G.number_of_nodes()):
            
            ## Original colours
#            if activitydata[a]['n'+str(b)]==-70:
#                color.append(-70)
#            if activitydata[a]['n'+str(b)]==-69:
#                color.append(-69)
#            if activitydata[a]['n'+str(b)]==-65:
#                color.append(-65)
#            if activitydata[a]['n'+str(b)]+int(G.node['n'+str(b)]['cellType_group'])==-29:
#                color.append(-29)
#            if activitydata[a]['n'+str(b)]+int(G.node['n'+str(b)]['cellType_group'])==-28:
#                color.append(-28)
#            if activitydata[a]['n'+str(b)]+int(G.node['n'+str(b)]['cellType_group'])==-27:
#                color.append(-27)#'olive'
#            if activitydata[a]['n'+str(b)]+int(G.node['n'+str(b)]['cellType_group'])==-26:
#                color.append(-26)
#            if activitydata[a]['n'+str(b)]+int(G.node['n'+str(b)]['cellType_group'])==-25:
#                color.append(-25)
#            if activitydata[a]['n'+str(b)]+int(G.node['n'+str(b)]['cellType_group'])==-24:
#                color.append(-24)
#            if activitydata[a]['n'+str(b)]+int(G.node['n'+str(b)]['cellType_group'])==-23:
#                color.append(-23)             
                
            ## Colors by cell type
            if activitydata[a]['n'+str(b)]==-70:
                color.append('w')
            if activitydata[a]['n'+str(b)]==-69:
                color.append('whitesmoke')
            if activitydata[a]['n'+str(b)]==-65:
                color.append('gainsboro')
            if activitydata[a]['n'+str(b)]+int(G.node['n'+str(b)]['cellType_group'])==-29:
                color.append('indianred')
            if activitydata[a]['n'+str(b)]+int(G.node['n'+str(b)]['cellType_group'])==-28:
                color.append('salmon')
            if activitydata[a]['n'+str(b)]+int(G.node['n'+str(b)]['cellType_group'])==-27:
                color.append('yellowgreen')#'olive'
            if activitydata[a]['n'+str(b)]+int(G.node['n'+str(b)]['cellType_group'])==-26:
                color.append('orchid')
            if activitydata[a]['n'+str(b)]+int(G.node['n'+str(b)]['cellType_group'])==-25:
                color.append('hotpink')
            if activitydata[a]['n'+str(b)]+int(G.node['n'+str(b)]['cellType_group'])==-24:
                color.append('cornflowerblue')
            if activitydata[a]['n'+str(b)]+int(G.node['n'+str(b)]['cellType_group'])==-23:
                color.append('royalblue')
            
        plt.figure(figsize=(8,13))
        nx.draw(G, pos, node_color = color, node_size=node_sizes, width=1,
                style='dotted', arrows=False, cmap=plt.cm.Blues, vmax=-30, vmin=-70)


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
