#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 19:58:17 2019

@author: jescab01
"""

import networkx as nx

G = nx.read_graphml("data/elegans.herm_connectome.graphml")


timesteps = 25
simulation_no = 2
refractoryPeriod=1

electricalWorm()
chemicalWorm()
mainWorm()