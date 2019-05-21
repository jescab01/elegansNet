#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 12:19:56 2019

@author: jescab01
"""

def plotting3D(G, sim, timesteps, activitydata, simInitActivity, infos, hpV):
        
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
    Representation in 3d with plotly offline
    '''
    import plotly.graph_objs as go
    import numpy as np
    import plotly.io as pio
    
    arrayx=np.asarray(posx)
    arrayy=np.asarray(posy)
    arrayz=np.asarray(posz)
    
    auxiliar_types=['Motor', 'Motor, Sensory', 'Interneuron, Motor',
                    'Interneuron, Sensory, Motor', 'Motor, Sensory']    
    
    for a in range(timesteps):
        color=[]
#        for b in range(302):
#            color.append(activitydata[a]['n'+str(b)])
        
        
###  Give different color to motor nodes  (NOT TESTED)

        for b in range(302):
            if G.node['n'+str(b)]['cell_type'] in auxiliar_types and activitydata[a]['n'+str(b)]==-30:
                color.append(-40)
            else: color.append(activitydata[a]['n'+str(b)])



        '''## realistic layout'''
        
        trace1= go.Scatter3d(x=arrayx,y=arrayy,z=arrayz,mode='markers',
                             marker=dict(size=5,
                                         color=color,
                                         cmax=-30,
                                         cmin=-75,
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
#                                         cmax=40,
#                                         cmin=hpV,
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
            
'''
Deepen. Plot one specific simulation at specific time in .html to deepen
'''

def plotting3Dhtml(G, sim, time, activitydata, simInitActivity, infos):   
    
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
        
        
    
    import plotly
    import plotly.graph_objs as go
    import numpy as np
    
    arrayx=np.asarray(posx)
    arrayy=np.asarray(posy)
    arrayz=np.asarray(posz)
    
    color=[]
    
    for a in range(302):
        if G.node['n'+str(a)]['cell_type']=='Motor' and activitydata[a]['n'+str(a)]==40:
            color.append(30)
        else: color.append(activitydata[a]['n'+str(a)])
    
    '''##realistic layout'''
    
    #trace1= go.Scatter3d(x=arrayx,y=arrayy,z=arrayz,mode='markers',
    #                     marker=dict(size=4,
    #                                 color=color,
#                                     cmax=40,
#                                     cmin=-80,
    #                                 colorscale='Viridis',
    #                                 line=dict(width=0.2),
    #                                 opacity=0.8))
    #
    #data=[trace1]
    #
    #layout=go.Layout(title=dict(text=str(infos)+'<br>'+
#                         'Initial node activation method = Random<br>' + 
#                         'Percentage of node activated at t0 = ' + str(simInitActivity) + '<br>'
#                         'Simulation number = ' + str(sim) + '<br>' +
#                         'Time = ' + str(a),
#                         font=dict(family='Arial', size=14)),
#                         #scene=dict(xaxis=dict(nticks=4,range=[-20,20]),
#                                    #yaxis=dict(nticks=4,range=[-300,450]),
#                                    #zaxis=dict(nticks=4,range=[-300,400])),
#                            width=1000, height=750, margin=dict(l=0,r=0,b=0,t=50))
    
    
    '''##spread layout'''
                                     
    trace1= go.Scatter3d(x=arrayx,y=arrayy,z=arrayz,mode='markers',
                         marker=dict(size=4,
                                     color=color,
                                     cmax=-30,
                                     cmin=-70,
                                     colorscale='Viridis',
                                     line=dict(width=0.5),
                                     opacity=0.8))
    
    data=[trace1]
    
    layout=go.Layout(title=dict(text=str(infos)+'<br>'+
                         'Initial node activation method = Random<br>' + 
                         'Percentage of node activated at t0 = ' + str(simInitActivity) + '<br>'
                         'Simulation number = ' + str(sim) + '<br>' +
                         'Time = ' + str(time),
                         font=dict(family='Arial', size=14)),
                         #scene=dict(xaxis=dict(nticks=4,range=[-20,20]),
                                    #yaxis=dict(nticks=4,range=[-300,450]),
                                    #zaxis=dict(nticks=4,range=[-300,400])),
                            width=1000, height=750, margin=dict(l=0,r=0,b=0,t=50))
    
    '''                                   ###                                      ''' 
                                
    
    fig=go.Figure(data=data,layout=layout)
    
    fig['layout']['scene'].update(go.layout.Scene(aspectmode='manual',
                   aspectratio=go.layout.scene.Aspectratio(x=1,y=1,z=0.3)))
    
    plotly.offline.plot(fig,filename="output/"+str(infos)+"Plots/plotly3D/sim"+str(sim)+'t'+str(time)+'.html')




