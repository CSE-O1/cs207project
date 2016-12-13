import pickle
from queue import Queue


class Color(object):
    RED = 'red'
    BLACK = 'black'


class ValueRef(object):
    """
    a reference to a string value on disk
    """

    def __init__(self, referent=None, address=0):
        """
        Initializes a value reference that takes in a referent and the address in disk.

        Parameters:
        referent -- Node
        address -- Address of the stored node

        Returns:
        None
        """
        self._referent = referent  # value to store
        self._address = address  # address to store at

    @property
    def address(self):
        """
        Address on disk of the value.
        """
        return self._address

    def prepare_to_store(self, storage):
        """
        Used in subclass RedBlackNodeRef to store refs in the provided Storage.
        """
        pass

    @staticmethod
    def referent_to_bytes(referent):
        """
        Convert referent data (utf-8 string) to bytes.

        Parameters:
        referent -- Node

        Returns:
        Bytes
        """
        return referent.encode('utf-8')

    @staticmethod
    def bytes_to_referent(bytes):
        """
        Converts bytes to utf-8 string.

        Parameters:
        bytes

        Returns:
        string
        """
        return bytes.decode('utf-8')

    def get(self, storage):
        """
        Read bytes for value from disk (storage) at the ref's address and return a utf-8 string.

        Parameters:
        storage

        Returns:
        utf-8 string
        """
        if self._referent is None and self._address:
            self._referent = self.bytes_to_referent(storage.read(self._address))
        return self._referent

    def store(self, storage):
        """
        Store bytes for value to disk

        Parameters:
        storage

        Returns:
        None
        """
        # called by RedBlackNode.store_refs
        if self._referent is not None and not self._address:
            self.prepare_to_store(storage)
            self._address = storage.write(self.referent_to_bytes(self._referent))


class RedBlackNodeRef(ValueRef):
    """
    Subclass of ValueRef
    calls the RedBlackNode's store_refs
    """

    def prepare_to_store(self, storage):
        """
        Have a node store its refs
        similar with ValueRef's store

        Parameters:
        storage

        Returns:
        None
        """
        if self._referent:
            self._referent.store_refs(storage)

    @staticmethod
    def referent_to_bytes(referent):
        """
        Use pickle to convert node to bytes

        Parameters：
        referent

        Returns：
        Bytes
        """
        return pickle.dumps({
            'left': referent.left_ref.address,
            'key': referent.key,
            'value': referent.value_ref.address,
            'right': referent.right_ref.address,
            'color': referent.color_ref.address
        })

    @staticmethod
    def bytes_to_referent(string):
        """
        Unpickle bytes to get a node object

        Parameters：
        string

        Returns：
        RedBlackNode
        """
        d = pickle.loads(string)
        return RedBlackNode(
            RedBlackNodeRef(address=d['left']),
            d['key'],
            ValueRef(address=d['value']),
            RedBlackNodeRef(address=d['right']),
            ValueRef(address=d['color'])
        )


class RedBlackNode(object):
    """
    Binary node in a Red Black Tree
    Node has a left_ref, right_ref, key, value_ref and color.
    """
    storage = 0

    @classmethod
    def from_node(cls, node, **kwargs):
        """
        Clone a node with some changes from another one
        """
        return cls(
            left_ref=kwargs.get('left_ref', node.left_ref),
            key=kwargs.get('key', node.key),
            value_ref=kwargs.get('value_ref', node.value_ref),
            right_ref=kwargs.get('right_ref', node.right_ref),
            color_ref=kwargs.get('color_ref', node.color_ref)
        )

    def __init__(self, left_ref, key, value_ref, right_ref, color_ref):
        """
        Initializes a RedBlackNode

        Parameters:
        left_ref -- RedBlackNodeRef with key lesser than this node's key
        key: string
        value_ref: ValueRef containing string value referent
        right_ref: RedBlackNodeRef with key greater than this node's key
        color: Color of Red Black Tree node, either RED or BLACK

        Returns:
        None
        """
        self.left_ref = left_ref
        self.key = key
        self.value_ref = value_ref
        self.right_ref = right_ref
        self.color_ref = color_ref

    def store_refs(self, storage):
        """
        Method for node to store all of its refs to the storage
        store would call prepare_to_store which recursively stores the whole tree

        Parameters:
        None

        Returns
        self (left and right node blackened, and own color red)
        """
        self.value_ref.store(storage)
        # calls RedBlackNodeRef.store. which calls
        # RedBlackNodeRef.prepate_to_store
        # which calls this again and recursively stores
        # the whole tree
        self.left_ref.store(storage)
        self.right_ref.store(storage)
        self.color_ref.store(storage)

    def is_empty(self):
        """
        Return whether the RedBlackNode is empty
        """
        return False

    def is_black(self):
        """
        Returns true if the node is black, else false

        Parameters:
        None

        Returns:
        True if node is black, else false
        """
        return self._follow(self.color_ref) == Color.BLACK

    def is_red(self):
        """
        Returns true if the node is red, else false

        Parameters:
        None

        Returns:
        True if node is red, else false
        """
        return self._follow(self.color_ref) == Color.RED

    def blacken(self):
        """
        If node is red, returns a blackened node, otherwise returns self

        Parameters:
        None

        Returns:
        black node if node is red, else self
        """
        if self.is_red():
            return RedBlackNode.from_node(
                self,
                color_ref=ValueRef(Color.BLACK)
            )
        return self

    def reden(self):
        """
        If node is black, returns a redened node, otherwise returns self

        Parameters:
        None

        Returns:
        red node if node is black, else self
        """
        if self.is_black():
            return RedBlackNode.from_node(
                self,
                color_ref=ValueRef(Color.RED)
            )
        return self

    def rotate_left(self):
        """
        Rotates a node along left axis.

        Parameters:
        None

        Returns:
        self, that has been rotated
        """
        rchild = self._follow(self.right_ref)
        rlchild = self._follow(rchild.left_ref)
        rrchild = self._follow(rchild.right_ref)
        return RedBlackNode(
            RedBlackNodeRef(RedBlackNode.from_node(
                self,
                right_ref=RedBlackNodeRef(referent=RedBlackEmptyNode().update(rlchild))
            )),
            rchild.key,
            rchild.value_ref,
            RedBlackNodeRef(referent=rrchild),
            rchild.color_ref
        )

    def rotate_right(self):
        """
        Rotates a node along right axis.

        Parameters:
        None

        Returns:
        self, that has been rotated
        """
        lchild = self._follow(self.left_ref)
        llchild = self._follow(lchild.left_ref)
        lrchild = self._follow(lchild.right_ref)
        return RedBlackNode(
            RedBlackNodeRef(referent=llchild),
            lchild.key,
            lchild.value_ref,
            RedBlackNodeRef(referent=RedBlackNode.from_node(
                self,
                left_ref=RedBlackNodeRef(referent=RedBlackEmptyNode().update(lrchild)),
            )),
            lchild.color_ref
        )

    def recolored(self):
        """
        If the node is black, blacken left and right nodes and reden self
        If the node is red, reden left and right nodes and blacken self

        Parameters:
        None

        Returns:
        self
        """
        lchild = self._follow(self.left_ref)
        rchild = self._follow(self.right_ref)
        if self.is_black():
            return RedBlackNode.from_node(
                self,
                left_ref=RedBlackNodeRef(referent=lchild.blacken()),
                right_ref=RedBlackNodeRef(referent=rchild.blacken()),
                color_ref=ValueRef(Color.RED)
            )
        else:
            return RedBlackNode.from_node(
                self,
                left_ref=RedBlackNodeRef(referent=lchild.reden()),
                right_ref=RedBlackNodeRef(referent=rchild.reden()),
                color_ref=ValueRef(Color.BLACK)
            )

    def balance(self):
        """
        Balance the subtree rooted at the node based on Red Black Tree property.
        If the node is red, no need to rebalance

        Parameters:
        None

        Returns:
        self (after being balanced).
        """
        lchild = self._follow(self.left_ref)
        rchild = self._follow(self.right_ref)
        llchild = self._follow(lchild.left_ref)
        lrchild = self._follow(lchild.right_ref)
        rlchild = self._follow(rchild.left_ref)
        rrchild = self._follow(rchild.right_ref)
        if self.is_red():
            return self

        if lchild.is_red():
            if rchild.is_red():
                if llchild.is_red() or lrchild.is_red() or lrchild.is_red() or rrchild.is_red():
                    return self.recolored()
                return self
            if llchild.is_red():
                return self.rotate_right().recolored()
            if lrchild.is_red():
                return RedBlackNode.from_node(
                    self,
                    left_ref=RedBlackNodeRef(referent=lchild.rotate_left())
                ).rotate_right().recolored()
            return self

        if rchild.is_red():
            if rrchild.is_red():
                return self.rotate_left().recolored()
            if rlchild.is_red():
                return RedBlackNode.from_node(
                    self,
                    right_ref=RedBlackNodeRef(referent=rchild.rotate_right())
                ).rotate_left().recolored()
        return self

    def update(self, node):
        """
        Update the subtree rooted at the current node with a new node.

        Parameters:
        Node

        Returns:
        self (after being updated).
        """
        lchild = self._follow(self.left_ref)
        rchild = self._follow(self.right_ref)
        if node.key == "Invalid Key":
            return self
        if node.key < self.key:
            return RedBlackNode.from_node(
                self,
                left_ref=RedBlackNodeRef(referent=lchild.update(node).balance())
            ).balance()
        return RedBlackNode.from_node(
            self,
            right_ref=RedBlackNodeRef(referent=rchild.update(node).balance())
        ).balance()

    def insert(self, key, value_ref):
        """
        Insert the paired key and value_ref into the subtree rooted at the current node.

        Parameters:
        Node

        Returns:
        self (after insertion).
        """
        return self.update(RedBlackNode(
            RedBlackNodeRef(referent=RedBlackEmptyNode()),
            key,
            value_ref,
            RedBlackNodeRef(referent=RedBlackEmptyNode()),
            color_ref=ValueRef(Color.RED)
        )).blacken()

    def _follow(self, ref):
        """
        Get a node from a reference
        call RedBlackNodeRef.get
        """
        return ref.get(RedBlackNode.storage)


class RedBlackEmptyNode(RedBlackNode):
    """
    Empty red black node
    """

    def __init__(self):
        """
        Initialization with invalid key and non-exist value_ref. The color of the root is black.
        """
        self.color_ref = ValueRef(Color.BLACK)
        self.value_ref = ValueRef("Doesn't exist")
        self.key = "Invalid Key"

    def is_empty(self):
        """
        Return True since the node is empty
        """
        return True

    def insert(self, key, value_ref):
        """
        Insert the paired key and value_ref into the subtree rooted at the current node.
        """
        return RedBlackNode(
            RedBlackNodeRef(referent=RedBlackEmptyNode()),
            key,
            value_ref,
            RedBlackNodeRef(referent=RedBlackEmptyNode()),
            color_ref=ValueRef(Color.BLACK)
        )

    def update(self, node):
        """
        Update the empty node with a new node.
        """
        return node

    @property
    def left_ref(self):
        return ValueRef()

    @property
    def right_ref(self):
        return ValueRef()


class RedBlackTree(object):
    """
    Immutable RedBlackTree Tree class.
    """

    def __init__(self, storage):
        """
        Initializes a balanced Red Black tree from a provided storage.

        Parameters:
        storage

        Returns:
        None
        """
        self._storage = storage
        self._refresh_tree_ref()
        RedBlackNode.storage = storage

    def commit(self):
        """
        Changes are final only when committed, which stores the root into disk.

        Parameters:
        None

        Returns:
        None
        """
        # trigger RedBlackNodeRef.store
        self._tree_ref.store(self._storage)
        # make sure address of new tree is stored
        self._storage.commit_root_address(self._tree_ref.address)

    def _refresh_tree_ref(self):
        """
        Get reference to the new tree if changed.

        Parameters:
        None

        Returns:
        None
        """
        self._tree_ref = RedBlackNodeRef(
            address=self._storage.get_root_address())

    def get(self, key):
        """
        Returns the node with the input key

        Parameters:
        key -- String key

        Returns:
        RedBlackNode with the key
        """
        # if tree is not locked by another writer
        # refresh the references and get new tree if needed
        if not self._storage.locked:
            self._refresh_tree_ref()
        # get the top level node
        node = self._follow(self._tree_ref)
        # traverse until you find appropriate node
        while node is not None:
            if key < node.key:
                node = self._follow(node.left_ref)
            elif key > node.key:
                node = self._follow(node.right_ref)
            else:
                return self._follow(node.value_ref)
        raise KeyError

    def set(self, key, value):
        """
        Set a new value in the tree with a key (Balance is also done), which will cause a new tree.

        Parameters:
        key -- String key
        value -- String value

        Returns:
        None
        """
        # try to lock the tree. If we succeed make sure we don't lose updates from any other process
        if self._storage.lock():
            self._refresh_tree_ref()
        # get current top-level node and make a value-ref
        node = self._follow(self._tree_ref)
        value_ref = ValueRef(value)
        # insert and get new tree ref
        self._tree_ref = self._insert(node, key, value_ref)

    def get_smaller_nodes(self, key):
        "find all of the nodes in RBTree whose key is less than given KEY"
        if not self._storage.locked:
            self._refresh_tree_ref()
        node = self._follow(self._tree_ref)
        smaller_keys, smaller_vals = [], []
        # using DFS recursion function to find smaller nodes
        smaller_keys, smaller_vals = self.dfs_helper(key, node, smaller_keys, smaller_vals)
        return smaller_keys, smaller_vals

    def dfs_helper(self, key, node, smaller_keys, smaller_vals):
        "DFS recursion helper function for get_smaller_nodes"
        if node.key == "Invalid Key":
            return smaller_keys, smaller_vals
        elif key >= node.key:
            smaller_keys.append(node.key)
            smaller_vals.append(self._follow(node.value_ref))
            # for right node
            right_node = self._follow(node.right_ref)
            self.dfs_helper(key, right_node, smaller_keys, smaller_vals)
        # for left node
        left_node = self._follow(node.left_ref)
        self.dfs_helper(key, left_node, smaller_keys, smaller_vals)
        return smaller_keys, smaller_vals

    def _insert(self, node, key, value_ref):
        """
        Insert key and value_ref into the tree (balance is done along the way), which creats a new path from root.

        Parameters:
        node -- current RedBlackNode
        key -- String key
        value_ref -- RedBlackNodeRef encapsulating value

        Returns:
        RedBlackNodeRef with node after insertion
        """
        # create a tree if there was none so far
        if node is None:
            new_node = RedBlackEmptyNode().insert(key, value_ref)
        else:
            new_node = node.insert(key, value_ref)

        return RedBlackNodeRef(referent=new_node)

    def _follow(self, ref):
        """
        Get a node from the reference by calling RedBlackNodeRef's get.

        Parameters:
        ref -- BinaryNodeRef

        Returns:
        RedBlackNode
        """
        return ref.get(self._storage)

    def _find_max(self, node):
        """
        Find the max value in the subtree of the node by traversing to the most right child

        Parameters:
        ref -- RedBlackNodeRef

        Returns:
        RedBlackNode
        """
        while True:
            next_node = self._follow(node.right_ref)
            if next_node is None:
                return node
            node = next_node
