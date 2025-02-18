#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 18:11:03 2019

@author: jescab01
"""

## Mantain network activity by randomly activating sensors  
def randomSensInput(G, Psens, sim, envActivation, timestep):
    import random
    
    sensWhole={'chemosensor':{'headL':['n4','n6','n39','n41','n43','n45','n47','n49','n121','n123','n125'],
                         'tailL':['n139','n141'],
                         'headR':['n5','n7','n40','n42','n44','n46','n48','n50','n122','n124','n126'],
                         'tailR':['n140','n142']},  
          'odorsensor':{'headL':['n72','n74','n43','n76'], 'headR':['n73','n75','n44','n77']},
          'oxygen': {'headL':['n78','n232','n208'], 'headR':['n27','n79','n233','n209'],
                     'tailR':['n149']},   
          'nociceptor':{'head':['n43','n44']},
          'osmoceptor':{'head':['n43','n44']},
          'thermosensor':{'head':['n8','n9','n76','n77'],'body':['n152','n153','n111','n112']},
          'mechanosensor':{'body':['n22','n71','n154','n23','n137','n24'],
                           'body1':['n138','n152','n153','n111','n112','n115','n116','n119','n120'],
                           'headL':['n2','n82','n84','n117','n129','n131','n133','n43','n121','n123','n125'],
                           'headR':['n3','n83','n85','n118','n130','n132','n134','n44','n122','n124','n126'],
                           'tail':['n145','n146']},           
          'propioSomatic':{'body':['n86','n87','n88','n89','n90','n91','n92','n93','n94','n95'],
                           'body1':['n96','n97','n98','n99','n100','n101','n238','n239','n240'],
                           'body2':['n241','n242','n243','n244','n245','n246','n247','n248'],
                           'body3':['n249','n250','n251','n252','n253','n254','n255','n256'],
                           'body4':['n257','n258','n259','n260','n152','n153','n111','n112'],
                           'tail':['n108','n150','n151', 'n147','n148']},                  
          'propioHead':{'L':['n201','n203','n218','n220','n222','n224','n226','n228', 'n234','n236'],
                        'R':['n202','n204','n219','n221','n223','n225','n227','n229', 'n235','n237']},         
          'propioTail':{'tail':['n63','n136','n161','n145','n146', 'n147','n148']}}
          
        
    sensHead={'chemosensor':{'headL':['n4','n6','n39','n41','n43','n45','n47','n49','n121','n123','n125'],
                         'headR':['n5','n7','n40','n42','n44','n46','n48','n50','n122','n124','n126']},
          'odorsensor':{'headL':['n72','n74','n43','n76'], 'headR':['n73','n75','n44','n77']},
          'oxygen': {'headL':['n78','n232','n208'], 'headR':['n27','n79','n233','n209']},
          'nociceptor':{'head':['n43','n44']},
          'osmoceptor':{'head':['n43','n44']},
          'thermosensor':{'head':['n8','n9','n76','n77']},
          'mechanosensor':{'headL':['n2','n82','n84','n117','n129','n131','n133','n43','n121','n123','n125'],
                           'headR':['n3','n83','n85','n118','n130','n132','n134','n44','n122','n124','n126']},                  
          'propioHead':{'L':['n201','n203','n218','n220','n222','n224','n226','n228', 'n234','n236'],
                        'R':['n202','n204','n219','n221','n223','n225','n227','n229', 'n235','n237']}}         
 
    
    
    if random.random() < Psens:
        envActivation[sim]['active'].append(timestep)
        for group, subG in sensWhole.items():            ### Define dictionary to use   
            if random.random() < 0.4:
                envActivation[sim]['activeG'].append(str(timestep)+group)
                for subgroup, nodes in subG.items():
                    if random.random() < 0.6:
                        envActivation[sim]['activeSG'].append(str(timestep)+group+subgroup)
                        for node in nodes:
                            if random.random() < 0.8:
                                G.node[node]['mV']=-30
                                envActivation[sim]['activeNode'].append(str(timestep)+group+subgroup+node)
                                
    return envActivation