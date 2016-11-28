"""
mostSimilarTS(inputFileName, howmany = 1)
-------------
- Expects the input file name (TS to be compared against) and howmany (the number of nearest neigbors to return)
- Returns the filenames of similar TS (the number of filenames returned depends on the input howmany)

Preconditions:
--------------
- VPDict should have been executed in buildVPDBforest and the same VPDict is used
- The same VPDict should be used because it contains k key-value pairs that contain information about the TS selected as VP
- target TS should be named in the format: 'ts_1.npy' ... to 'ts_1000.npy' 

Example input and output: 
-------------------------
>>> mostSimilarTS.mostSimilarTS('./ts_100.npy', 10)
Nodes in search region =  561
['./ts_100.npy', './ts_586.npy', './ts_106.npy', './ts_283.npy', './ts_478.npy', './ts_702.npy', './ts_248.npy', './ts_439.npy', './ts_800.npy', './ts_274.npy']


"""

import numpy as np
from selectVPs import selectVPs
import ArrayTimeSeries as ts
from TimeSeriesDistance import tsmaker, random_ts, stand, ccor, max_corr_at_phase, kernel_corr, kcorr_dist
import buildVPDBforest as VPDBforest
from buildVPDBforest import VPDict as VPDict

def mostSimilarTS(inputFileName, howmany = 1):
    # distance from target to each of the VPs
    distance = []
    # to store the database file name of VP (VPDBx.dbdb)
    VPDBList = []
    
    inputTS = ts.ArrayTimeSeries(np.load(inputFileName))
    inputstdTS =  stand(inputTS, inputTS.mean(), inputTS.std())
    
    # find most similar vantage point distance measure
    
    for i in range(len(VPDict)):
        vpTS = ts.ArrayTimeSeries(np.load(VPDict[i + 1][0]))
        VPstdTS =  stand(vpTS, vpTS.mean(), vpTS.std())
        VPDBList.append(VPDict[i + 1][1])
        distance.append(kcorr_dist(kernel_corr(inputstdTS, VPstdTS)))
    bestdist = min(distance)
    bestdistIndex = np.argmin(distance)
    bestVPDBfilename = VPDBList[bestdistIndex]
    bestVPDB = VPDBforest.VantagePointDB(bestVPDBfilename, VPDict[bestdistIndex + 1][0] )
    
    # define the area to search for 
    regionRadius = 2.0*bestdist
    
    #get the root level node
    root = bestVPDB._tree._follow(bestVPDB._tree._tree_ref)
    listofdistance = []
    nodesinregion = []
    # compare with the root node key first
    nodesinregion.append(root)
    
    # this is a breadth first search that prunes right side subtree that are outside the search region
    # each node within the region is examined. distance from the target TS is computed and stored in a list
    
    while nodesinregion:

        node = nodesinregion[0]
        if node is not None:
            nodeKey = bestVPDB.getNodeKey(node)
        # examine current node
        if  node is not None and (nodeKey > regionRadius):
            nodesinregion.append(bestVPDB.getLeftChildNode(node))
        elif node is not None and (nodeKey <= regionRadius):
            tsfilename = bestVPDB.get(nodeKey)
            # obtain the TS for the node and compute the distance between the TS 
            # at the node and the target TS
            TS = ts.ArrayTimeSeries(np.load(tsfilename))
            stdTS = stand(TS, TS.mean(), TS.std())
            distance = kcorr_dist(kernel_corr(stdTS, inputstdTS))
            
            listofdistance.append((distance, nodeKey))
            nodesinregion.append(bestVPDB.getLeftChildNode(node))
            nodesinregion.append(bestVPDB.getRightChildNode(node))
        # remove examined node
        nodesinregion.remove(node)
    print ("Nodes in search region = ",  len(listofdistance))
    return [bestVPDB.get(nodeKey) for (distance, nodeKey) in sorted(listofdistance)[0: howmany ]]