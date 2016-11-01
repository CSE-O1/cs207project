from Interface import SizedContainerTimeSeriesInterface
from pytest import raises
import reprlib
import numpy as np
import collections

#define a concrete SizedContainerTimeSeriesInterface
class ConcreteSizedContainerTimeSeriesInterface(SizedContainerTimeSeriesInterface):

    def __init__(self, values, times=None):
        self._time = list(times)
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

#one instance used for some of the following tests
ts = ConcreteSizedContainerTimeSeriesInterface([1, 2], [3, 4])

#test mean() which returns the mean of self._value
def test_mean():
    assert ts.mean() == 1.5

#test std() which returns the std of self._value:
def test_std():
    assert ts.std() == 0.5

#test len(self)
def test_len():
    assert len(ts) == 2

#test getitem
def test_getitem():
    assert ts[0] == (3, 1)

#test contains
def test_contains():
    nts = ConcreteSizedContainerTimeSeriesInterface(list(range(10)), list(range(1, 11)))
    assert (0 in nts) == True
    assert (15 in nts) == False

#test values which returns self._value
def test_values():
    assert ts.values() == [1, 2]

#test times which returns self._time
def test_times():
    assert ts.times() == [3, 4]

#test items which returns self._timeseries
def test_items():
    assert ts.items() == [(3, 1), (4, 2)]

#test str()
def test_str():
    assert str(ts) == "ConcreteSizedContainerTimeSeriesInterface([(3, 1), (4, 2)]"

#test repr()
def test_repr():
    assert repr(ts) == "ConcreteSizedContainerTimeSeriesInterface([(3, 1), (4, 2)]), length=2"
