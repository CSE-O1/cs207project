"""
 Purpose: to generate (using tsmaker) a set of 1000 time series, each stored in a file
 Function expects input of n which is the number of timeseries to be generated, with the default of 1000.
 Output is n timeseries saved in the format of 'ts_1.npy' ... to 'ts_1000.npy' in the current working directory
"""
from TimeSeriesDistance import tsmaker
import numpy as np
def generateAndStoreTimeSeries(n = 1000):
    for i in range(n):
        fileName = 'data2/ts_'+str(i+1)+'.npy'
        timeSeries = tsmaker(0.5, 0.1, 0.01)
        np.save(fileName, timeSeries)

