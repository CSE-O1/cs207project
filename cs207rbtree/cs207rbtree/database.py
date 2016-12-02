import os
import struct
import portalocker
from cs207rbtree.tree import RedBlackTree

class Storage(object):
    SUPERBLOCK_SIZE = 4096
    INTEGER_FORMAT = "!Q"
    INTEGER_LENGTH = 8

    def __init__(self, f):
        """
        Initializes storage from a file

        Parameters:
        f -- File

        Returns:
        None
        """
        self._f = f
        self.locked = False
        #we ensure that we start in a sector boundary
        self._ensure_superblock()

    def _ensure_superblock(self):
        """
        Guarantees that the next write will start on a sector boundary

        Parameters:
        None

        Returns:
        None
        """
        self.lock()
        self._seek_end()
        end_address = self._f.tell()
        if end_address < self.SUPERBLOCK_SIZE:
            self._f.write(b'\x00' * (self.SUPERBLOCK_SIZE - end_address))
        self.unlock()

    def lock(self):
        """
        If it's not locked, lock the file for writing.

        Parameters:
        None

        Returns:
        None
        """
        if not self.locked:
            portalocker.lock(self._f, portalocker.LOCK_EX)
            self.locked = True
            return True
        else:
            return False

    def unlock(self):
        """
        If it's locked, flush and unlock.

        Parameters:
        None

        Returns:
        None
        """
        if self.locked:
            self._f.flush()
            portalocker.unlock(self._f)
            self.locked = False

    def _seek_end(self):
        """
        Go to the end of the file
        """
        self._f.seek(0, os.SEEK_END)

    def _seek_superblock(self):
        """
        Go to beginning of file which is on sec boundary.
        """
        self._f.seek(0)

    def _bytes_to_integer(self, integer_bytes):
        """
        Convert bytes to integer

        Parameters:
        integer_bytes -- Bytes

        Returns:
        Integer
        """
        return struct.unpack(self.INTEGER_FORMAT, integer_bytes)[0]

    def _integer_to_bytes(self, integer):
        """
        Convert integer to bytes

        Parameters:
        integer

        Returns:
        bytes
        """
        return struct.pack(self.INTEGER_FORMAT, integer)

    def _read_integer(self):
        """
        Read in an integer
        """
        return self._bytes_to_integer(self._f.read(self.INTEGER_LENGTH))

    def _write_integer(self, integer):
        """
        Lock and write an integer
        """
        self.lock()
        self._f.write(self._integer_to_bytes(integer))

    def write(self, data):
        """
        Write data to disk, returning the adress at which you wrote it

        Parameters:
        data

        Returns:
        address
        """
        # first lock, get to end, get address to return, write size
        # write data, unlock <==WRONG, dont want to unlock here
        self.lock()
        self._seek_end()
        object_address = self._f.tell()
        self._write_integer(len(data))
        self._f.write(data)
        return object_address

    def read(self, address):
        """
        Read data from the address

        Parameters:
        address

        Returns:
        data
        """
        self._f.seek(address)
        length = self._read_integer()
        data = self._f.read(length)
        return data

    def commit_root_address(self, root_address):
        """
        Lock, write root address at position 0, then unlock.
        """
        self.lock()
        self._f.flush()
        # make sure you write root address at position 0
        self._seek_superblock()
        # write is atomic because we store the address on a sector boundary.
        self._write_integer(root_address)
        self._f.flush()
        self.unlock()

    def get_root_address(self):
        """
        Get root address, which is the first integer in the file
        """
        # read the first integer in the file
        self._seek_superblock()
        root_address = self._read_integer()
        return root_address

    def close(self):
        """
        Close the storage by unlocking it and closing the disk (file)
        """
        self.unlock()
        self._f.close()

    @property
    def closed(self):
        """
        Returns true if storage is closed, false otherwise

        Parameters:
        None

        Returns:
        True if storage closed, False otherwise
        """
        return self._f.closed


class DBDB(object):
    """
    DBDB class contains both the tree and its associated storage (disk)
    Functions are wrappers around tree and storage.
    """

    def __init__(self, f):
        """
        Initialize DBDB with a file, and create the tree and its associated storage

        Parameters:
        f: File

        Returns:
        None
        """
        self._storage = Storage(f)
        self._tree = RedBlackTree(self._storage)

    def _assert_not_closed(self):
        """
        Raises an error when associated storage is closed
        """
        if self._storage.closed:
            raise ValueError('Database closed.')

    def close(self):
        """
        Closes associated storage
        """
        self._storage.close()

    def commit(self):
        """
        Commits changes to the tree
        """
        self._assert_not_closed()
        self._tree.commit()

    def get(self, key):
        """
        Get the value associated with the key from the tree
        """
        self._assert_not_closed()
        return self._tree.get(key)

    def set(self, key, value):
        """
        Set the value at the associated key in the tree
        """
        self._assert_not_closed()
        return self._tree.set(key, value)

    def delete(self, key):
        """
        delete the key
        """
        self._assert_not_closed()
        return self._tree.delete(key)


def connect(dbname):
    try:
        f = open(dbname, 'r+b')
    except IOError:
        fd = os.open(dbname, os.O_RDWR | os.O_CREAT)
        f = os.fdopen(fd, 'r+b')
    return DBDB(f)
