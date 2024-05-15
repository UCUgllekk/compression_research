'''Huffman algorithm implementation'''
import os
import pickle
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
    name = 'huff'
    def __init__(self) -> None:
        """
        Initializes dict of symbols and name of algorithm
        """
        self.main_dict = {}

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
        for [char, freq] in frequency:
            nodes.append(Node(freq, char))
        while len(nodes) > 1:
            first_lowest = nodes[0]
            second_lowest = nodes[1]
            min_freq = nodes.pop(0).freq + nodes.pop(0).freq
            new_node = Node(min_freq)
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
        unique_symbols = set(text)
        len_text = len(text)
        symbols_and_freqs = []
        for sym in unique_symbols:
            symbols_and_freqs.append([sym, text.count(sym) / len_text])
        symbols_and_freqs = sorted(symbols_and_freqs, key=lambda el: el[1])
        return symbols_and_freqs

    def decode(self, code: str, coding_dict: dict[bytes, str]) -> bytes:
        """
        Decodes files
        """
        decoded_str = bytearray()
        coding_dict = {i : j for j, i in coding_dict.items()}
        buffer = ''
        for bit in code:
            buffer += bit
            if buffer in coding_dict:
                decoded_str += bytes([coding_dict[buffer]])
                buffer = ''
        return decoded_str

    def add_fictious_bins(self, bin_str: str) -> str:
        """
        Adds fictious bits in the end, so that sequence
        can be fully transformed into bytes. Also adds
        byte representaion of nums of added bits, so that
        correct number will be removed in decompression
        """
        fictious = (8 - len(bin_str) % 8)
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

    def dict_to_bytes(self, dictt: dict):
        """
        Converts dicts to bytes
        """
        keys = bytes(dictt.keys())
        values = bytes(':'.join(dictt.values()), encoding='utf-8')
        data = keys + b'separ' + values + b'end'
        return data

    def dict_from_bytes(self, data: bytes):
        """
        Converts dict(expressed by bytes) to dict
        """
        data = data.split(b'separ')
        keys = list(data[0])
        values = list(data[1].decode('utf-8').split(':'))
        reconstructed_dict = {}
        for i in range(len(keys)):
            key = keys[i]
            value = values[i]
            reconstructed_dict[key] = value
        return reconstructed_dict

    def compress(self, path: str) -> None:
        """
        Compresses files, uses encode func to generate
        sequence of bits
        """
        with open(path, 'rb') as file:
            image = file.read()
        encoded_data, encoded_dict = self.encode(image)
        encoded_data = self.add_fictious_bins(encoded_data)
        b = bytearray()
        for i in range(0, len(encoded_data), 8):
            byte = encoded_data[i:i+8]
            b.append(int(byte, 2))
        new_path = f'{path}.{self.name}'
        dict_to_byte = self.dict_to_bytes(encoded_dict)
        with open(new_path, 'wb') as file:
            file.write(dict_to_byte)
            file.write(bytes(b))
        return new_path

    def decompress(self, file: tuple[str, dict, str]) -> None:
        """
        Removes fictious bits and decompresses files.
        """
        o_u = os.path.splitext(file)
        f_f = os.path.splitext(o_u[0])
        output_path = f_f[0] + '_decoded' + f_f[1]
        with open(file, 'rb') as file:
            file = file.read()
            encoded_dict = file[:file.index(b'end')]
            file = file[file.index(b'end')+3:]
            encoded_dict = self.dict_from_bytes(encoded_dict)
            bit_str = ''
            for byte in file:
                bits = bin(byte)[2:].rjust(8, '0')
                bit_str += bits
            bit_str = self.remove_fictious(bit_str)
            decompr = self.decode(bit_str, encoded_dict)
        with open(output_path, 'wb') as writte:
            writte.write(bytes(decompr))
        return output_path

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

    def encode(self, data: str) -> list[Node]:
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

    def decode(self, code: list[Node]) -> str:
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

    def compress(self, path: str):
        with open(path, 'r') as file:
            data = file.read()
        compressed_data = self.encode(data)
        file_path = path + f'.{self.name}'
        with open(file_path, 'wb') as file:
            pickle.dump(compressed_data, file)
        return file_path

    def decompress(self, path: str):
        with open(path, 'rb') as file:
            compressed_data = pickle.load(file)
        decompressed_data = self.decode(compressed_data)
        file_path = path[:-4][::-1].split('.', maxsplit=1)
        file_path = '.'.join([file_path[1][::-1] + "_decoded", file_path[0][::-1]])
        with open(file_path, 'w') as file:
            file.write(decompressed_data)
        return file_path
