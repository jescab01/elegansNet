#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 14:12:18 2019

@author: jescab01
"""

#export strange cases
def exportAnomalies(mainInfo, simInitActivity, c):
    import pandas
    import time
    
    localtime = time.asctime( time.localtime(time.time()) )
    weirdActivity=pandas.DataFrame(mainInfo['activitydata'][0])
    weirdActivity.to_csv('output/weirdActivities/weirdActivity['+str(simInitActivity[0])+']['+str(c)+']'+localtime+'.csv')
    
    
    
        
                    