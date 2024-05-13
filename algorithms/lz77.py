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
    def __init__(self, buffer_size: int):
        self.buffer_size = buffer_size

    def find_best_match(self, cur_ind: int, data: str) -> Node:
        buffer = data[max(0, cur_ind - self.buffer_size):cur_ind]
        if data[cur_ind] not in buffer:
            return Node(freq=0, char=data[cur_ind])

        possib = [ind for ind, elem in enumerate(buffer) if elem == data[cur_ind]]
        possib = [cur_ind - len(buffer) + elem for elem in possib]

        best_match = Node(freq=0, char=data[cur_ind])
        for offset in possib:
            length = 0
            while cur_ind + length < len(data) and data[cur_ind + length] == data[offset + length]:
                length += 1
                if len(buffer) == self.buffer_size:
                    buffer = buffer[1:] + data[cur_ind + length - 1]
                else:
                    buffer += data[cur_ind + length - 1]

            if cur_ind + length == len(data):
                char = data[-1]
                best_match = Node(freq=length + 1, offset=offset, next_byte=char) if char == data[offset + length - 1] else Node(freq=length, offset=offset, next_byte=char)
                break
            elif length >= best_match.length:
                best_match = Node(freq=length, offset=offset, next_byte=data[cur_ind + length])

        return best_match

    def encode_string(self, data: str) -> list[Node]:
        result = []
        cur_ind = 0
        while cur_ind < len(data):
            match = self.find_best_match(cur_ind, data)
            if match is None or match.length == 0:
                result.append(Node(freq=1, char=data[cur_ind]))
                cur_ind += 1
            else:
                result.append(match)
                cur_ind += match.length
        return result

    def decode_string(self, code: list[Node]) -> str:
        result = []
        decoded_data = ""
        for node in code:
            if node.char is not None:
                result.append(node.char)
                decoded_data += node.char
            else:
                for _ in range(node.length):
                    result.append(result[-node.offset])
                    decoded_data += result[-node.offset]
        return decoded_data