from pytest import raises
import unittest
import numpy as np
from cs207rbtree.tree import ValueRef, RedBlackNodeRef, RedBlackNode, RedBlackTree, Color
from cs207rbtree.database import Storage, DBDB, connect
import os
import sys

# test init method in class Storage
def test_init_storage():
    dbname = "test.dbdb"
    try:
        f = open(dbname, 'r+b')
    except IOError:
        fd = os.open(dbname, os.O_RDWR | os.O_CREAT)
        f = os.fdopen(fd, 'r+b')
    storage = Storage(f)
    assert type(storage) == Storage
    redBlackTree = RedBlackTree(storage)
    db = DBDB(f)
    db.close()
    os.remove('test.dbdb')

# test lock in class Storage
def test_lock_storage():
    dbname = "test.dbdb"
    try:
        f = open('test.dbdb', 'r+b')
    except IOError:
        fd = os.open('test.dbdb', os.O_RDWR | os.O_CREAT)
        f = os.fdopen(fd, 'r+b')
    storage = Storage(f)
    assert storage.lock() == True
    db = DBDB(f)
    db.close()
    os.remove('test.dbdb')

# test unlock in class Storage
def test_unlock_Storage():
    dbname = "test.dbdb"
    try:
        f = open('test.dbdb', 'r+b')
    except IOError:
        fd = os.open('test.dbdb', os.O_RDWR | os.O_CREAT)
        f = os.fdopen(fd, 'r+b')
    storage = Storage(f)
    storage.unlock()
    assert storage.locked == False
    db = DBDB(f)
    db.close()
    os.remove('test.dbdb')

# test _bytes_to_integer in class Storage
def test_bytes_to_integer_Storage():
    dbname = "test.dbdb"
    try:
        f = open('test.dbdb', 'r+b')
    except IOError:
        fd = os.open('test.dbdb', os.O_RDWR | os.O_CREAT)
        f = os.fdopen(fd, 'r+b')
    storage = Storage(f)
    assert storage._bytes_to_integer(b'01234567') == 3472611983179986487
    db = DBDB(f)
    db.close()
    os.remove('test.dbdb')

# test _integer_to_bytes in class Storage
def test_integer_to_bytes_Storage():
    dbname = "test.dbdb"
    try:
        f = open('test.dbdb', 'r+b')
    except IOError:
        fd = os.open('test.dbdb', os.O_RDWR | os.O_CREAT)
        f = os.fdopen(fd, 'r+b')
    storage = Storage(f)
    bytes = storage._bytes_to_integer(b'01234567')
    assert storage._integer_to_bytes(bytes) == b'01234567'
    db = DBDB(f)
    db.close()
    os.remove('test.dbdb')

# test write in class Storage
def test_write_Storage():
    dbname = "test.dbdb"
    try:
        f = open('test.dbdb', 'r+b')
    except IOError:
        fd = os.open('test.dbdb', os.O_RDWR | os.O_CREAT)
        f = os.fdopen(fd, 'r+b')
    storage = Storage(f)
    address = storage.write(b'01234567')
    assert type(address) == int
    db = DBDB(f)
    db.close()
    os.remove('test.dbdb')

# test close and closed in class Storage
def test_close_closed_Storage():
    dbname = "test.dbdb"
    try:
        f = open('test.dbdb', 'r+b')
    except IOError:
        fd = os.open('test.dbdb', os.O_RDWR | os.O_CREAT)
        f = os.fdopen(fd, 'r+b')
    storage = Storage(f)
    assert storage.closed == False
    storage.close()
    assert storage.closed == True
    os.remove('test.dbdb')

# test init method in class DBDB
def test_init_DBDB():
    dbname = "test.dbdb"
    try:
        f = open('test.dbdb', 'r+b')
    except IOError:
        fd = os.open('test.dbdb', os.O_RDWR | os.O_CREAT)
        f = os.fdopen(fd, 'r+b')
    dbdb = DBDB(f)
    assert type(dbdb) == DBDB
    os.remove('test.dbdb')