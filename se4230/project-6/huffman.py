# PART 3.2
from priority_queue import PriorityQueue

class Node:
    """A node of a Huffman tree. Leaves have a symbol | internal nodes have children."""
    __slots__ = ("weight", "symbol", "left", "right", "parent")

    def __init__(self, weight, symbol=None, left=None, right=None):
        self.weight = weight
        self.symbol = symbol
        self.left = left      # edge = 0
        self.right = right    # edge = 1
        self.parent = None

    def is_leaf(self):
        return self.left is None and self.right is None


class Codec:
    """Huffman tree + a hash map from symbol -> leaf node."""

    def __init__(self, root, leaves):
        self.root = root
        self.leaves = leaves   # dict: symbol -> leaf Node

    def encode(self, symbols):
        """YIELD the bits for each symbol. O(total bits) time."""
        for symbol in symbols:
            node = self.leaves[symbol]          
            path = []
            while node.parent is not None:
                path.append(0 if node.parent.left is node else 1)
                node = node.parent
            yield from reversed(path)

    def decode(self, bits):
        """YIELD symbols from a stream of bits. O(number of bits) time."""
        node = self.root
        for bit in bits:
            if bit == 0:
                node = node.left
            elif bit == 1:
                node = node.right
            else:
                raise ValueError(f"Shouldn't happen? Not a bit: {bit!r}")
            if node is None:
                raise ValueError("bit sequence does not match this codec")
            if node.is_leaf():
                yield node.symbol
                node = self.root
        if node is not self.root:
            raise ValueError("bit sequence ended in the middle of a code")


def huffman_codec(frequencies):
    """Build a Codec from an iterable of (symbol, frequency) pairs."""
    pq = PriorityQueue()
    leaves = {}
    next_id = 0

    for symbol, freq in frequencies:
        if symbol in leaves:
            raise ValueError(f"duplicate symbol: {symbol!r}")
        leaf = Node(freq, symbol=symbol)
        leaves[symbol] = leaf
        pq.update(next_id, freq, data=leaf)
        next_id += 1

    if not leaves:
        raise ValueError("need at least one symbol")

    if len(leaves) == 1:
        # A lone leaf would get a 0-bit code, which can't be decoded.
        # Give it a 1-bit code by hanging it under a root as the 0-child.
        (leaf,) = leaves.values()
        root = Node(leaf.weight, left=leaf)
        leaf.parent = root
        return Codec(root, leaves)

    while pq.count() > 1:
        ka = pq.peek_min()
        a = pq.get_data(ka)
        pq.remove(ka)
        kb = pq.peek_min()
        b = pq.get_data(kb)
        pq.remove(kb)

        parent = Node(a.weight + b.weight, left=a, right=b)
        a.parent = parent
        b.parent = parent
        pq.update(next_id, parent.weight, data=parent)
        next_id += 1

    root = pq.get_data(pq.peek_min())
    return Codec(root, leaves)


# "Implement and test [an encode and decode method]"
def test_encode():
    codec = huffman_codec([("a", 3), ("b", 8), ("c", 10), ("d", 14), ("e", 17), ("f", 42)])
    assert list(codec.encode("bacd")) == [int(n) for n in "10111010100110"]

def test_decode():
    codec = huffman_codec([("a", 3), ("b", 8), ("c", 10), ("d", 14), ("e", 17), ("f", 42)])
    assert list(codec.decode([int(n) for n in "10111010100110"])) == [*"bacd"]