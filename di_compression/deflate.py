"""Deflate, algorithm implementation"""
from .lz77 import LZ77
from .huffman import HuffmanCompression
import pickle

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
        print(data)
        data = data.split(b'|')
        keys = list(data[0])
        values = data[1].split(b':')

        reconstructed_dict = {}
        for i in range(len(keys)):
            key = keys[i]
            if i < len(values):
                value = values[i]
                if value == b'_':
                    reconstructed_dict[key] = None
                else:
                    reconstructed_dict[key] = value
            else:
                reconstructed_dict[key] = None

        return reconstructed_dict

    def compress(self, file_path: str) -> bytes:
        with open(file_path, 'rb') as file:
            data = file.read()
        compressed_data = self.deflate(data)
        compressed_file_path = file_path + '.deflate'
        with open(compressed_file_path, 'wb') as file:
            pickle.dump(compressed_data[1], file)
            file.write(self.dict_to_bytes(compressed_data[0]))
        return compressed_file_path

    def decompress(self, path: str) -> str:
        with open(path, 'rb') as file:
            compressed_lz77_nodes = pickle.load(file)
            compressed_dict = self.dict_from_bytes(file.readline().rstrip())
        file_path = path[:-7][::-1].split('.', maxsplit=1)
        file_path = '.'.join([file_path[1][::-1] + "_decoded", file_path[0][::-1]])
        huffman_dict = compressed_dict
        huffman_encoded = self.lz77.decode(compressed_lz77_nodes)
        decoded_text = self.huffman.decode(huffman_encoded, huffman_dict)
        with open(file, 'wb') as output_file:
            output_file.write(decoded_text)
        return file_path

    def deflate(self, text: str) -> bytes:
        huffman_encoded, huffman_dict = self.huffman.encode(text)
        lz77_nodes = self.lz77.encode(huffman_encoded)
        combined_data = huffman_dict, lz77_nodes
        return combined_data

    def inflate(self, compressed_data: bytes) -> str:
        huffman_dict, lz77_nodes = compressed_data
        huffman_encoded = self.lz77.decode(lz77_nodes)
        decoded_text = self.huffman.decode(huffman_encoded, huffman_dict)
        return decoded_text
