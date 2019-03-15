#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 11:01:36 2019

@author: jescab01
"""

def videoWriter(info, folder):

    if folder=='nx2D':
        nxWriter(info, folder)
    else: plotlyWriter(info, folder)
    
    
    # Generate VideoWriter for networkx plots
def nxWriter(info, folder):
    
    import cv2
    import glob
    import os
    
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output/'+str(info)+'Plots/'+str(folder)+'/0Nx'+str(info)+'.avi',fourcc, 3.0, (1296,720))
    
    image_list=glob.glob(f'output/'+str(info)+'Plots/'+str(folder)+'/*.jpg')
    sorted_images = sorted(image_list, key=os.path.getmtime)
    
    
    for file in sorted_images:
        image_frame=cv2.imread(file)
        out.write(image_frame)
    
    
    out.release()
    
    
    
    # Generate VideoWriter for plotly plots
def plotlyWriter(info, folder):
    
    import cv2
    import glob
    import os
    
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output/'+str(info)+'Plots/'+str(folder)+'/Plotly'+str(info)+'.avi',fourcc, 3.0, (1000,750))
    
    image_list=glob.glob(f'output/'+str(info)+'Plots/'+str(folder)+'/*.jpg')
    sorted_images = sorted(image_list, key=os.path.getmtime)
    
    
    for file in sorted_images:
        image_frame=cv2.imread(file)
        out.write(image_frame)
    
    
    out.release()

