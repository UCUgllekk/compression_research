"""Deflate algorithm implementation"""
import pickle
from .lz77 import LZ77
from .huffman import HuffmanCompression
class Deflate:
    '''Deflate'''
    name = 'deflate'
    def __init__(self, buffer_size: int):
        self.huffman = HuffmanCompression()
        self.lz77 = LZ77(buffer_size)

    def dict_to_bytes(self, dictt):
        keys = bytes(dictt.keys())
        values = bytes(':'.join(dictt.values()), encoding='utf-8')
        data = keys + b'|' + values
        return data

    def dict_from_bytes(self, data):
        data = data.split(b'|')
        keys = list(data[0])
        values = list(data[1].decode('utf-8').split(':'))
        reconstructed_dict = {}
        for i in range(len(keys)):
            key = keys[i]
            value = values[i]
            reconstructed_dict[key] = value.replace('_', '')
        return reconstructed_dict

    def deflate(self, text: str) -> bytes:
        huffman_encoded, huffman_dict = self.huffman.encode(text)
        lz77_nodes = self.lz77.encode(huffman_encoded)
        combined_data = huffman_dict, lz77_nodes
        return combined_data

    def huff_decode(self, code: str, coding_dict: dict[bytes, str]) -> bytes:
        """
        Decodes files
        """
        decoded_str = ''
        coding_dict = {i : j for j, i in coding_dict.items()}
        while code:
            for cd in coding_dict:
                if code.startswith(cd):
                    decoded_str += coding_dict[cd]
                    code = code[len(cd):]
        return decoded_str

    def inflate(self, compressed_data: bytes) -> str:
        huffman_dict, lz77_nodes = compressed_data
        huffman_encoded = self.lz77.decode(lz77_nodes)
        decoded_text = self.huff_decode(huffman_encoded, huffman_dict)
        return decoded_text

    def compress(self, file_path: str) -> bytes:
        with open(file_path, 'rb') as file:
            data = file.read()
        compressed_data = self.deflate(data)
        compressed_file_path = file_path + f'.{self.name}'
        with open(compressed_file_path, 'wb') as file:
            pickle.dump(compressed_data[1], file)
            file.write(self.dict_to_bytes(compressed_data[0]))
        return compressed_file_path

    def decompress(self, compressed_file_path: str) -> str:
        with open(compressed_file_path, 'rb') as file:
            compressed_lz77_nodes = pickle.load(file)
            compressed_dict = self.dict_from_bytes(file.readline().rstrip())
        out_file_name = compressed_file_path.replace('.deflate', '')
        huffman_dict = compressed_dict
        huffman_encoded = self.lz77.decode(compressed_lz77_nodes)
        decoded_text = self.huffman.decode(huffman_encoded, huffman_dict)
        with open(out_file_name, 'wb') as output_file:
            output_file.write(decoded_text)
        return out_file_name
