""" Test code for FileStorageManager
This module contains tests for FileStorageManager.

Methods
-------
test_init():
    A function to test __init__
test_gen_id():
    A function to test gen_id
test_ts2nparray():
    A function to test ts2nparray
test_store():
    A function to test store
test_size():
    A function to test size
test_get():
    A function to test get
test_multiple_ts():
    A function to test when multiple timeserieses exist

"""

import numpy as np
from os import system
from pytest import raises
from SMInterface import StorageManagerInterface
from FileStorageManager import FileStorageManager
from timeseries.ArrayTimeSeries import ArrayTimeSeries

# clean up data folder
system("rm ./data/*.npy")

def test_init():
    """
    A function to test __init__

    """
    test_fsm = FileStorageManager()
    assert test_fsm._id == set()

def test_gen_id():
    """
    A function to test gen_id

    """
    test_fsm = FileStorageManager()
    test_id = test_fsm.gen_id()
    assert test_id == 0

def test_ts2nparray():
    """
    A function to test ts2nparray

    """
    test_fsm = FileStorageManager()
    test_ts = ArrayTimeSeries([11, 12, 13, 14, 15], [1, 2, 3, 4, 5])
    correct_array = np.array([[1., 2., 3., 4., 5.],
                              [11., 12., 13., 14., 15.]])
    test_array = test_fsm.ts2nparray(test_ts)
    assert np.array_equal(test_array, correct_array)
    assert test_array.dtype == 'float64'

def test_store():
    """
    A function to test store

    """
    test_fsm = FileStorageManager()
    test_id = test_fsm.gen_id()
    test_ts = ArrayTimeSeries([11, 12, 13, 14, 15], [1, 2, 3, 4, 5])
    return_ts = test_fsm.store(test_id, test_ts)
    assert isinstance(return_ts, ArrayTimeSeries)
    assert np.array_equal(return_ts.times(), np.array([1, 2, 3, 4, 5]))
    assert np.array_equal(return_ts.values(), np.array([11, 12, 13, 14, 15]))

def test_size():
    """
    A function to test size

    """
    test_fsm = FileStorageManager()
    id_now = max(test_fsm._id)
    assert test_fsm.size(id_now) == 5
    with raises(ValueError): test_fsm.size(3)

def test_get():
    """
    A function to test get

    """
    test_fsm = FileStorageManager()
    id_now = max(test_fsm._id)
    gotten_ts_00 = test_fsm.get(id_now)
    assert isinstance(gotten_ts_00, ArrayTimeSeries)
    assert np.array_equal(gotten_ts_00.times(), np.array([1, 2, 3, 4, 5]))
    assert np.array_equal(gotten_ts_00.values(), np.array([11, 12, 13, 14, 15]))
    with raises(ValueError): test_fsm.get(3)

def test_multiple_ts():
    """
    A function to test when multiple timeserieses exist

    """
    test_fsm = FileStorageManager()
    id_now = max(test_fsm._id)
    # timeseries with ID = 1
    test_id_01 = test_fsm.gen_id()
    test_ts_01 = ArrayTimeSeries([21, 22, 23, 24, 25, 26, 27], [1, 2, 3, 4, 5, 6, 7])
    return_ts_01 = test_fsm.store(test_id_01, test_ts_01)
    # timeseries with ID = 2
    test_id_02 = test_fsm.gen_id()
    test_ts_02 = ArrayTimeSeries([31, 32, 33, 34, 35, 36, 37, 38, 39, 40],
                                 [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    return_ts_02 = test_fsm.store(test_id_02, test_ts_02)
    # get timeseries and check
    gotten_ts_01 = test_fsm.get(test_id_01)
    gotten_ts_02 = test_fsm.get(test_id_02)
    assert id_now == 0
    assert isinstance(gotten_ts_01, ArrayTimeSeries)
    assert np.array_equal(gotten_ts_01.times(), np.array([1, 2, 3, 4, 5, 6, 7]))
    assert np.array_equal(gotten_ts_01.values(), np.array([21, 22, 23, 24, 25, 26, 27]))
    assert isinstance(gotten_ts_02, ArrayTimeSeries)
    assert np.array_equal(gotten_ts_02.times(), np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))
    assert np.array_equal(gotten_ts_02.values(), np.array([31, 32, 33, 34, 35, 36, 37, 38, 39, 40]))
