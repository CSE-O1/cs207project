"""
mostSimilarTS(inputFileName, howmany = 1)
-------------

Parameters
----------
- Input file name (TS to be compared against)
- VPDict: a dictionary which the key is just numeric index from 1 to n, and value is a tuple (vptsfilename, name of vantage point database filename))
- howmany (the number of nearest neigbors to return)

Returns
-------
- Returns the filenames of similar TS (the number of filenames returned depends on the input howmany)

Preconditions:
--------------
- VPDict should have been built in buildVPDBforest and the attribute VPDict is used
- The same VPDict should be used because it contains k key-value pairs that contain information about the TS selected as VP
- target TS should be named in the format: 'ts_1.npy' ... to 'ts_1000.npy' 

WARNINGS
--------
- File directory for timeseries assumes UNIX OS syntax 
- Will raise exception if timeseries files do not exist in current directory

"""

import numpy as np
import timeseries.ArrayTimeSeries as ts
from timeseries.TimeSeriesDistance import tsmaker, random_ts, stand, ccor, max_corr_at_phase, kernel_corr, kcorr_dist
import timeseries.buildVPDBforest as VPDBforest

def mostSimilarTS(inputFileName, VPDict, howmany = 1):
    # to store the distance from target to each of the VPs
    distance = []
    # to store the database file name of VP (VPDBx.dbdb) so that the VP can be identified
    VPDBList = []
    
    inputTS = ts.ArrayTimeSeries(np.load(inputFileName))
    inputstdTS =  stand(inputTS, inputTS.mean(), inputTS.std())
    
    # find most similar vantage point distance measure
    
    for i in range(len(VPDict)):
        # load vantage point TS, note increment in VPDict key is because it is indexed from 1-20
        vpTS = ts.ArrayTimeSeries(np.load(VPDict[i + 1][0]))
        VPstdTS =  stand(vpTS, vpTS.mean(), vpTS.std())
        VPDBList.append(VPDict[i + 1][1])
        distance.append(kcorr_dist(kernel_corr(inputstdTS, VPstdTS)))

    # locate the best VP to the target TS
    bestdist = min(distance)
    bestdistIndex = np.argmin(distance)
    bestVPDBfilename = VPDBList[bestdistIndex]

    # retrieve 
    bestVPDB = VPDBforest.VantagePointDB(bestVPDBfilename, VPDict[bestdistIndex + 1][0], VPDict )
    
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
            dist = kcorr_dist(kernel_corr(stdTS, inputstdTS))
            
            listofdistance.append((dist, nodeKey))
            nodesinregion.append(bestVPDB.getLeftChildNode(node))
            nodesinregion.append(bestVPDB.getRightChildNode(node))
        # remove examined node
        nodesinregion.remove(node)
    
    #print ("Nodes in search region = ",  len(listofdistance))
    #print ("Most similar TS sorted from most similar TS onwards = " )
    answerList = [bestVPDB.get(nk) for (d, nk) in sorted(listofdistance)[0: howmany ]]
    print (answerList)
    return answerList