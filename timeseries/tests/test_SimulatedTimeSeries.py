""" test code for SimulatedTimeSeries
This module contains tests for SimulatedTimeSeries.

Methods
-------
make_simple_data(stop=None):
    A function to generate simulated data
make_stat_data(m, stop=None):
    A function to generate normally distributed data with mean of 1e4 and standard deviation m
test_type():
    A function to test if input is a generator
test_str():
    A function to test __str__
test_repr():
    A function to test __repr__
test_produce():
    A function to test produce using data size of 50 and 5 different chunk sizes
test_mean():
    A function to test mean with size of 10000 and 30000
test_std():
    A function to test std with size of 15000 and 30000
test_mean_std():
    A function to test online_mean and online_std using data size 1e5 and chunk size 9e4
    Error in last mean is limited to 0.1%, error in last standard deviation is limiated to 1%.

"""


from itertools import count
from random import normalvariate, random
from pytest import raises
from SimulatedTimeSeries import SimulatedTimeSeries
import numpy as np
from pytest import raises


def make_simple_data(stop=None):
    """
    A function to generate simulated data

    """
    for value in count():
        if stop and value > stop:
            break
        yield value


def make_stat_data(in_std, stop=None):
    """
    A function to generate normally distributed data with mean of 1e4 and standard deviation in_std

    """
    for _ in count():
        if stop and _ > stop:
            break
        yield 1.0e04 + normalvariate(0, in_std*random())


def test_type():
    """
    A function to test if input is a generator

    """
    with raises(TypeError):
        wrongtype = SimulatedTimeSeries(5)


def test_str():
    """
    A function to test __str__

    """
    data = make_simple_data(5)
    timeseries_5 = SimulatedTimeSeries(data)
    assert str(timeseries_5) == "SimulatedTimeSeries(time=0)"


def test_repr():
    """
    A function to test __repr__

    """
    data = make_simple_data(5)
    timeseries_5 = SimulatedTimeSeries(data)
    assert repr(timeseries_5) == "SimulatedTimeSeries(time=0)"


def test_produce():
    """
    A function to test produce using data size of 50 and 5 different chunk sizes

    """
    # test chunk=1 and chunk>1
    for data_size, chunk_size in [(50, 5), (50, 4), (50, 3), (50, 2), (50, 1)]:
        data = make_simple_data(data_size)
        test_ts = SimulatedTimeSeries(data)
        result = list(test_ts.produce(chunk_size))
        expect_result = []
        for time, value in enumerate(make_simple_data(data_size)):
            if len(expect_result) >= chunk_size:
                assert result == expect_result
                result = list(test_ts.produce(chunk_size))
                expect_result = []
            expect_result.append((time, value))

def test_mean():
    """
    A function to test mean with size of 10000 and 30000

    """
    finite_data = make_simple_data(10000)
    ts = SimulatedTimeSeries(finite_data)
    assert ts.mean() == 5000

    infinite_data = make_simple_data(30000)
    ts = SimulatedTimeSeries(infinite_data)
    with raises(ValueError):
        ts.mean()

def test_std():
    """
    A function to test std with size of 15000 and 30000

    """
    finite_data = make_simple_data(15000)
    ts = SimulatedTimeSeries(finite_data)
    finite_data_copy = make_simple_data(15000)
    data_list = []
    for time, value in enumerate(finite_data_copy):
        data_list.append(value) 
    expect_result = np.std(data_list)
    err_std = (ts.std() - expect_result) / expect_result 
    assert abs(err_std) < 1e-4

    infinite_data = make_simple_data(30000)
    ts = SimulatedTimeSeries(infinite_data)
    with raises(ValueError):
        ts.std()


# def test_mean_std():
#     """
#     A function to test online_mean and online_std using data size 1e5 and chunk size 9e4
#     Error in last mean is limited to 0.1%, error in last standard deviation is limiated to 1%.
#
#     """
#     #test data_size=1e5, chunk=9e4
#     for data_size, chunk_size in [(1e5, 9e4)]:
#         # randomly generate data
#         np.random.seed(0)
#         data_for_mean = make_stat_data(500, data_size)
#         np.random.seed(0)
#         data_for_std = make_stat_data(500, data_size)
#         np.random.seed(0)
#         data_list = list(make_stat_data(500, data_size))
#
#         # produce online_mean and oneline_std
#         ts_mean = SimulatedTimeSeries(data_for_mean).online_mean()
#         ts_std = SimulatedTimeSeries(data_for_std).online_std()
#         result_mean = list(ts_mean.produce(chunk_size))
#         result_std = list(ts_std.produce(chunk_size))
#
#         expect_result_mean, expect_result_std = [], []
#
#         for time in range(len(data_list)):
#             if len(expect_result_mean) >= chunk_size:
#                 # check error of online_mean from the last mean
#                 err_mean = np.divide(np.subtract(result_mean, expect_result_mean), \
#                                      expect_result_mean)
#                 assert abs(err_mean[-1, 1]) < 1e-3 # error of online_mean should < 0.1%
#                 # check error of online_std from the last std
#                 err_std = np.divide(np.subtract(result_std, expect_result_std), expect_result_std)
#                 assert abs(err_std[-1, 1]) < 1e-2 # error of online_std should < 1%
#                 # generate mean and std for next chunk
#                 result_mean = list(ts_mean.produce(chunk_size))
#                 result_std = list(ts_std.produce(chunk_size))
#                 expect_result_mean, expect_result_std = [], []
#                 # only test the first chunk to save time
#                 break
#             expect_result_mean.append((time, np.mean(data_list[:time+1])))
#             expect_result_std.append((time, np.std(data_list[:time+1])))
