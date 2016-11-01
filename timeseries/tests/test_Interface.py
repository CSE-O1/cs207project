from Interface import SizedContainerTimeSeriesInterface
from pytest import raises
import reprlib
import numpy as np
import collections

#define a concrete SizedContainerTimeSeriesInterface
class concrete_SizedContainerTimeSeriesInterface(SizedContainerTimeSeriesInterface):

    def __init__(self, values, times=None):
        if not isinstance(values, collections.Sequence):
            raise TypeError("Input values must be Sequence")
        if times is not None:
            if not isinstance(times, collections.Sequence):
                raise TypeError("Input times must be Sequence")
            if len(times) != len(values):
                raise ValueError("Input values sequence and times sequence must have the same length")
            self._time = list(times)
        else:
            self._time = list(range(len(values)))
        self._value = list(values)
        self._timeseries = list(zip(self._time, self._value))

    def __setitem__(self, index, value):
        pass

    def __add__(self, other):
        pass

    def __sub__(self, other):
        pass

    def __mul__(self, other):
        pass

    def __eq__(self, other):
        pass

    def __abs__(self):
        pass

    def __bool__(self):
        pass

    def __neg__(self):
        pass

    def __pos__(self):
        pass

    def interpolate(self, time_seq):
        pass

    def mean(self):
        return np.mean(self._value)

    def std(self):
        return np.std(self._value)

    def __len__(self):
        return len(self._value)

    def __getitem__(self, index):
        return self._timeseries[index]

    def __contains__(self, val):
        return val in self._value

    def values(self):
        return self._value

    def times(self):
        return self._time

    def items(self):
        return self._timeseries

    def __str__(self):
        class_name = type(self).__name__
        return class_name + '(' + reprlib.repr([item for item in self._timeseries])

    def __repr__(self):
        class_name = type(self).__name__
        return class_name + '(' + reprlib.repr([item for item in self._timeseries]) + '), length={}'.format(len(self))

#test mean
def test_mean():
    ts = concrete_SizedContainerTimeSeriesInterface([1, 2], [3, 4])
    assert ts.mean() == 1.5

#test std(self):
def test_std():
    ts = concrete_SizedContainerTimeSeriesInterface([1, 2], [3, 4])
    assert ts.std() == 0.5

#test len(self)
def test_len():
    ts = concrete_SizedContainerTimeSeriesInterface([1, 2], [3, 4])
    assert len(ts) == 2

#test getitem
def test_getitem():
    ts = concrete_SizedContainerTimeSeriesInterface([1, 2], [3, 4])
    assert ts[0] == (3, 1)

#test contains
def test_contains():
    ts = concrete_SizedContainerTimeSeriesInterface(list(range(10)), list(range(1, 11)))
    assert (0 in ts) == True
    assert (15 in ts) == False

#test values
def test_values():
    ts = concrete_SizedContainerTimeSeriesInterface([1, 2], [3, 4])
    assert ts.values() == [1, 2]

#test times
def test_times():
    ts = concrete_SizedContainerTimeSeriesInterface([1, 2], [3, 4])
    assert ts.times() == [3, 4]

#test items
def test_items():
    ts = concrete_SizedContainerTimeSeriesInterface([1, 2], [3, 4])
    assert ts.items() == [(3, 1), (4, 2)]

#test str
def test_str():
    ts = concrete_SizedContainerTimeSeriesInterface([1, 2], [3, 4])
    assert str(ts) == "concrete_SizedContainerTimeSeriesInterface([(3, 1), (4, 2)]"

#test repr
def test_repr():
    ts = concrete_SizedContainerTimeSeriesInterface([1, 2], [3, 4])
    assert repr(ts) == "concrete_SizedContainerTimeSeriesInterface([(3, 1), (4, 2)]), length=2"
