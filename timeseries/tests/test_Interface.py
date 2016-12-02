from timeseries.TSInterface import SizedContainerTimeSeriesInterface
from pytest import raises
import reprlib
import numpy as np
import collections

#define a concrete class from SizedContainerTimeSeriesInterface
class ConcreteSizedContainerTimeSeriesInterface(SizedContainerTimeSeriesInterface):

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
        self._timeseries = list(zip(self._value, self._time))


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

#one instance used for some of the following tests
ts = ConcreteSizedContainerTimeSeriesInterface([1, 2], [3, 4])

#test mean() which returns the mean of self._value
def test_mean():
    assert ts.mean() == 1.5

#test std() which returns the std of self._value:
def test_std():
    assert ts.std() == 0.5

def test_len():
    assert len(ts) == 2

def test_getitem():
    assert ts[0] == (1, 3)

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
    assert ts.items() == [(1, 3), (2, 4)]

def test_str():
    nts = ConcreteSizedContainerTimeSeriesInterface(list(range(100)), list(range(100)))
    assert str(ts) == "ConcreteSizedContainerTimeSeriesInterface([(1, 3), (2, 4)]"
    assert str(nts) == "ConcreteSizedContainerTimeSeriesInterface([(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), ...]"

def test_repr():
    nts = ConcreteSizedContainerTimeSeriesInterface(list(range(100)), list(range(100)))
    assert repr(ts) == "ConcreteSizedContainerTimeSeriesInterface([(1, 3), (2, 4)]), length=2"
    assert repr(nts) == "ConcreteSizedContainerTimeSeriesInterface([(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), ...]), length=100"

#test interpolate with valid parameters
def test_valid_input_interpolate():
    ts_1 = ConcreteSizedContainerTimeSeriesInterface([1,2,3], [0,5,10])
    ts_2 = ConcreteSizedContainerTimeSeriesInterface([100, -100], [2.5, 7.5])
    ts_interpolate_test_1 = ts_1.interpolate([1])
    assert ts_interpolate_test_1._value == [1.2]
    assert ts_interpolate_test_1._time == [1]

    ts_interpolate_test_2 = ts_1.interpolate([-100, 100])
    assert repr(ts_interpolate_test_2) == "ConcreteSizedContainerTimeSeriesInterface([(1, -100), (3, 100)]), length=2"

    ts_interpolate_test_3 = ts_1.interpolate([2.5, 7.5])
    assert repr(ts_interpolate_test_3) == "ConcreteSizedContainerTimeSeriesInterface([(1.5, 2.5), (2.5, 7.5)]), length=2"

    assert repr(ts_1.interpolate(ts_2.itertimes())) == "ConcreteSizedContainerTimeSeriesInterface([(1.5, 2.5), (2.5, 7.5)]), length=2"

#test interpolate with invalid parameters
def test_invalid_input_interpolate():
    ts_1 = ConcreteSizedContainerTimeSeriesInterface([1, 2, 3], [0, 5, 10])

    with raises(TypeError):
        ts_1.interpolate(1)