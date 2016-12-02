""" Module for File Storage Manager.
This module defines the FileStorageManager class.

Classes
-------
FileStorageManager(StorageManagerInterface):
    Define the FileStorageManager class for managing storage of timeseries data to database files.

Methods
-------
__init__(self):
    Constructor of FileStorageManager, loading IDs for timeseries in the database
gen_id(self):
    Generate an ID for a timeseries
ts2nparray(self, t):
    Convert a timeseries to a 2D np array in float64, returning a 2D np array
     containing time and value
store(self, id, t):
    Store the given timeseries t in database using the input id, returning the same timeseries
size(self, id):
    Get the size of timeseries using the given ID, returning int size of the timeseries
get(self, id):
    Get the timeseries using an given ID, returning the timeseries of the given ID

"""

import os
import numpy as np
import pickle
from storagemanager.SMInterface import StorageManagerInterface
from timeseries.ArrayTimeSeries import ArrayTimeSeries


class FileStorageManager(StorageManagerInterface):
    """ FileStorageManager(StorageManagerInterface):
    Define the FileStorageManager class for managing storage of timeseries data to database files.

    Methods
    -------
    __init__(self):
        Constructor of FileStorageManager, loading IDs for timeseries in the database
    gen_id(self):
        Generate an ID for a timeseries
    ts2nparray(self, t):
        Convert a timeseries to a 2D np array in float64, returning a 2D np array
         containing time and value
    store(self, id, t):
        Store the given timeseries t in database using the input id, returning the same timeseries
    size(self, id):
        Get the size of timeseries using the given ID, returning int size of the timeseries
    get(self, id):
        Get the timeseries using an given ID, returning the timeseries of the given ID

    """
    def __init__(self):
        """
        Constructor of FileStorageManager
        """
        try:
            with open('data/id.pkl', 'rb') as f:
                self._id = pickle.load(f)
        except FileNotFoundError:
            self._id = set()

    def gen_id(self):
        """
        Generate an ID for a timeseries
        :return: ID of a timeseries
        """
        gid = 0
        while gid in self._id: gid += 1
        self._id.add(gid)
        return gid

    def ts2nparray(self, t):
        """
        Convert a timeseries to a 2D np array in float64
        :param t: input timeseries
        :return: a 2D np array containing time and value
        """
        return np.vstack((t.times(), t.values())).astype(np.float64)

    def store(self, id, t):
        """
        Store the given timeseries t in database using the input id
        :param id: assigned ID of timeseries,
        :param t: the timeseries to store
        :type id: int or string
        :type t: SizedContainerTimeSeriesInterface
        :return: the same timeseries
        :rtype: SizedContainerTimeSeriesInterface
        """
        np.save('data/ts.'+str(id), self.ts2nparray(t))
        self._id.add(id)
        with open('data/id.pkl', 'wb') as f:
            pickle.dump(self._id, f)
        return t

    def size(self, id):
        """
        Get the size of timeseries using the given ID
        :param id: ID of timeseries
        :type id: int or string
        :return: size of the timeseries
        :rtype: int
        """
        if not os.path.exists('data/ts.'+str(id)+'.npy'):
            raise ValueError("Timeseries with ID={0} does not exist.".format(id))
        return len(np.load('data/ts.'+str(id)+'.npy')[0])

    def get(self, id):
        """
        Get the timeseries using an given ID
        :param id: ID of timeseries
        :type id: int or string
        :return: timeseries of the given ID
        :rtype: SizedContainerTimeSeriesInterface
        """
        if not os.path.exists('data/ts.' + str(id) + '.npy'):
            raise ValueError("Timeseries with ID={0} does not exist.".format(id))
        tsnparray = np.load('data/ts.' + str(id) + '.npy')
        return ArrayTimeSeries(tsnparray[1], tsnparray[0])
