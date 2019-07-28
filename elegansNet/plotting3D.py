#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 12:19:56 2019

@author: jescab01
"""

def plotting3D(G, sim, timesteps, activitydata, simInitActivity, infos):
        
    '''
    listing positions 3D
    '''
    posx=list(range(G.number_of_nodes()))
    for i in range(G.number_of_nodes()):
        posx[i] = G.node['n'+str(i)]['soma_posx']
    
    #listing y positions
    posy=list(range(G.number_of_nodes()))
    for i in range(G.number_of_nodes()):
        posy[i] = G.node['n'+str(i)]['soma_posy']
    
    #listing z positions
    posz=list(range(G.number_of_nodes()))
    for i in range(G.number_of_nodes()):
        posz[i] = G.node['n'+str(i)]['soma_posz']
        
       
    
    
    '''
    Representation in 3d with plotly offline
    '''
    import plotly.graph_objs as go
    import numpy as np
    import plotly.io as pio
    
    arrayx=np.asarray(posx)
    arrayy=np.asarray(posy)
    arrayz=np.asarray(posz)

    
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
                color.append('white')
            if activitydata[a]['n'+str(b)]==-69:
                color.append('whitesmoke')
            if activitydata[a]['n'+str(b)]==-65:
                color.append('gainsboro')
            if activitydata[a]['n'+str(b)]+int(G.node['n'+str(b)]['cellType_group'])==-29:
                color.append('indianred')
            if activitydata[a]['n'+str(b)]+int(G.node['n'+str(b)]['cellType_group'])==-28:
                color.append('salmon')
            if activitydata[a]['n'+str(b)]+int(G.node['n'+str(b)]['cellType_group'])==-27:
                color.append('olive')#'yellowgreen'
            if activitydata[a]['n'+str(b)]+int(G.node['n'+str(b)]['cellType_group'])==-26:
                color.append('orchid')
            if activitydata[a]['n'+str(b)]+int(G.node['n'+str(b)]['cellType_group'])==-25:
                color.append('hotpink')
            if activitydata[a]['n'+str(b)]+int(G.node['n'+str(b)]['cellType_group'])==-24:
                color.append('cornflowerblue')
            if activitydata[a]['n'+str(b)]+int(G.node['n'+str(b)]['cellType_group'])==-23:
                color.append('royalblue')



        '''## realistic layout'''
        
        trace1= go.Scatter3d(x=arrayx,y=arrayy,z=arrayz,mode='markers',
                             marker=dict(size=5,
                                         color=color,
                                         cmax=-30,
                                         cmin=-70,
                                         colorscale='Viridis',
                                         line=dict(width=0.2),
                                         opacity=0.8))
        
        data=[trace1]
        
        layout=go.Layout(title=dict(text=str(infos)+'<br>'+
                         'Initial node activation method = Random<br>' + 
                         'Percentage of node activated at t0 = ' + str(simInitActivity) + '<br>'
                         'Simulation number = ' + str(sim) + '<br>' +
                         'Time = ' + str(a),
                         font=dict(family='Arial', size=14)),
                            width=1400, height=900, margin=dict(l=0,r=0,b=0,t=0),
                            scene=dict(aspectmode='manual',
                                       aspectratio=go.layout.scene.Aspectratio(x=0.6,y=2.2,z=0.9)))
        
        fig=go.Figure(data=data,layout=layout)
        
           
        
        '''## spread layout'''
                                         
#        trace1= go.Scatter3d(x=arrayx,y=arrayy,z=arrayz,mode='markers',
#                             marker=dict(size=6,
#                                         color=color,
#                                         colorscale='Viridis',
#                                         cmax=-30,
#                                         cmin=-70,
#                                         line=dict(width=0.5),
#                                         opacity=0.7))
#        
#        data=[trace1]
#        
#        layout=go.Layout(title=dict(text=str(infos)+'<br>'+
#                         'Initial node activation method = Random<br>' + 
#                         'Percentage of node activated at t0 = ' + str(simInitActivity) + '<br>'
#                         'Simulation number = ' + str(sim) + '<br>' +
#                         'Time = ' + str(a),
#                         font=dict(family='Arial', size=14)),
#                            width=1400, height=900, margin=dict(l=0,r=0,b=0,t=0),
#                            scene=dict(aspectmode='manual', 
#                                       aspectratio=go.layout.scene.Aspectratio(x=1.8,y=1.8,z=0.45)))
#        
#        fig=go.Figure(data=data,layout=layout)

        
        '''                          ###                          '''


        
        pio.write_image(fig, "output/"+str(infos)+"Plots/plotly3D/sim"+str(sim)+'t'+str(a)+'.jpg')
        
        fig=None