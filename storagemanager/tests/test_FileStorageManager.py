""" test code for FileStorageManager
This module contains tests for FileStorageManager.

Methods
-------
"""

import numpy as np
from pytest import raises
from SMInterface import StorageManagerInterface
from FileStorageManager import FileStorageManager
from cs207project.timeseries.ArrayTimeSeries import ArrayTimeSeries


def test_init():
    test_fsm = FileStorageManager()
    assert (test_fsm._id == set()) == True

def test_gen_id():
    test_fsm = FileStorageManager()
    test_id = test_fsm.gen_id()
    assert (test_id == 0) == True

def test_ts2nparray():
    test_fsm = FileStorageManager()
    test_ts = ArrayTimeSeries([11, 12, 13, 14, 15], [1, 2, 3, 4, 5])
    correct_array = np.array([[1., 2., 3., 4., 5.],
                              [11., 12., 13., 14., 15.]])
    test_array = test_fsm.ts2nparray(test_ts)
    assert (np.array_equal(test_array, correct_array)) == True
