#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 12:19:56 2019

@author: jescab01
"""
import networkx as nx

G = nx.read_graphml("elegansNet/data/elegans.herm_connectome.graphml")


'''
listing positions 3D
'''
#def plot3D():
#listing x positions
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

#    import random
#    x=[]
#    for i in range(302):
#        x.append(random.randrange(0,150,50))

import copy

colors=copy.deepcopy(activitydata)

for a,b in colors.items():
    for c,d in b.items():
        for e,f in d.items():
            if f==100:
                d[e]=2
            elif f==50:
                d[e]=1
            else: d[e]=0



'''
Representation in 3d with plotly offline
'''
import plotly
import plotly.graph_objs as go
import numpy as np
import plotly.io as pio

arrayx=np.asarray(posx)
arrayy=np.asarray(posy)
arrayz=np.asarray(posz)


for a in range(simulation_no):
    for b in range(timesteps):
        color=[]
        for c in range(302):            
            color.append(colors[a][b]['n'+str(c)])

        '''##realistic layout'''
        
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
        
        
        '''##spread layout'''
                                         
        trace1= go.Scatter3d(x=arrayx,y=arrayy,z=arrayz,mode='markers',
                             marker=dict(size=4,
                                         color=color,
                                         colorscale='Viridis',
                                         line=dict(width=0.5),
                                         opacity=0.8))
        
        data=[trace1]
        
        layout=go.Layout(scene=dict(xaxis=dict(nticks=4,range=[-20,20]),
                                    yaxis=dict(nticks=4,range=[-300,450]),
                                    zaxis=dict(nticks=4,range=[-300,400])),
                            width=700,margin=dict(l=0,r=0,b=0,t=0))
        
        '''###'''
                                    
        
        fig=go.Figure(data=data,layout=layout)
        
        fig['layout']['scene'].update(go.layout.Scene(aspectmode='manual',
                       aspectratio=go.layout.scene.Aspectratio(x=1,y=1,z=1)))
        
        pio.write_image(fig, '3Dplots/sim'+str(a)+'t'+str(b)+'.jpg')
        
        
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




