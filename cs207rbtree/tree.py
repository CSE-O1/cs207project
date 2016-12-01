"""
TODO:
1. Add BST module, and refactoring red-black tree
2. Unittest
3. 
"""
import pickle
from queue import Queue


class Color(object):
    RED = 'red'
    BLACK = 'black'


class ValueRef(object):
    " a reference to a string value on disk"
    def __init__(self, referent=None, address=0):
        self._referent = referent  # value to store
        self._address = address  # address to store at

    @property
    def address(self):
        return self._address

    def prepare_to_store(self, storage):
        pass

    @staticmethod
    def referent_to_bytes(referent):
        return referent.encode('utf-8')

    @staticmethod
    def bytes_to_referent(bytes):
        return bytes.decode('utf-8')

    def get(self, storage):
        "read bytes for value from disk"
        if self._referent is None and self._address:
            self._referent = self.bytes_to_referent(storage.read(self._address))
        return self._referent

    def store(self, storage):
        "store bytes for value to disk"
        # called by RedBlackNode.store_refs
        if self._referent is not None and not self._address:
            self.prepare_to_store(storage)
            self._address = storage.write(self.referent_to_bytes(self._referent))


class RedBlackNodeRef(ValueRef):
    "reference to a btree node on disk"

    # calls the RedBlackNode's store_refs
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
            'color': referent.color_ref.address
        })

    @staticmethod
    def bytes_to_referent(string):
        "unpickle bytes to get a node object"
        d = pickle.loads(string)
        return RedBlackNode(
            RedBlackNodeRef(address=d['left']),
            d['key'],
            ValueRef(address=d['value']),
            RedBlackNodeRef(address=d['right']),
            ValueRef(address=d['color'])
        )


class RedBlackNode(object):
    @classmethod
    def from_node(cls, node, **kwargs):
        "clone a node with some changes from another one"
        return cls(
            left_ref=kwargs.get('left_ref', node.left_ref),
            key=kwargs.get('key', node.key),
            value_ref=kwargs.get('value_ref', node.value_ref),
            right_ref=kwargs.get('right_ref', node.right_ref),
            color_ref=kwargs.get('color_ref', node.color_ref)
        )

    def __init__(self, left_ref, key, value_ref, right_ref, color_ref):
        self.left_ref = left_ref
        self.key = key
        self.value_ref = value_ref
        self.right_ref = right_ref
        self.color_ref = color_ref

    def store_refs(self, storage):
        "method for a node to store all of its stuff"
        self.value_ref.store(storage)
        # calls RedBlackNodeRef.store. which calls
        # RedBlackNodeRef.prepate_to_store
        # which calls this again and recursively stores
        # the whole tree
        self.left_ref.store(storage)
        self.right_ref.store(storage)
        self.color_ref.store(storage)

    def is_empty(self):
        return False

    def is_black(self, storage):
        return self.color_ref.get(storage) == Color.BLACK

    def is_red(self, storage):
        return self.color_ref.get(storage) == Color.RED

    def blacken(self, storage):
        if self.is_red(storage):
            return RedBlackNode.from_node(
                self,
                color_ref=ValueRef(Color.BLACK)
            )
        return self

    def reden(self, storage):
        if self.is_black(storage):
            return RedBlackNode.from_node(
                self,
                color_ref=ValueRef(Color.RED)
            )
        return self

    def rotate_left(self, storage):
        rchild = self.right_ref.get(storage)
        rlchild = rchild.left_ref.get(storage)
        rrchild = rchild.right_ref.get(storage)
        return RedBlackNode(
            RedBlackNodeRef(RedBlackNode.from_node(
                self,
                right_ref=RedBlackNodeRef(referent=RedBlackEmptyNode().update(rlchild, storage))
            )),
            rchild.key,
            rchild.value_ref,
            RedBlackNodeRef(referent=rrchild),
            rchild.color_ref
        )

    def rotate_right(self, storage):
        lchild = self.left_ref.get(storage)
        llchild = lchild.left_ref.get(storage)
        lrchild = lchild.right_ref.get(storage)
        return RedBlackNode(
            RedBlackNodeRef(referent=llchild),
            lchild.key,
            lchild.value_ref,
            RedBlackNodeRef(referent=RedBlackNode.from_node(
                self,
                left_ref=RedBlackNodeRef(referent=RedBlackEmptyNode().update(lrchild, storage)),
            )),
            lchild.color_ref
        )

    def recolored(self, storage):
        lchild = self.left_ref.get(storage)
        rchild = self.right_ref.get(storage)
        if self.is_black(storage):
            return RedBlackNode.from_node(
                self,
                left_ref=RedBlackNodeRef(referent=lchild.blacken(storage)),
                right_ref=RedBlackNodeRef(referent=rchild.blacken(storage)),
                color_ref=ValueRef(Color.RED)
            )
        else:
            return RedBlackNode.from_node(
                self,
                left_ref=RedBlackNodeRef(referent=lchild.reden(storage)),
                right_ref=RedBlackNodeRef(referent=rchild.reden(storage)),
                color_ref=ValueRef(Color.BLACK)
            )

    def balance(self, storage):
        lchild = self.left_ref.get(storage)
        rchild = self.right_ref.get(storage)
        llchild = lchild.left_ref.get(storage)
        lrchild = lchild.right_ref.get(storage)
        rlchild = rchild.left_ref.get(storage)
        rrchild = rchild.right_ref.get(storage)
        if self.is_red(storage):
            return self

        if lchild.is_red(storage):
            if rchild.is_red(storage):
                if llchild.is_red(storage) or lrchild.is_red(storage) or lrchild.is_red(storage) or rrchild.is_red(storage):
                    return self.recolored(storage)
                return self
            if llchild.is_red(storage):
                return self.rotate_right(storage).recolored(storage)
            if lrchild.is_red(storage):
                return RedBlackNode.from_node(
                    self,
                    left_ref=RedBlackNodeRef(referent=lchild.rotate_left(storage))
                ).rotate_right(storage).recolored(storage)
            return self

        if rchild.is_red(storage):
            if rrchild.is_red(storage):
                return self.rotate_left(storage).recolored(storage)
            if rlchild.is_red(storage):
                return RedBlackNode.from_node(
                    self,
                    right_ref=RedBlackNodeRef(referent=rchild.rotate_right(storage))
                ).rotate_left(storage).recolored(storage)
        return self

    def update(self, node, storage):
        lchild = self.left_ref.get(storage)
        rchild = self.right_ref.get(storage)
        if node.key == "Invalid key":
            return self
        if node.key < self.key:
            return RedBlackNode.from_node(
                self,
                left_ref=RedBlackNodeRef(referent=lchild.update(node, storage).balance(storage))
            ).balance(storage)
        return RedBlackNode.from_node(
            self,
            right_ref=RedBlackNodeRef(referent=rchild.update(node, storage).balance(storage))
        ).balance(storage)

    def insert(self, key, value_ref, storage):
        return self.update(
            RedBlackNode(
                RedBlackNodeRef(referent=RedBlackEmptyNode()),
                key,
                value_ref,
                RedBlackNodeRef(referent=RedBlackEmptyNode()),
                color_ref=ValueRef(Color.RED)
            ), storage
        ).blacken(storage)


class RedBlackEmptyNode(RedBlackNode):

    def __init__(self):
        self.color_ref = ValueRef(Color.BLACK)
        self.value_ref = ValueRef("Doesn't exist")
        self.key = "Invalid Key"

    def is_empty(self):
        return True

    def get(self, storage):
        return RedBlackEmptyNode()

    def insert(self, key, value_ref, storage):
        return RedBlackNode(
            RedBlackNodeRef(referent=RedBlackEmptyNode()),
            key,
            value_ref,
            RedBlackNodeRef(referent=RedBlackEmptyNode()),
            color_ref=ValueRef(Color.BLACK)
        )

    def update(self, node, storage):
        return node

    @property
    def left_ref(self):
        return ValueRef()

    @property
    def right_ref(self):
        return ValueRef()


class RedBlackTree(object):
    "Immutable Binary Tree class. Constructs new tree on changes"
    def __init__(self, storage):
        self._storage = storage
        self._refresh_tree_ref()

    def commit(self):
        "changes are final only when committed"
        # triggers RedBlackNodeRef.store
        self._tree_ref.store(self._storage)
        # make sure address of new tree is stored
        self._storage.commit_root_address(self._tree_ref.address)

    def _refresh_tree_ref(self):
        "get reference to new tree if it has changed"
        self._tree_ref = RedBlackNodeRef(
            address=self._storage.get_root_address())

    def get(self, key):
        "get value for a key"
        # your code here
        # if tree is not locked by another writer
        # refresh the references and get new tree if needed
        if not self._storage.locked:
            self._refresh_tree_ref()

        #BFS print to check the tree
        # print("*****************")
        # # node = self._follow(self._tree_ref)
        # node = self._tree_ref.get(self._storage)
        # q = Queue()
        # q.put(node)
        # #level = 1
        # #print (q.empty())
        # while not q.empty():
        #     nd=q.get()
        #     #print(nd)
        #     #print ("level: ", level)
        #     if nd==None:
        #         print("None")
        #     else:
        #         print (nd.key)
        #         print (self._follow(nd.color_ref))
        #         if nd.key != "Invalid Key":
        #             q.put(self._follow(nd.left_ref))
        #             q.put(self._follow(nd.right_ref))
        #
        # print("*****************")
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
        "set a new value in the tree. will cause a new tree"
        # try to lock the tree. If we succeed make sure
        # we dont lose updates from any other process
        if self._storage.lock():
            self._refresh_tree_ref()
        # get current top-level node and make a value-ref
        node = self._follow(self._tree_ref)
        value_ref = ValueRef(value)
        # insert and get new tree ref
        self._tree_ref = self._insert(node, key, value_ref)

    def _insert(self, node, key, value_ref):
        "insert a new node creating a new path from root"
        # create a tree ifnthere was none so far
        if node is None:
            new_node = RedBlackEmptyNode().insert(key, value_ref, self._storage)

        else:
            new_node = node.insert(key, value_ref, self._storage)

        return RedBlackNodeRef(referent=new_node)

    def _follow(self, ref):
        "get a node from a reference"
        # calls RedBlackNodeRef.get
        return ref.get(self._storage)

    def _find_max(self, node):
        while True:
            next_node = self._follow(node.right_ref)
            if next_node is None:
                return node
            node = next_node