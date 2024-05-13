"""LZ77 algorithm implementation"""
class Node:
    """
    Class Node for Huffman and LZ77 algorithms.
    """
    def __init__(self, freq: bytes, char=None, offset=None, length=0, next_byte=None):
        """
        Initializes a node with relevant attributes.
        """
        self.freq = freq
        self.char = char
        self.offset = offset
        self.length = length
        self.next_byte = next_byte
        self.left_child = None
        self.right_child = None

    def __repr__(self):
        """
        String representation of the node.
        """
        if self.char is not None:
            return f'("{self.char}", {self.freq})'
        else:
            return f'(Offset: {self.offset}, Length: {self.length}, Next Byte: {self.next_byte})'

class LZ77:
    '''LZ77'''
    name = 'lz77'
    ...
