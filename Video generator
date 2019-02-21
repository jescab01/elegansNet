#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 11:01:36 2019

@author: jescab01
"""

import cv2
import glob
import os

# Generate VideoWriter for networkx plots

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('nx.avi',fourcc, 3.0, (504,504))

image_list=glob.glob(f'elegansNet/imgChem/*.jpg')
sorted_images = sorted(image_list, key=os.path.getmtime)


for file in sorted_images:
    image_frame=cv2.imread(file)
    out.write(image_frame)


out.release()



# Generate VideoWriter for plotly plots

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('pltly.avi',fourcc, 3.0, (700,500))

image_list=glob.glob(f'3Dplots/*.jpg')
sorted_images = sorted(image_list, key=os.path.getmtime)


for file in sorted_images:
    image_frame=cv2.imread(file)
    out.write(image_frame)


out.release()

