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
    posx=list(range(302))
    for i in range(302):
        posx[i] = G.node['n'+str(i)]['soma_posx']
    
    #listing y positions
    posy=list(range(302))
    for i in range(302):
        posy[i] = G.node['n'+str(i)]['soma_posy']
    
    #listing z positions
    posz=list(range(302))
    for i in range(302):
        posz[i] = G.node['n'+str(i)]['soma_posz']
        
    
    '''
    generating colour from activity
    '''
#        
#    import copy
#    
#    colors=copy.deepcopy(activitydata)
#    
#    for times, nodescolors in colors.items():
#        for node, color in nodescolors.items():
#            if color==100:
#                color=5
#            elif color==60:
#                color=4
#            elif color==50:
#                color=3
#            elif color==30:
#                color=2
#            elif color==10:
#                color=1
#            else: color=0
    
    
    
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
        for b in range(302):            
            color.append(activitydata[a]['n'+str(b)])

        '''## realistic layout'''
        
#        trace1= go.Scatter3d(x=arrayx,y=arrayy,z=arrayz,mode='markers',
#                             marker=dict(size=2,
#                                         color=color,
#                                         colorscale='Viridis',
#                                         line=dict(width=0.2),
#                                         opacity=0.8))
#        
#        data=[trace1]
#        
#        layout=go.Layout(scene=dict(xaxis=dict(nticks=4,range=[-450,450]),
#                                    yaxis=dict(nticks=4,range=[-450,450]),
#                                    zaxis=dict(nticks=4,range=[-450,450])),
#                            width=700,margin=dict(l=0,r=0,b=0,t=0))
        
        
        '''## spread layout'''
                                         
        trace1= go.Scatter3d(x=arrayx,y=arrayy,z=arrayz,mode='markers',
                             marker=dict(size=4,
                                         color=color,
                                         colorscale='Viridis',
                                         colorbar=dict(title='Colorbar'),
                                         line=dict(width=0.5),
                                         opacity=0.8))
        
        data=[trace1]
        
        layout=go.Layout(title=dict(text=str(infos)+'<br>'+
                         'Initial node activation method = Random<br>' + 
                         'Percentage of node activated at t0 = ' + str(simInitActivity) + '<br>'
                         'Simulation number = ' + str(sim) + '<br>' +
                         'Time = ' + str(a),
                         font=dict(family='Arial', size=14)),
                         #scene=dict(xaxis=dict(nticks=4,range=[-20,20]),
                                    #yaxis=dict(nticks=4,range=[-300,450]),
                                    #zaxis=dict(nticks=4,range=[-300,400])),
                            width=1000, height=750, margin=dict(l=0,r=0,b=0,t=50))

        
        '''                          ###                          '''
                                    
        
        fig=go.Figure(data=data,layout=layout)
        
        fig['layout']['scene'].update(go.layout.Scene(aspectmode='manual',
                       aspectratio=go.layout.scene.Aspectratio(x=1,y=1,z=0.25)))
        
        pio.write_image(fig, "output/"+str(infos)+"Plots/plotly3D/sim"+str(sim)+'t'+str(a)+'.jpg')
        
        
            
    '''
    Deepen. Plot one specific simulation at specific time in .html to deepen
    '''
    
    #sim=1
    #time=1
    #color=[]
    #
    #for c in range(302):            
    #    color.append(colors[sim][time]['n'+str(c)])
    #
    #'''##realistic layout'''
    #
    ##trace1= go.Scatter3d(x=arrayx,y=arrayy,z=arrayz,mode='markers',
    ##                     marker=dict(size=4,
    ##                                 color=color,
    ##                                 colorscale='Viridis',
    ##                                 line=dict(width=0.2),
    ##                                 opacity=0.8))
    ##
    ##data=[trace1]
    ##
    ##layout=go.Layout(scene=dict(xaxis=dict(nticks=4,range=[-450,450]),
    ##                            yaxis=dict(nticks=4,range=[-450,450]),
    ##                            zaxis=dict(nticks=4,range=[-450,450])),
    ##                    width=700,margin=dict(l=0,r=0,b=0,t=0))
    #
    #
    #'''##spread layout'''
    #                                 
    #trace1= go.Scatter3d(x=arrayx,y=arrayy,z=arrayz,mode='markers',
    #                     marker=dict(size=4,
    #                                 color=color,
    #                                 colorscale='Viridis',
    #                                 line=dict(width=0.5),
    #                                 opacity=0.8))
    #
    #data=[trace1]
    #
    #layout=go.Layout(scene=dict(xaxis=dict(nticks=4,range=[-20,20]),
    #                            yaxis=dict(nticks=4,range=[-300,450]),
    #                            zaxis=dict(nticks=4,range=[-300,400])),
    #                    width=700,margin=dict(l=0,r=0,b=0,t=0))
    #
    #'''###'''
    #                            
    #
    #fig=go.Figure(data=data,layout=layout)
    #
    #fig['layout']['scene'].update(go.layout.Scene(aspectmode='manual',
    #               aspectratio=go.layout.scene.Aspectratio(x=1,y=1,z=1)))
    #
    #plotly.offline.plot(fig,filename='3Dplots/sim'+str(a)+'time'+str(b)+'.jpg')




