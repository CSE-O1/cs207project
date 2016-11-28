"""
Randomly chose 20 vantage points from the 1000 TS generated, and create 20 database indexes
and return dictionary with numeric key from 1 - 20 and values are (name of TS selected as VP, name of database) 

Example of returned value: {('ts_806.npy', 'VPDB1.dbdb'), ...}

Precondition:
------------
The name of the timeseries generated should follow the format 'ts_1.npy' ... to 'ts_1000.npy' 
"""
import numpy as np

def selectVPs(n = 20):
    VPindex = np.random.choice(np.arange(1, 1001), size = n, replace = False)
    VPDict = {}
    for i in range(n):
        VPfileName = 'ts_'+ str(VPindex[i]) +'.npy'
        VPDB = 'VPDB'+ str(i + 1) + '.dbdb'
        VPDict[i+1] =  (VPfileName, VPDB)
    return VPDict

