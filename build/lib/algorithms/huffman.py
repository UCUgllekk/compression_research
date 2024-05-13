'''Huffman algorithm implementation'''
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


class HuffmanCompression:
    """
    Class for compression and decompression, uses
    Huffman algorithm.
    """
    def __init__(self) -> None:
        """
        Initializes dict of symbols and name of algorithm
        """
        self.main_dict = {}
        self.name = 'huffm'

    def generate_code(self, node: 'Node', coding: str) -> None:
        """
        Generates all codings of symbols
        """
        if node.char is not None:
            char = node.char
            code = coding
            self.main_dict[char] = code
        else:
            self.generate_code(node.left_child, coding + '0')
            self.generate_code(node.right_child, coding + '1')

    def encode(self, text: str) -> tuple[str, dict[bytes, str]]:
        """
        Encoder functions, returns sequence of bits and dict of all codings.
        """
        frequency = self.frequency(text)
        nodes = []
        for (char, freq) in frequency:
            nodes.append(Node(freq=freq, char=char))
        while len(nodes) > 1:
            first_lowest = nodes[0]
            second_lowest = nodes[1]
            min_freq = nodes.pop(0).freq + nodes.pop(0).freq
            new_node = Node(freq=min_freq)
            new_node.left_child = first_lowest
            new_node.right_child = second_lowest
            nodes.append(new_node)
            nodes = sorted(nodes, key= lambda x: x.freq)
        self.generate_code(nodes[0], '')
        coded_str = ''
        for i in text:
            coded_str += self.main_dict[i]
        return (coded_str, self.main_dict)

    def frequency(self, text: bytes):
        """
        Function that helps calculate the frequency of all symbols
        """
        freq = {}
        for char in text:
            if char not in freq:
                freq[char] = 1
            else:
                freq[char] += 1
        return sorted(freq.items(), key= lambda x: x[1])

    def decode(self, code: str, coding_dict: dict[bytes, str]) -> bytes:
        """
        Decodes files
        """
        decoded_str = bytearray()
        coding_dict = {i : j for j, i in coding_dict.items()}
        while code:
            for cd in coding_dict:
                if code.startswith(cd):
                    decoded_str += bytes([coding_dict[cd]])
                    code = code[len(cd):]
        return decoded_str

    def add_fictious_bins(self, bin_str: str) -> str:
        """
        Adds fictious bits in the end, so that sequence
        can be fully transformed into bytes. Also adds
        byte representaion of nums of added bits, so that
        correct number will be removed in decompression
        """
        fictious = 8 - len(bin_str) % 8
        for i in range(fictious):
            bin_str += '0'
        fictious_info_secret = "{0:08b}".format(fictious)
        return fictious_info_secret + bin_str

    def remove_fictious(self, bin_str: str):
        """
        Removes fictious bits
        """
        fict_info = bin_str[:8]
        fict_info = int(fict_info, 2)
        bin_str = bin_str[8:]
        return bin_str[:-1 * fict_info]

    def compress(self, path: str) -> None:
        """
        Compresses files, uses encode func to generate
        sequence of bits
        """
        with open(path, 'rb') as file:
            image = file.read()
        encoded_data, encoded_dict = self.encode(image)
        file_type = path[len(path)-3:]
        encoded_data = self.add_fictious_bins(encoded_data)
        b = bytearray()
        for i in range(0, len(encoded_data), 8):
            byte = encoded_data[i:i+8]
            b.append(int(byte, 2))
        with open((path:=path[:-3]+self.name.lower()), 'wb') as file:
            file.write(bytes(b))
        return path, encoded_dict, file_type

    def decompress(self, file_mix: tuple[str, dict, str]) -> None:
        """
        Removes fictious bits and decompresses files.
        """
        output_path = file_mix[0][:-4] + '_decoded.' + file_mix[2]
        with open(file_mix[0], 'rb') as file:
            bit_str = ''
            byte = file.read(1)
            while len(byte) > 0:
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, '0')
                bit_str += bits
                byte = file.read(1)
            bit_str = self.remove_fictious(bit_str)
            decompr = self.decode(bit_str, file_mix[1])
        with open(output_path, 'wb') as writte:
            writte.write(bytes(decompr))
