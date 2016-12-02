from timeseries.TimeSeries import TimeSeries, check_length, LazyOperation
from pytest import raises
from math import sqrt

"""
test function

"""
#test class init with valid times and values input
def test_valid_full_input():
    ts = TimeSeries([1, 2], [3, 4])
    assert ts._value == [1, 2]
    assert ts._time == [3, 4]

#test class init without times input
def test_valid_non_times_input():
    ts = TimeSeries([1, 2])
    assert ts._value == [1, 2]
    assert ts._time == [0, 1]

#test class init with invalid times and values input
def test_invalid_input():
    with raises(ValueError):
        TimeSeries([1, 2], [3, 4, 5])
    with raises(TypeError):
        TimeSeries(1, 2)
    with raises(TypeError):
        TimeSeries(1, [1])
    with raises(TypeError):
        TimeSeries([1, 2], 3)
    with raises(ValueError):
        TimeSeries([1, 2], [2, 2])

#test len
def test_len():
    ts = TimeSeries([1,2],[3,4])
    assert len(ts) == 2

#test getitem
def test_getitem():
    ts = TimeSeries([1, 2], [3, 4])
    assert ts[1] == (2, 4)

#test setitem with valid parameters
def test_valid_input_setitem():
    ts = TimeSeries([1, 2], [3, 4])
    ts[0] = 10
    assert ts[0] == (10, 3)

#test setitem with invalid parameters
def test_invalid_input_setitem():
    ts = TimeSeries([1, 2], [3, 4])
    with raises(ValueError):
        ts[3] = 10
    with raises(TypeError):
        ts[{1}] = 10

#test contains
def test_contains():
    ts = TimeSeries(list(range(10)), list(range(1, 11)))
    assert (0 in ts) == True

#test add with valid parameters
def test_valid_input_add():
    ts_1 = TimeSeries([1, 2], [3, 4])
    ts_2 = TimeSeries([1, 2], [3, 4])
    ts_sum = ts_1 + ts_2
    assert ts_sum == TimeSeries([2, 4], [3, 4])

#test add with invalid parameters
def test_invalid_input_add():
    ts_1 = TimeSeries([1, 2], [3, 4])
    ts_2 = TimeSeries([1, 2, 3], [3, 4, 5])
    ts_3 = TimeSeries([2, 3], [5, 6])
    arry = [1, 2]
    with raises(ValueError):
        ts_sum = ts_1 + ts_2
    with raises(TypeError):
        ts_sum = ts_1 + arry
    with raises(ValueError):
        ts_sum = ts_1 + ts_3

#test sub with valid parameters
def test_valid_input_sub():
    ts_1 = TimeSeries([1, 2], [3, 4])
    ts_2 = TimeSeries([1, 2], [3, 4])
    ts_sub = ts_1 - ts_2
    assert ts_sub == TimeSeries([0, 0], [3, 4])

#test sub with invalid parameters
def test_invalid_input_sub():
    ts_1 = TimeSeries([1, 2], [3, 4])
    ts_2 = TimeSeries([1, 2, 3], [3, 4, 5])
    ts_3 = TimeSeries([2, 3], [5, 6])
    arry = [1, 2]
    with raises(ValueError):
        ts_sum = ts_1 - ts_2
    with raises(TypeError):
        ts_sum = ts_1 - arry
    with raises(ValueError):
        ts_sum = ts_1 - ts_3

#test mul with valid parameters
def test_valid_input_mul():
    ts_1 = TimeSeries([1, 2], [3, 4])
    ts_2 = TimeSeries([1, 2], [3, 4])
    ts_sub = ts_1 * ts_2
    assert ts_sub == TimeSeries([1, 4], [3, 4])

#test mul with invalid parameters
def test_invalid_input_mul():
    ts_1 = TimeSeries([1, 2], [3, 4])
    ts_2 = TimeSeries([1, 2, 3], [3, 4, 5])
    ts_3 = TimeSeries([2, 3], [5, 6])
    arry = [1, 2]
    with raises(ValueError):
        ts_sum = ts_1 * ts_2
    with raises(TypeError):
        ts_sum = ts_1 * arry
    with raises(ValueError):
        ts_sum = ts_1 * ts_3

#test eq with valid parameters
def test_valid_input_eq():
    ts_1 = TimeSeries([1, 2], [3, 4])
    ts_2 = TimeSeries([1, 2], [3, 4])
    ts_3 = TimeSeries([1, 3], [3, 4])
    assert ts_1 == ts_2
    assert ts_1 != ts_3

#test eq with invalid parameters
def test_invalid_input_eq():
    ts_1 = TimeSeries([1, 2], [3, 4])
    ts_2 = TimeSeries([1, 2, 3], [3, 4, 5])
    with raises(TypeError):
        ts_1 == ([3, 1], [4, 2])
    with raises(ValueError):
        ts_1 == ts_2

#test abs
def test_abs():
    ts = TimeSeries([3, 4], [3, 4])
    assert abs(ts) == 5

#test bool
def test_bool():
    ts = TimeSeries([2, 2], [3, 4])
    assert bool(ts) == True

#test neg
def test_neg():
    ts = TimeSeries([2, 2], [3, 4])
    assert -ts == TimeSeries([-2, -2], [3, 4])

#test pos
def test_pos():
    ts = TimeSeries([1, 2], [3, 4])
    assert +ts == ts

#test interpolate with valid parameters
def test_valid_input_interpolate():
    ts_1 = TimeSeries([1,2,3], [0,5,10])
    ts_2 = TimeSeries([100, -100], [2.5, 7.5])
    ts_interpolate_test_1 = ts_1.interpolate([1])
    assert ts_interpolate_test_1._value == [1.2]
    assert ts_interpolate_test_1._time == [1]

    ts_interpolate_test_2 = ts_1.interpolate([-100, 100])
    assert ts_interpolate_test_2 == TimeSeries([1, 3], [-100, 100])

    ts_interpolate_test_3 = ts_1.interpolate([2.5, 7.5])
    assert ts_interpolate_test_3 == TimeSeries([1.5, 2.5], [2.5, 7.5])

    assert ts_1.interpolate(ts_2.itertimes()) == TimeSeries([1.5, 2.5], [2.5, 7.5])


#test interpolate with invalid parameters
def test_invalid_input_interpolate():
    ts_1 = TimeSeries([1, 2, 3], [0, 5, 10])

    with raises(TypeError):
        ts_1.interpolate(1)

#test lazy
def test_lazy_in_TS_class():
    ts = TimeSeries([1,2],[3,4])
    thunk = ts.lazy
    assert isinstance(thunk, LazyOperation) == True
    assert thunk.eval() == ts

#test lazy check_length
def test_lazy_check_length():
    l1 = TimeSeries(range(0,3), range(1,4))
    l2 = TimeSeries(range(1,4), range(2,5))
    thunk = check_length(l1,l2)
    assert isinstance(thunk, LazyOperation) == True
    assert thunk.eval() == True;

def test_mean():
    ts = TimeSeries([1, 2], [3, 4])
    assert ts.mean() == 1.5

def test_std():
    ts = TimeSeries([1, 2], [3, 4])
    assert ts.std() == sqrt(0.25)
