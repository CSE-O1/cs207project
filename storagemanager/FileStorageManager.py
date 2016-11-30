import numpy as np
import os
from SMInterface import StorageManagerInterface
from timeseries.ArrayTimeSeries import ArrayTimeSeries

class FileStorageManager(StorageManagerInterface):

    def __init__(self):
        """
        Constructor of FileStorageManager
        """
        try:
            self._id = np.load('data/id.npz')
        except:
            self._id = {}

    def gen_id(self):
        gid = 0
        while gid in self._id: gid += 1
        self._id.add(gid)
        return gid

    def ts2nparray(self, t):
        return np.vstack((t.times(), t.values())).astype(np.float64)

    def store(self, id, t):
        """
        Store the given timeseries in database
        :param id: Assigned ID of timeseries,
        :param t: The timeseries to store
        :type id: int or string
        :type t: SizedContainerTimeSeriesInterface
        :return: The same timeseries
        :rtype: SizedContainerTimeSeriesInterface
        """
        np.save('data/ts.'+str(id), self.ts2nparray(t))
        self._id.add(id)
        np.save('data/id.npz', self._id)
        return t

    def size(self, id):
        """
        Get the size of timeseries with given ID
        :param id: ID of timeseries
        :type id: int or string
        :return: Size of the timeseries
        :rtype: int
        """
        if not os.path.exists('data/ts.'+str(id)+'.npz'):
            raise ValueError("Timeseries with ID={0} does not exist.".format(id))
        return len(np.load('data/ts.'+str(id)+'.npz')[0])

    def get(self, id):
        """
        Get the timeseries of given ID
        :param id: ID of timeseries
        :type id: int or string
        :return: Timeseries of given ID
        :rtype: SizedContainerTimeSeriesInterface
        """
        if not os.path.exists('data/ts.' + str(id) + '.npz'):
            raise ValueError("Timeseries with ID={0} does not exist.".format(id))
        tsnparray = np.load('data/ts.' + str(id) + '.npz')
        return ArrayTimeSeries(tsnparray[1], tsnparray[0])