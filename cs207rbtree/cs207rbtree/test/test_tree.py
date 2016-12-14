from pytest import raises
import unittest
import numpy as np
from cs207rbtree.tree import ValueRef, RedBlackNodeRef, RedBlackNode,RedBlackEmptyNode, RedBlackTree, Color
from cs207rbtree.database import Storage, DBDB, connect
import os
import sys
from queue import Queue

# basic test to make sure red black tree functions well
def test_basic():
    db = connect("test.dbdb")
    db.set(2, "aged")
    db.set(1, "gd")
    db.set(4, "stillyoung")
    db.set(5, "stillyoung")
    db.set(9, "stillyoung")
    db.set(3, "stillyoung")
    db.set(6, "stillyoung")
    db.set(7, "stillyoung")
    db.commit()
    db.close()
    newdb = connect("test.dbdb")
    assert newdb.get(2) == "aged"
    newdb.close()
    os.remove('test.dbdb')

# test init method in class ValueRef
def test_init_ValueRef():
    ref = ValueRef()
    assert type(ref) is ValueRef

# test referent_to_bytes in class ValueRef
def test_referent_to_bytes_ValueRef():
    ref = ValueRef()
    referent = '5'
    assert ref.referent_to_bytes(referent) == b'5'

# test bytes_to_referent in class ValueRef
def test_bytes_to_referent_ValueRef():
    ref = ValueRef()
    referent = '5'
    bytes = ref.referent_to_bytes(referent)
    assert ref.bytes_to_referent(bytes) == '5'

# test get in class ValueRef
def test_get_ValueRef():
    ref = ValueRef()
    db = connect('test.dbdb')
    storage = db._storage
    ref._referent = '1111'
    ref.store(storage)
    assert ref.get(storage) == '1111'
    os.remove('test.dbdb')

# test store in class ValueRef
def test_store_ValueRef():
    ref = ValueRef()
    db = connect('test.dbdb')
    storage = db._storage
    ref._referent = '007'
    ref.store(storage)
    assert ref.get(storage) == '007'
    os.remove('test.dbdb')


# test prepare_to_store in class RedBlackNodeRef
def test_prepare_to_store_RedBlackNodeRef():
    ref = RedBlackNodeRef()
    db = connect('test.dbdb')
    storage = db._storage
    ref._referent = RedBlackNode(ValueRef(), '1', ValueRef(), ValueRef(), ValueRef())
    ref.prepare_to_store(storage)
    node = ref.get(storage)
    assert type(node) == RedBlackNode
    assert node.key == '1'
    os.remove('test.dbdb')


# test referent_to_bytes and bytes_to_referent in class RedBlackNodeRef
def test_referent_to_bytes_RedBlackNodeRef():
    ref = RedBlackNodeRef()
    db = connect('test.dbdb')
    storage = db._storage
    referent = RedBlackNode(ValueRef(), '1', ValueRef(), ValueRef(),ValueRef())
    bytes = ref.referent_to_bytes(referent)
    node = ref.bytes_to_referent(bytes)
    assert node.key == '1'
    os.remove('test.dbdb')


# test init method in class RedBlackNode
def test_init_RedBlackNode():
    node = RedBlackNode(ValueRef(), '1', ValueRef(), ValueRef(), ValueRef())
    assert type(node) == RedBlackNode
    assert node.key == '1'

# test store_refs in class RedBlackNode
def test_store_refs_RedBlackNode():
    ref = ValueRef()
    db = connect('test.dbdb')
    storage = db._storage
    ref._referent = '000'
    node = RedBlackNode(ValueRef(), '1', ref, ValueRef(), ValueRef())
    node.store_refs(storage)
    assert node.value_ref.get(storage) == '000'
    os.remove('test.dbdb')

# test is_empty in class RedBlackNode
def test_is_empty_RedBlackNode():
    node = RedBlackNode(ValueRef(), '1', ValueRef(), ValueRef(), ValueRef())
    assert node.is_empty() == False

# test is_black in class RedBlackNode
def test_is_black_RedBlackNode():
    node = RedBlackNode(ValueRef(), '1', ValueRef(), ValueRef(), ValueRef(Color.RED))
    assert node.is_black() == False

# test is_red in class RedBlackNode
def test_is_red_RedBlackNode():
    node = RedBlackNode(ValueRef(), '1', ValueRef(), ValueRef(), ValueRef(Color.RED))
    assert node.is_red() == True

# test blacken in class RedBlackNode
def test_blacken_RedBlackNode():
    node = RedBlackNode(ValueRef(), '1', ValueRef(), ValueRef(), ValueRef(Color.RED))
    node = node.blacken()
    assert node.is_black() == True

# test reden in class RedBlackNode
def test_reden_RedBlackNode():
    node = RedBlackNode(ValueRef(), '1', ValueRef(), ValueRef(), ValueRef(Color.BLACK))
    node = node.reden()
    assert node._follow(node.color_ref) == "red"

# test rotate_left in class RedBlackNode
def test_rotate_left_RedBlackNode():
    leftRef = RedBlackNodeRef(referent=RedBlackNode(ValueRef(), '1', ValueRef(), ValueRef(), ValueRef(Color.RED)))
    rightRef = RedBlackNodeRef(referent=RedBlackNode(ValueRef(), '2', ValueRef(), ValueRef(), ValueRef(Color.RED)))
    node = RedBlackNode(leftRef, '3', ValueRef(), rightRef, ValueRef(Color.RED))
    node = node.rotate_left()
    assert node.key == '2'

# test rotate_right in class RedBlackNode
def test_rotate_right_RedBlackNode():
    leftRef = RedBlackNodeRef(referent=RedBlackNode(ValueRef(), '1', ValueRef(), ValueRef(), ValueRef(Color.RED)))
    rightRef = RedBlackNodeRef(referent=RedBlackNode(ValueRef(), '3', ValueRef(), ValueRef(), ValueRef(Color.RED)))
    node = RedBlackNode(leftRef, '2', ValueRef(), rightRef, ValueRef(Color.RED))
    node = node.rotate_right()
    assert node.key == '1'

# test recolored in class RedBlackNode
def test_recolored_RedBlackNode():
    leftRef = RedBlackNodeRef(referent=RedBlackNode(ValueRef(), '1', ValueRef(), ValueRef(), ValueRef(Color.BLACK)))
    rightRef = RedBlackNodeRef(referent=RedBlackNode(ValueRef(), '3', ValueRef(), ValueRef(), ValueRef(Color.BLACK)))
    node = RedBlackNode(leftRef, '2', ValueRef(), rightRef, ValueRef(Color.RED))
    node = node.recolored()
    leftNode = node._follow(node.left_ref)
    rightNode = node._follow(node.right_ref)
    assert leftNode._follow(leftNode.color_ref) == "red"
    assert rightNode._follow(rightNode.color_ref) == "red"


# test init in class RedBlackTree
def test_init_RedBlackTree():
    db = connect('test.dbdb')
    storage = db._storage
    tree = RedBlackTree(storage)
    assert type(tree) == RedBlackTree
    os.remove('test.dbdb')

# test commit method in class RedBlackTree (whether the change is successfully made if it is not committed)
def test_commit_RedBlackTree():
    db = connect("test.dbdb")
    db.set("rahul", "aged")
    db.set("pavlos", "aged")
    db.set("kobe", "stillyoung")
    db.close()
    db = connect("test.dbdb")
    with raises(KeyError):
        db.get("pavlos")
    db.close()
    os.remove('test.dbdb')

# change the input sequence and test more rotation
def test_rotation_more_RedBlackTree():
    db = connect("test.dbdb")
    db.set("kobe", "stillyoung")
    db.set("pavlos", "aged")
    db.set("rahul", "aged")
    db.commit()
    db.close()
    newdb = connect("test.dbdb")
    assert newdb.get("pavlos")=="aged"
    newdb.close()
    os.remove('test.dbdb')

# test get and set in class RedBlackTree
def test_get_set_RedBlackTree():
    db = connect('test.dbdb')
    storage = db._storage
    rbtree = RedBlackTree(storage)
    rbtree.set('1', 'aaa')
    rbtree.set('2', 'bbb')
    rbtree.set('3', 'ccc')
    assert rbtree.get('3') == 'ccc'
    os.remove('test.dbdb')

# test insert in class RedBlackTree
def test_insert_RedBlackTree():
    db = connect('test.dbdb')
    storage = db._storage
    rbtree = RedBlackTree(storage)
    root = rbtree._follow(rbtree._tree_ref)
    value_ref = ValueRef('2')
    rbtree._tree_ref = rbtree._insert(root, '1', value_ref)
    assert rbtree._tree_ref._referent.key == '1'
    os.remove('test.dbdb')

# test follow in class RedBlackTree
def test_follow_RedBlackTree():
    db = connect('test.dbdb')
    storage = db._storage
    rbtree = RedBlackTree(storage)
    rbtree.set('1', '2')
    rbtree.set('2', '3')
    root = rbtree._follow(rbtree._tree_ref)
    assert root.key == '1'
    os.remove('test.dbdb')

# test _find_max in class RedBlackTree
def test__find_max_RedBlackTree():
    db = connect('test.dbdb')
    storage = db._storage
    rbtree = RedBlackTree(storage)
    rbtree.set('1', 2)
    rbtree.set('2', 3)
    rbtree.set('3', 4)
    root = rbtree._follow(rbtree._tree_ref)
    rbtree._find_max(root).key == '3'
    os.remove('test.dbdb')

# check if the tree is a red black tree
def test_red_black_tree():
    db = connect('test.dbdb')
    storage = db._storage
    rbtree = RedBlackTree(storage)
    rbtree.set(13, 'aaa')
    rbtree.set(8, 'bbb')
    rbtree.set(17, 'ccc')
    rbtree.set(1, 'ddd')
    rbtree.set(11, 'eee')
    rbtree.set(6, 'fff')
    rbtree.set(15, 'ggg')
    rbtree.set(25, 'hhh')
    rbtree.set(22, 'iii')
    rbtree.set(27, 'jjj')
    root = rbtree._follow(rbtree._tree_ref)
    leftNode = root._follow(root.left_ref)
    rightNode = root._follow(root.right_ref)
    leftleftNode = leftNode._follow(leftNode.left_ref)
    leftrightNode = leftNode._follow(leftNode.right_ref)
    rightleftNode = rightNode._follow(rightNode.left_ref)
    rightrightNode = rightNode._follow(rightNode.right_ref)
    leftleftrightNode = leftleftNode._follow(leftleftNode.right_ref)
    rightrightleftNode = rightrightNode._follow(rightrightNode.left_ref)
    rightrightrightNode = rightrightNode._follow(rightrightNode.right_ref)

    q = Queue()
    q.put(root)
    q.put(leftNode)
    q.put(rightNode)
    q.put(leftleftNode)
    q.put(leftrightNode)
    q.put(rightleftNode)
    q.put(rightrightNode)
    q.put(leftleftrightNode)
    q.put(rightrightleftNode)
    q.put(rightrightrightNode)

    #level = 1
    assert q.empty() == False
    node1 = q.get()
    assert node1.key == 13
    assert node1._follow(node1.color_ref) == "black"
    # level = 2
    node2 = q.get()
    assert node2.key == 8
    assert node2._follow(node2.color_ref) == "red"
    node3 = q.get()
    assert node3.key == 17
    assert node3._follow(node3.color_ref) == "red"
    # level = 3
    node4 = q.get()
    assert node4.key == 1
    assert node4._follow(node4.color_ref) == "black"
    node5 = q.get()
    assert node5.key == 11
    assert node5._follow(node5.color_ref) == "black"
    node6 = q.get()
    assert node6.key == 15
    assert node6._follow(node6.color_ref) == "black"
    node7 = q.get()
    assert node7.key == 25
    assert node7._follow(node7.color_ref) == "black"
    # level = 4
    node8 = q.get()
    assert node8.key == 6
    assert node8._follow(node8.color_ref) == "red"
    node9 = q.get()
    assert node9.key == 22
    assert node9._follow(node9.color_ref) == "red"
    node10 = q.get()
    assert node10.key == 27
    assert node10._follow(node10.color_ref) == "red"

    os.remove('test.dbdb')

