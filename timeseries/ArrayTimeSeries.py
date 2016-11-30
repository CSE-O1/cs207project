import numpy as np
import numbers
import reprlib
import collections
import math
from TimeSeries import TimeSeries
from TSInterface import SizedContainerTimeSeriesInterface
from Lazy import lazy, LazyOperation


class ArrayTimeSeries(SizedContainerTimeSeriesInterface):
    """
    A time series class that implements SizedContainerTimeSeriesInterface, with times and values stored in
    numpy arrays.

    The times and values should be numbers. Times numpy array are considered equal when the difference is 
    within a small tolerance (using numpy.allclose default tolerance). It implements basic unary functions 
    abs, bool, neg, pos, and binary functions add, sub, mul, eq, and interpolate function.

    >>> A=ArrayTimeSeries([3,4], [1,2])
    >>> B=ArrayTimeSeries([5,6], [1,2])
    >>> A+B 
    ArrayTimeSeries([array([8, 1]), array([10,  2])]), length=2
    >>> A-B
    ArrayTimeSeries([array([-2,  1]), array([-2,  2])]), length=2
    >>> A==B
    False
    >>> -A
    ArrayTimeSeries([array([-3,  1]), array([-4,  2])]), length=2
    >>> abs(A)
    5.0
    """
    def __init__(self, values, times = None):
        """
        Initialize a ArrayTimeSeries instance, inherited from SizedContainerTimeSeriesInterface

        The input times and values sequences should have fixed lengths, assume n is the length
        self._time: store the times in a n*1 numpy array
        self._value: store the values in a n*1 numpy array
        self._timeseries: a n*2 numpy array with the times as the first column and values as the second column
        """
        if not isinstance(values, collections.Sequence) and not isinstance(values, np.ndarray):
            raise TypeError("Input values must be Sequence")
        if times is not None:
            if not isinstance(times, collections.Sequence) and not isinstance(values, np.ndarray):
                raise TypeError("Input times must be Sequence")
            if len(times) != len(values):
                raise ValueError("Input values and times sequence must have the same length")
            if len(times) != len(set(times)):
                raise ValueError("Input times sequence must be unique")
            self._time = np.array(times)
        else:
            self._time = np.array(list(range(len(values))))
        self._value = np.array(values)
        self._timeseries = np.array(list(zip(self._value, self._time)))

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
        self._value[index] = value
        self._timeseries[index][0] = value

    def __add__(self, other):
        """ 
        Add two ArrayTimeSeries' values at each time point

        other: another ArrayTimeSeries instance
        Return a new ArrayTimeSeries instance with the values being sum of both timeseries values
        Raise "TypeError" when other is not an instance of ArrayTimeSeries class,
        and raise "ValueError" when self's and other's times are not element-wise equal within a tolerance
        """ 
        if not isinstance(other, ArrayTimeSeries):
            raise TypeError("NotImplemented Error")
        if len(self) != len(other):
            raise ValueError(str(self)+' and '+str(other)+' must have the same length')
        if not np.allclose(self._time, other._time):
            raise ValueError(str(self)+' and '+str(other)+' must have the same time points')
        return ArrayTimeSeries(self._value + other._value, self._time)

    def __sub__(self, other):
        """ 
        Subtract by other's value at each time point

        other: another ArrayTimeSeries instance 
        Return a new ArrayTimeSeries instance with the values calculated by subtracting other's values from
        self's values
        Raise "TypeError" when other is not an instance of ArrayTimeSeries class,
        and raise "ValueError" when self's and other's times are not element-wise equal within a tolerance
        """ 
        if not isinstance(other, ArrayTimeSeries):
            raise TypeError("NotImplemented Error")
        if len(self) != len(other):
            raise ValueError(str(self)+' and '+str(other)+' must have the same length')
        if not np.allclose(self._time, other._time):
            raise ValueError(str(self)+' and '+str(other)+' must have the same time points')
        return ArrayTimeSeries(self._value - other._value, self._time)

    def __mul__(self, other):
        """ 
        Multiply by other's value at each time point

        other: another ArrayTimeSeries instance
        Return a new ArrayTimeSeries instance with the values calculated by multiplying self's and other's values 
        Raise "TypeError" when other is not an instance of ArrayTimeSeries class,
        and raise "ValueError" when self's and other's times are not element-wise equal within a tolerance
        """ 
        if not isinstance(other, ArrayTimeSeries):
            raise TypeError("NotImplemented Error")
        if len(self) != len(other):
            raise ValueError(str(self)+' and '+str(other)+' must have the same length')
        if not np.allclose(self._time, other._time):
            raise ValueError(str(self)+' and '+str(other)+' must have the same time points')
        return ArrayTimeSeries(self._value * other._value, self._time)

    def __eq__(self, other):
        """ 
        Check if two ArrayTimeSeries instance are equal

        other: another ArrayTimeSeries instance
        Return true when they are equal, false otherwise 
        Raise "TypeError" when other is not an instance of ArrayTimeSeries class,
        and raise "ValueError" when self's and other's times are not element-wise equal within a tolerance
        """ 
        if not isinstance(other, ArrayTimeSeries):
            raise TypeError("NotImplemented Error")
        if len(self) != len(other):
            raise ValueError(str(self) + ' and ' + str(other) + ' must have the same length')
        return np.all(self._value == other._value) == True and np.allclose(self._time, other._time)

    def __abs__(self):
        """ 
        Return the L^2 norm of values(the root square of the sum of the squared values)
        """ 
        return math.sqrt(self._value.dot(self._value))

    def __bool__(self):
        """ 
        Return true if the L^2 norm of values is non-zero, false if it's zero
        """ 
        return bool(abs(self))

    def __neg__(self):
        """ 
        Return a new ArrayTimeseries instance with the opposite number of value at each time point
        """ 
        return ArrayTimeSeries(- self._value, self._time)

    def __pos__(self):
        """ 
        Return a new ArrayTimeseries instance with the same value at each time point
        """ 
        return ArrayTimeSeries(self._value, self._time)

    @property
    def lazy(self):
        # indentity function
        identity = lambda x: x
        return LazyOperation(identity, self)


# lazy test part
@lazy
def check_length(a, b):
    return len(a) == len(b)
