import collections
import numpy as np
import numbers
from timeseries.TSInterface import SizedContainerTimeSeriesInterface
from storagemanager.FileStorageManager import FileStorageManager
from timeseries.ArrayTimeSeries import ArrayTimeSeries


class SMTimeSeries(SizedContainerTimeSeriesInterface):

    global fsm

    def __init__(self, times, values, fsm, id = None):
        """
        Constructor for SMTimeSeries
        :param fsm: File manager
        :type fsm: FileStorageManager
        :param times:
        :param values:
        :param id:
        """
        if not isinstance(values, collections.Sequence) and not isinstance(values, np.ndarray):
            raise TypeError("Input values must be Sequence")
        if not isinstance(times, collections.Sequence) and not isinstance(values, np.ndarray):
            raise TypeError("Input times must be Sequence")
        if len(times) != len(values):
            raise ValueError("Input values and times sequence must have the same length")
        if len(times) != len(set(times)):
            raise ValueError("Input times sequence must be unique")
        self._fsm = fsm
        if id == None:
            id = self._fsm.gen_id()
        self._id = id
        self._fsm.store(self._id, ArrayTimeSeries(values, times))

    @classmethod
    def from_db(cls, id, fsm):
        """
        Look up and fetch timeseries from the storage manager
        :param fsm: File manager
        :type fsm: FileStorageManager
        :param id: ID of timeseries
        :type id: int or string
        :return: Timeseries
        """
        return fsm.get(id)

    def __setitem__(self, index, value):
        """
        Set the value at the index time by value

        Update the values numpy array and the timeseries numpy array
        Raise "LookupError" when the index is out of boundary,
        and raise "TypeError" when the value is of illegal type
        """
        if not isinstance(index, numbers.Integral):
            raise TypeError("Input index must be integer")
        if index >= len(self._value):
            raise ValueError("Input index is out of boundary")
        ts = self._fsm.get(self._id)
        ts[index] = value
        self._fsm.store(self._id, ts)

    def __add__(self, other):
        """
        Add two SMTimeSeries' values at each time point

        other: another SMTimeSeries instance
        Return a new SMTimeSeries instance with the values being sum of both timeseries values
        Raise "TypeError" when other is not an instance of SMTimeSeries class,
        and raise "ValueError" when self's and other's times are not element-wise equal within a tolerance
        """
        if not isinstance(other, SMTimeSeries):
            raise TypeError("NotImplemented Error")
        ts = self._fsm.get(self._id) + other._fsm.get(other._id)
        return SMTimeSeries(ts._time, ts._value, self._fsm)

    def __sub__(self, other):
        """
        Subtract by other's value at each time point

        other: another SMTimeSeries instance
        Return a new SMTimeSeries instance with the values calculated by subtracting other's values from
        self's values
        Raise "TypeError" when other is not an instance of SMTimeSeries class,
        and raise "ValueError" when self's and other's times are not element-wise equal within a tolerance
        """
        if not isinstance(other, SMTimeSeries):
            raise TypeError("NotImplemented Error")
        ts = self._fsm.get(self._id) - other._fsm.get(other._id)
        return SMTimeSeries(ts._time, ts._value, self._fsm)

    def __mul__(self, other):
        """
        Multiply by other's value at each time point

        other: another SMTimeSeries instance
        Return a new SMTimeSeries instance with the values calculated by multiplying self's and other's values
        Raise "TypeError" when other is not an instance of SMTimeSeries class,
        and raise "ValueError" when self's and other's times are not element-wise equal within a tolerance
        """
        if not isinstance(other, SMTimeSeries):
            raise TypeError("NotImplemented Error")
        ts = self._fsm.get(self._id) * other._fsm.get(other._id)
        return SMTimeSeries(ts._time, ts._value, self._fsm)

    def __eq__(self, other):
        """
        Check if two SMTimeSeries instance are equal

        other: another SMTimeSeries instance
        Return true when they are equal, false otherwise
        Raise "TypeError" when other is not an instance of SMTimeSeries class,
        and raise "ValueError" when self's and other's times are not element-wise equal within a tolerance
        """
        if not isinstance(other, SMTimeSeries):
            raise TypeError("NotImplemented Error")
        return (self._fsm.get(self._id) == other._fsm.get(other._id))

    def __abs__(self):
        """
        Return the L^2 norm of values(the root square of the sum of the squared values)
        """
        return abs(self._fsm.get(self._id))

    def __bool__(self):
        """
        Return true if the L^2 norm of values is non-zero, false if it's zero
        """
        return bool(abs(self))


    def __neg__(self):
        """
        Return a new SMTimeseries instance with the opposite number of value at each time point
        """
        ts = -self._fsm.get(self._id)
        return SMTimeSeries(ts._time, ts._value, self._fsm)

    def __pos__(self):
        """
        Return a new SMTimeseries instance with the same value at each time point
        """
        ts = self._fsm.get(self._id)
        return SMTimeSeries(ts._time, ts._value, self._fsm)
