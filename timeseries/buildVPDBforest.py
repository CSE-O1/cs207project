"""
Implementation of similarity searches using unbalanced binary search tree, wrapped into a database, with reference to implementation from  Lab 10

With 20 vantage points selected, there will be 20 BST.
Given a target TS, the nearest VP will be identified and searches will be carried out on the database associated with the vantage point

Classes:
--------
1. DBDB
- Methods:
        getRootKey(): return the key of the root node of the tree
        getNodeKey(node): returns the key of the node
        getLeftChildNode(node = 0): returns the left child node from parent node, with parent node set as the root node as the default
        getRightChildNode(node = 0): returns the right child node from parent node, with parent node set as the root node as the default

2. VantagePointDB
- Inherits from DBDB. 
- Note that there is no need for a connect method as the constructor opens connection to the filenames required
- Methods: 
    populate_VPDistTree(n, folderPath)
    Purpose: Takes a folder path and expects n timeseries files of the format 'ts_1000.npy' and create the VP database.
             Note this creates one database for a vantage point.
             Database is a binary search tree which contains key-value at each node, 
             where the key is the distance of the particular TS to the VP, and value is the name string of the TS
    Inputs - n: the total number of timeseries to be compared against the target TS
            folderPath: to be specified without the last '/', example: if TS files are in current folder, the input should be "." 

3. createVPForest(k = 20)
- Create a forest of VPDB, with k being 20 as the default. k corresponds to the number of vantage points identified as listed in VPDict

Preconditions:
-------------
- 1000 TS generated should follow the naming convention: 'ts_1.npy' ... to 'ts_1000.npy'

"""
import pickle
import os
import struct
import portalocker
import os
import timeseries.ArrayTimeSeries as ts
from timeseries.TimeSeriesDistance import tsmaker, random_ts, stand, ccor, max_corr_at_phase, kernel_corr, kcorr_dist
import numpy as np



class ValueRef(object):
    """
    Reference to a string value on disk
    Parameters
    ----------
    referent : optional
        The value to store (default is None)
    address : int, optional
        Address of the referent (default is 0)
        
    Attributes
    ----------
    _referent
    _address
        
    Notes
    -----
    WARNINGS:
        - return type of get for a value will always be a string type
    """

    def __init__(self, referent=None, address=0):
    #"""
    #Constructor for ValueRef.  Initializes with a value given by the `referent`
    #at the address given by `address`
        
    #Parameters
    #----------
    #referent : int/float/string, optional
    #    The value to be stored (default is None)
    #address : int, optional
    #    Address of the referent (default is 0)
    # """
        self._referent = referent #value to store
        self._address = address #address to store at
        
    @property
    def address(self):
        """returns address of the value"""
        return self._address
    
    def prepare_to_store(self, storage):
        """acts as a placeholder for BinaryNodRef method which stores refs"""
        pass

    @staticmethod
    def referent_to_bytes(referent):
        """converts string of referent value to bytes"""
        return referent.encode('utf-8')

    @staticmethod
    def bytes_to_referent(bytes):
        """converts bytes back to string of the referent value"""
        return bytes.decode('utf-8')

    
    def get(self, storage):
        "read bytes for value from disk"
        if self._referent is None and self._address:
            self._referent = self.bytes_to_referent(storage.read(self._address))
        return self._referent

    def store(self, storage):
        "store bytes for value to disk"
        #called by BinaryNode.store_refs
        if self._referent is not None and not self._address:
            self.prepare_to_store(storage)
            self._address = storage.write(self.referent_to_bytes(self._referent))

class BinaryNodeRef(ValueRef):
    """"
    A reference to a btree node on the disk. Specialized subclass of ValueRef to 
    serialize/deserialize a BinaryNode
    
    Parameters
    ----------
    referent : optional
        The value to store (default is None)
    address : int, optional
        Address of the referent (default is 0)
    """
    
    #calls the BinaryNode's store_refs
    def prepare_to_store(self, storage):
        "have a node store its refs"
        if self._referent:
            self._referent.store_refs(storage)

    @staticmethod
    def referent_to_bytes(referent):
        "use pickle to convert node to bytes"
        return pickle.dumps({
            'left': referent.left_ref.address,
            'key': referent.key,
            'value': referent.value_ref.address,
            'right': referent.right_ref.address,
        })

    @staticmethod
    def bytes_to_referent(string):
        "unpickle bytes to get a node object"
        d = pickle.loads(string)
        return BinaryNode(
            BinaryNodeRef(address=d['left']),
            d['key'],
            ValueRef(address=d['value']),
            BinaryNodeRef(address=d['right']),
        )

class BinaryNode(object):
    """
    Implements a node in the binary tree
    
    Parameters
    ----------
    left_ref : BinaryNodeRef
        Reference to the left child
    key:
        The key component in a key value pair
    value_ref: ValueRef
        Reference to the value that corresponds to key
    right_ref: BinaryNodeRef
        Reference to the right child
    
    Attributes
    ----------
    left_ref
    key
    value_ref
    right_ref
    """

    @classmethod
    def from_node(cls, node, **kwargs):
        "clone a node with some changes from another one"
        return cls(
            left_ref=kwargs.get('left_ref', node.left_ref),
            key=kwargs.get('key', node.key),
            value_ref=kwargs.get('value_ref', node.value_ref),
            right_ref=kwargs.get('right_ref', node.right_ref),
        )

    def __init__(self, left_ref, key, value_ref, right_ref):
        """
        Constructor for the BinaryNode class. Initializes with a `key`, a reference to the value
        given by `value_ref`, a reference to the left child `left_ref`, and a
        reference to the right child `right_ref`
        """

        self.left_ref = left_ref
        self.key = key
        self.value_ref = value_ref
        self.right_ref = right_ref

    def store_refs(self, storage):
        "method for a node to store all of its stuff"
        self.value_ref.store(storage)
        #calls BinaryNodeRef.store. which calls
        #BinaryNodeRef.prepate_to_store
        #which calls this again and recursively stores
        #the whole tree
        self.left_ref.store(storage)
        self.right_ref.store(storage)

class BinaryTree(object):
    """"
    Immutable Binary Tree class. Constructs a new tree when changes happen
    
    Parameters
    ----------
    storage : Storage
        A Storage object to manage storage of Binary Tree
        
    Attributes
    ----------
    _storage : Storage
        a storage object to manage read/write
    _tree_ref : BinaryNodeRef
        refrence to unbalanced bst, created when `self_refresh_tree_ref()` called in constructor
    Notes
    -----
    WARNINGS:
        - return type of get for a value will always be a string type
    """
    def __init__(self, storage):
        """
        Constructor for the BinaryTree class. Initialized with an instance of Storage 
        given by `storage`. The _refresh_tree_ref method initializes the value `_tree_ref`,
        a reference to the root node or root address of the tree, which is itself a BinaryNodeRef.
        """
        self._storage = storage
        self._refresh_tree_ref()

    def commit(self):
        "changes are final only when committed"
        #triggers BinaryNodeRef.store
        self._tree_ref.store(self._storage)
        #make sure address of new tree is stored
        self._storage.commit_root_address(self._tree_ref.address)

    def _refresh_tree_ref(self):
        "get reference to new tree if it has changed"
        self._tree_ref = BinaryNodeRef(
            address=self._storage.get_root_address())

    def get(self, key):
        "get value for a key"
        #if tree is not locked by another writer
        #refresh the references and get new tree if needed
        if not self._storage.locked:
            self._refresh_tree_ref()
        #get the top level node
        node = self._follow(self._tree_ref)
        #traverse until you find appropriate node
        while node is not None:
            if key < node.key:
                node = self._follow(node.left_ref)
            elif key > node.key:
                node = self._follow(node.right_ref)
            else:
                return self._follow(node.value_ref)
        raise KeyError

    def set(self, key, value):
        "set a new value in the tree. will cause a new tree"
        #try to lock the tree. If we succeed make sure
        #we dont lose updates from any other process
        if self._storage.lock():
            self._refresh_tree_ref()
        #get current top-level node and make a value-ref
        node = self._follow(self._tree_ref)
        value_ref = ValueRef(value)
        #insert and get new tree ref
        self._tree_ref = self._insert(node, key, value_ref)
        
    
    def _insert(self, node, key, value_ref):
        "insert a new node creating a new path from root"
        #create a tree ifnthere was none so far
        if node is None:
            new_node = BinaryNode(
                BinaryNodeRef(), key, value_ref, BinaryNodeRef())
        elif key < node.key:
            new_node = BinaryNode.from_node(
                node,
                left_ref=self._insert(
                    self._follow(node.left_ref), key, value_ref))
        elif key > node.key:
            new_node = BinaryNode.from_node(
                node,
                right_ref=self._insert(
                    self._follow(node.right_ref), key, value_ref))
        else: #create a new node to represent this data
            new_node = BinaryNode.from_node(node, value_ref=value_ref)
        return BinaryNodeRef(referent=new_node)

    def delete(self, key):
        "delete node with key, creating new tree and path"
        if self._storage.lock():
            self._refresh_tree_ref()
        node = self._follow(self._tree_ref)
        self._tree_ref = self._delete(node, key)
        
    def _delete(self, node, key):
        """underlying delete implementation. removes the node given by `node` when the `key` is a match.
        traverses tree until it reaches the matching key."""
        if node is None:
            raise KeyError
        elif key < node.key:
            new_node = BinaryNode.from_node(
                node,
                left_ref=self._delete(
                    self._follow(node.left_ref), key))
        elif key > node.key:
            new_node = BinaryNode.from_node(
                node,
                right_ref=self._delete(
                    self._follow(node.right_ref), key))
        else:
            left = self._follow(node.left_ref)
            right = self._follow(node.right_ref)
            if left and right:
                replacement = self._find_max(left)
                left_ref = self._delete(
                    self._follow(node.left_ref), replacement.key)
                new_node = BinaryNode(
                    left_ref,
                    replacement.key,
                    replacement.value_ref,
                    node.right_ref,
                )
            elif left:
                return node.left_ref
            else:
                return node.right_ref
        return BinaryNodeRef(referent=new_node)

    def _follow(self, ref):
        # """get a node from the given reference"""
        #calls BinaryNodeRef.get
        return ref.get(self._storage)
    
    def _find_max(self, node):
        """returns the right most node, which is the maximum"""
        while True:
            next_node = self._follow(node.right_ref)
            if next_node is None:
                return node
            node = next_node

class Storage(object):
    """
    Storage class manages access to disk, controlling the reads and writes 
    as well as locking of the files
    Parameters
    ----------
    f : file name (string)
        Database filename to store the binary tree
    Attributes
    ----------
    _f : string
        filename of the file to store to
    
    locked: bool
        indicator for status of storage lock
        
    Notes
    -----
    WARNINGS:
        - return type of get for a value will always be a string type
    """


    SUPERBLOCK_SIZE = 4096
    INTEGER_FORMAT = "!Q"
    INTEGER_LENGTH = 8

    def __init__(self, f):
        """
        Constructor for the Storage class. Initializes with storage in file `f`,
        initial storage being unlocked, and calls _ensure_superblock method so as 
        to ensure the first write starts on sector boundary.
        """
        self._f = f
        self.locked = False
        #we ensure that we start in a sector boundary
        self._ensure_superblock()

    def _ensure_superblock(self):
        "guarantee that the next write will start on a sector boundary"
        self.lock()
        self._seek_end()
        end_address = self._f.tell()
        if end_address < self.SUPERBLOCK_SIZE:
            self._f.write(b'\x00' * (self.SUPERBLOCK_SIZE - end_address))
        self.unlock()

    def lock(self):
        "if not locked, lock the file for writing"
        if not self.locked:
            portalocker.lock(self._f, portalocker.LOCK_EX)
            self.locked = True
            return True
        else:
            return False

    def unlock(self):
        """if locked, then unlock"""
        if self.locked:
            self._f.flush()
            portalocker.unlock(self._f)
            self.locked = False

    def _seek_end(self):
        """find the end of the storage file"""
        self._f.seek(0, os.SEEK_END)

    def _seek_superblock(self):
        "go to beginning of file which is on sec boundary"
        self._f.seek(0)

    def _bytes_to_integer(self, integer_bytes):
        """
        unpacks the string `integer_bytes` to format given by the `INTEGER_FORMAT`
        returns the corresponding integer value
        """
        return struct.unpack(self.INTEGER_FORMAT, integer_bytes)[0]

    def _integer_to_bytes(self, integer):
        """returns a string with value given by `integer` packed according to format given by `INTEGER_FORMAT`"""
        return struct.pack(self.INTEGER_FORMAT, integer)

    def _read_integer(self):
        """reads the next `INTEGER_LENGTH` positions in file and returns its integer value"""
        return self._bytes_to_integer(self._f.read(self.INTEGER_LENGTH))

    def _write_integer(self, integer):
        """writes to storage file value of `integer` in bytes"""
        self.lock()
        self._f.write(self._integer_to_bytes(integer))

    def write(self, data):
        """
        write data to disk, and return the address at which it is written
        first lock, get to end, get address to return, write size
        write data, do not unlock here

        """
        self.lock()
        self._seek_end()
        object_address = self._f.tell()
        self._write_integer(len(data))
        self._f.write(data)
        return object_address

    def read(self, address):
        """returns the data at the location given by `address`"""
        self._f.seek(address)
        length = self._read_integer()
        data = self._f.read(length)
        return data

    def commit_root_address(self, root_address):
        """write integer given by `root_address` into storage"""
        self.lock()
        self._f.flush()
        # write root address at position 0
        self._seek_superblock()
        #write is atomic because we store the address on a sector boundary.
        self._write_integer(root_address)
        self._f.flush()
        self.unlock()

    def get_root_address(self):
        """reads the first integer in the superblock"""
        #read the first integer in the file
        self._seek_superblock()
        root_address = self._read_integer()
        return root_address

    def close(self):
        """closes the storage file"""
        self.unlock()
        self._f.close()

    @property
    def closed(self):

        """checks if the storage file is closed and returns True if closed"""
        return self._f.closed

class DBDB(object):
    """
    The DBDB class acts as a database, it holds the binary tree of all key, value 
    pairs, as well as its storage manager
    
    Parameters
    ----------
    f : string
        Database filename to store the binary tree
        
    Attributes
    ----------
    _storage : Storage
        storage to be used with `_tree`
    _tree : BinaryTree
        unbalanced binary tree initialized with storage `_storage`
        
    Notes
    -----
    PRE:
        - `key` must be of type int, float, or str
        - `value` must be of type str
        
    WARNINGS:
        - return type of `self._tree.get` for will always be a string type
        - `DBDB.get` will always try to convert output to an int or float if possible,
        otherwise it will be left as a string
    """

    # constructor: creates a binary tree and stores on disk
    def __init__(self, f):

        """
        Constructor for DBDB. Initiallizes with storage in
        file `f` and a binary tree is created with the initialized storage
        
        Parameters
        ----------
        f : file name (string)
            Database filename to store the binary tree
        """
        self._storage = Storage(f)
        self._tree = BinaryTree(self._storage)

    def _assert_not_closed(self):
        """checks that the database is open, and raises error if not"""
        if self._storage.closed:
            raise ValueError('Database closed.')

    def close(self):
        """closes the storage"""
        self._storage.close()

    def commit(self):
        """
        saves the final changes
        calls BinaryTree commit to save
        """
        self._assert_not_closed()
        self._tree.commit()

    def get(self, key):
        """
        returns the final value stored with key
        calls BinaryTree get method to traverse the tree's branches
        """
        self._assert_not_closed()
        return self._tree.get(key)
    
    def getRootKey(self):
        """refreshes the references and gets the new tree root key if needed"""
        if not self._tree._storage.locked:
            self._tree._refresh_tree_ref()
        #get the top level node
        node = self._tree._follow(self._tree._tree_ref)
        return node.key
    
    def getNodeKey(self, node):
        """gets key of 'node'"""
        return node.key
    
    def getLeftChildNode(self, node = 0):
        """gets the left child node"""
        if node == 0:
            node = self._tree._follow(self._tree._tree_ref)
        node = self._tree._follow(node.left_ref)
        return node
    
    def getRightChildNode(self, node = 0):
        """gets the right child node"""
        if node == 0:
            node = self._tree._follow(self._tree._tree_ref)
        node = self._tree._follow(node.right_ref)
        return node         

    def set(self, key, value):
        """
        assigns a new value to key
        calls BinaryTree set to set the key, value
        """
        self._assert_not_closed()
        return self._tree.set(key, value)

    def delete(self, key):
        """
        deletes node with key and its value
        calls BinaryTree delete to delete the node
        """
        self._assert_not_closed()
        return self._tree.delete(key)


def selectVPs(n = 20):
    """
    Randomly chose 20 vantage points from the 1000 TS generated, and create 20 database indexes
    and return dictionary with numeric key from 1 - 20 and values are (name of TS selected as VP, name of database) 

    Example of returned value: {('ts_806.npy', 'VPDB1.dbdb'), ...}

    Precondition:
    ------------
    The name of the timeseries generated should follow the format 'ts_1.npy' ... to 'ts_1000.npy' 
    """
    VPindex = np.random.choice(np.arange(1, 1001), size = n, replace = False)
    VPDict = {}
    for i in range(n):
        VPfileName = 'ts_'+ str(VPindex[i]) +'.npy'
        VPDB = 'data2/VPDB'+ str(i + 1) + '.dbdb'
        VPDict[i+1] =  (VPfileName, VPDB)
    return VPDict


class VantagePointDB(DBDB):
    """
    Class to create an unbalanced binary search tree database for one single Vantage Point
    BST key is the distance from the vantage point to all other timeseries points in the space
    BST value is the name of the respective timeseries file
    This class inherits from the class DBDB

    Parameters
    ---------
    Constructor takes 2 filenames:
    VPdbfilename: file name that will hold the Vantage Point BST 
    VPtsfilename: file name that contains the vantage point timeseries

    Attributes
    ---------
    VPDBfile : file name that will hold the Vantage Point BST 
    VPTSfile : file name that contains the vantage point timeseries
    VPDict: a dictionary which the key is just numeric index from 1 to n, and value is a tuple (vptsfilename, name of vantage point database filename)
    
    Pre-condition:
    -------------
    All timeseries files must already exist in file name syntax like this 'ts_1.npy' ... to 'ts_1000.npy' 
    
    WARNINGS
    --------
    - File directory for timeseries assumes UNIX OS syntax 
    - Will raise exception if timeseries files do not exist in current directory
    
    """

    def __init__(self, VPdbfilename, VPtsfilename, VPDict = {}):

        self.VPDBfile = VPdbfilename
        self.VPTSfile = VPtsfilename
        self.VPDict = VPDict
        try:
            f = open(self.VPDBfile, 'r+b')
        except IOError:
            fd = os.open(self.VPDBfile, os.O_RDWR | os.O_CREAT)
            f = os.fdopen(fd, 'r+b')
        DBDB.__init__(self, f)
        

    def populate_VPDistTree(self, n, folderPath):
        """
        Create a single VP BST for n timeseries in the space with BST index as distance, for a single Vantage Point

        Parameters:
        n: number of timeseries to be compared with against the vantage point
        folderPath: folder that contains the n timeseries files. If run on the current directory, it is '.' 
        """
        # load VP timeseries
        vantagePoint = ts.ArrayTimeSeries(np.load(folderPath+self.VPTSfile))
        stdVP =  stand(vantagePoint, vantagePoint.mean(), vantagePoint.std())
        # load each of the n timeseries
        for i in range(n):
            # tsFileName = str(folderPath) + '/' + 'ts_' +str(i + 1)+'.npy'
            tsFileName = './data2/ts_' + str(i + 1) + '.npy'
            TS = ts.ArrayTimeSeries(np.load(tsFileName))
            # standardize TS
            stdts = stand(TS, TS.mean(), TS.std())
            distance = kcorr_dist(kernel_corr(stdts, stdVP))
            self.set(distance, tsFileName)
        self.commit()
        self.close()
        
def createVPForest(k = 20, n = 1000):
    """
    Function creates k vantage point databases from n timeseries and populates VPDict
    Returns vpdb list that contains k instances of VPDB

    WARNINGS
    --------
    - File directory name to save VPDB assumes UNIX OS syntax 
          
    """
    # create a dictionary of {index: (ts, name of .dbdb)
    vpdbList = []
    VPDict = selectVPs()
    for i in range(k):
        # vpdb = VantagePointDB("./" + VPDict[i+1][1] , "./" + VPDict[i+1][0], VPDict)
        vpdb = VantagePointDB(VPDict[i + 1][1], VPDict[i + 1][0], VPDict)
        vpdb.populate_VPDistTree(n, './data2/')
        # store list of vpdb instances
        vpdbList.append(vpdb)
    return vpdbList

