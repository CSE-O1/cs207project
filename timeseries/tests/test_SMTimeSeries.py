""" Test code for SMTimeSeries
This module contains tests for SMTimeSeries.

Methods
-------
test_init():
    A function to test __init__
test_from_db():
    A function to test from_db
test_setitem():
    A function to test __setitem__
test_add():
    A function to test  add
test_sub():
    A function to test sub
test_mul():
    A function to test mul
test_eq():
    A function to test eq
test_abs():
    A function to test abs
test_bool():
    A function to test bool
test_neg():
    A function to test neg
test_pos():
    A function to test pos

"""

import numpy as np
from os import system
from pytest import raises
from timeseries.ArrayTimeSeries import ArrayTimeSeries
from timeseries.SMTimeSeries import SMTimeSeries
from storagemanager.FileStorageManager import FileStorageManager


# clean up data folder
system("rm ./data/*.npy")

def test_init():
    """
    A function to test __init__

    """
    test_fsm = FileStorageManager()
    test_time = np.array([1, 2, 3, 4, 5])
    test_value = np.array([11, 12, 13, 14, 15])
    test_smts = SMTimeSeries(test_time, test_value, test_fsm)
    with raises(TypeError): SMTimeSeries(1, [11, 12, 13], test_fsm)
    with raises(TypeError): SMTimeSeries([1, 2, 3], 11, test_fsm)
    with raises(ValueError): SMTimeSeries([1, 2, 3], [11, 12, 13, 14, 15], test_fsm)
    with raises(ValueError): SMTimeSeries([1, 1, 2, 2, 3], [11, 12, 13, 14, 15], test_fsm)

def test_from_db():
    """
    A function to test from_db

    """
    test_fsm = FileStorageManager()
    id_now = max(test_fsm._id)
    gotten_ts = SMTimeSeries.from_db(id_now, test_fsm)
    assert np.array_equal(gotten_ts.times, np.array([1, 2, 3, 4, 5]))
    assert np.array_equal(gotten_ts.values, np.array([11, 12, 13, 14, 15]))

def test_setitem():
    """
    A function to test __setitem__

    """
    test_fsm = FileStorageManager()
    test_time_01 = np.array([1, 2, 3, 4, 5, 6])
    test_value_01 = np.array([11, 12, 13, 14, 15, 16])
    test_smts_01 = SMTimeSeries(test_time_01, test_value_01, test_fsm)
    test_smts_01[0] = 15
    test_smts_01[2] = 35
    gotten_ts_01 = test_smts_01.from_db(test_smts_01._id, test_smts_01._fsm)
    assert np.array_equal(gotten_ts_01.values, np.array([15, 12, 35, 14, 15, 16]))
    with raises(TypeError): test_smts_01[3.5] = 25
    with raises(ValueError): test_smts_01[15] = 25

def test_add():
    """
    A funciton to test add

    """
    test_fsm = FileStorageManager()
    test_time_01 = np.array([1, 2, 3, 4, 5, 6])
    test_value_01 = np.array([11, 12, 13, 14, 15, 16])
    test_smts_01 = SMTimeSeries(test_time_01, test_value_01, test_fsm)
    test_time_02 = np.array([1, 2, 3, 4, 5, 6])
    test_value_02 = np.array([10, 20, 30, 40, 50, 60])
    test_smts_02 = SMTimeSeries(test_time_02, test_value_02, test_fsm)
    test_smts_03 = test_smts_01 + test_smts_02
    gotten_ts = test_smts_03.from_db(test_smts_03._id, test_smts_03._fsm)
    assert np.array_equal(gotten_ts.times, np.array([1, 2, 3, 4, 5, 6]))
    assert np.array_equal(gotten_ts.values, np.array([21, 32, 43, 54, 65, 76]))
    with raises(TypeError): test_smts_04 = test_smts_01 + np.array([10, 20, 30, 40, 50, 60])

def test_sub():
    """
    A function to test sub

    """
    test_fsm = FileStorageManager()
    test_time_01 = np.array([1, 2, 3, 4, 5, 6])
    test_value_01 = np.array([11, 12, 13, 14, 15, 16])
    test_smts_01 = SMTimeSeries(test_time_01, test_value_01, test_fsm)
    test_time_02 = np.array([1, 2, 3, 4, 5, 6])
    test_value_02 = np.array([10, 20, 30, 40, 50, 60])
    test_smts_02 = SMTimeSeries(test_time_02, test_value_02, test_fsm)
    test_smts_03 = test_smts_01 - test_smts_02
    gotten_ts = test_smts_03.from_db(test_smts_03._id, test_smts_03._fsm)
    assert np.array_equal(gotten_ts.times, np.array([1, 2, 3, 4, 5, 6]))
    assert np.array_equal(gotten_ts.values, np.array([1, -8, -17, -26, -35, -44]))
    with raises(TypeError): test_smts_04 = test_smts_01 - np.array([10, 20, 30, 40, 50, 60])

def test_mul():
    """
    A function to test mul

    """
    test_fsm = FileStorageManager()
    test_time_01 = np.array([1, 2, 3, 4, 5, 6])
    test_value_01 = np.array([11, 12, 13, 14, 15, 16])
    test_smts_01 = SMTimeSeries(test_time_01, test_value_01, test_fsm)
    test_time_02 = np.array([1, 2, 3, 4, 5, 6])
    test_value_02 = np.array([1, 2, 1, 2, 1, 2])
    test_smts_02 = SMTimeSeries(test_time_02, test_value_02, test_fsm)
    test_smts_03 = test_smts_01 * test_smts_02
    gotten_ts = test_smts_03.from_db(test_smts_03._id, test_smts_03._fsm)
    assert np.array_equal(gotten_ts.times, np.array([1, 2, 3, 4, 5, 6]))
    assert np.array_equal(gotten_ts.values, np.array([11, 24, 13, 28, 15, 32]))
    with raises(TypeError): test_smts_04 = test_smts_01 * np.array([1, 2, 1, 2, 1, 2])

def test_eq():
    """
    A function to test eq

    """
    test_fsm = FileStorageManager()
    test_time_01 = np.array([1, 2, 3, 4, 5, 6])
    test_value_01 = np.array([11, 12, 13, 14, 15, 16])
    test_smts_01 = SMTimeSeries(test_time_01, test_value_01, test_fsm)
    test_time_02 = np.array([1, 2, 3, 4, 5, 6])
    test_value_02 = np.array([11, 12, 13, 14, 15, 16])
    test_smts_02 = SMTimeSeries(test_time_02, test_value_02, test_fsm)
    test_time_03 = np.array([1, 2, 3, 4, 5, 6])
    test_value_03 = np.array([11, 12, 13, 14, 15, 6])
    test_smts_03 = SMTimeSeries(test_time_03, test_value_03, test_fsm)
    assert test_smts_01 == test_smts_02
    assert test_smts_01 != test_smts_03
    with raises(TypeError): test_smts_01 == np.array([11, 12, 13, 14, 15, 16])

def test_abs():
    """
    A function to test abs

    """
    test_fsm = FileStorageManager()
    test_time_01 = np.array([1, 2])
    test_value_01 = np.array([3, 4])
    test_smts_01 = SMTimeSeries(test_time_01, test_value_01, test_fsm)
    assert abs(test_smts_01) == 5

def test_bool():
    """
    A function to test bool

    """
    test_fsm = FileStorageManager()
    test_time_01 = np.array([1, 2])
    test_value_01 = np.array([3, 4])
    test_smts_01 = SMTimeSeries(test_time_01, test_value_01, test_fsm)
    assert bool(test_smts_01) == True

def test_neg():
    """
    A function to test neg

    """
    test_fsm = FileStorageManager()
    test_time_01 = np.array([1, 2, 3, 4, 5, 6])
    test_value_01 = np.array([11, 12, 13, 14, 15, 16])
    test_smts_01 = SMTimeSeries(test_time_01, test_value_01, test_fsm)
    test_time_02 = np.array([1, 2, 3, 4, 5, 6])
    test_value_02 = np.array([-11, -12, -13, -14, -15, -16])
    test_smts_02 = SMTimeSeries(test_time_02, test_value_02, test_fsm)
    assert -test_smts_01 == test_smts_02

def test_pos():
    """
    A function to test pos

    """
    test_fsm = FileStorageManager()
    test_time_01 = np.array([1, 2, 3, 4, 5, 6])
    test_value_01 = np.array([11, 12, 13, 14, 15, 16])
    test_smts_01 = SMTimeSeries(test_time_01, test_value_01, test_fsm)
    test_time_02 = np.array([1, 2, 3, 4, 5, 6])
    test_value_02 = np.array([11, 12, 13, 14, 15, 16])
    test_smts_02 = SMTimeSeries(test_time_02, test_value_02, test_fsm)
    assert +test_smts_01 == test_smts_02
