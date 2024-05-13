"""LZW algorithm implementation"""
class LZW:
    '''LZW compression algorithm'''
    name = 'lzw'
    @staticmethod
    def encoding(data: bytes) -> list:
        '''LZW encoding'''
        output = []
        w = b''
        dictionary = {bytes([i]): i for i in range(256)}
        for byte in data:
            byte = bytes([byte])
            wc = w + byte
            if wc in dictionary:
                w = wc
            else:
                output.append(dictionary[w])
                dictionary[wc] = len(dictionary)
                w = byte
        if w:
            output.append(dictionary[w])
        return output

    @staticmethod
    def decoding(code: list) -> bytes:
        '''LZW decoding'''
        coding_dict = {i:bytes([i]) for i in range(256)}
        string = coding_dict[code[0]]
        output = bytearray()
        output += string
        for i in range(1, len(code)):
            new = code[i]
            if new not in coding_dict:
                entry = string + string[:1]
            else:
                entry = coding_dict[new]
            output += entry
            coding_dict[len(coding_dict)] = string + entry[:1]
            string = entry
        return bytes(output)

    @staticmethod
    def compress(path:str):
        '''Encode and write to file'''
        with open(path, 'rb') as file:
            data = file.read()
        encoded_data = LZW.encoding(data)
        file_type = path.split('.')[-1]
        file_path = '.'.join(path.split('.')[:-1])+'.'+ LZW.name.lower()
        with open(file_path, 'wb') as file:
            for value in encoded_data:
                file.write(value.to_bytes(3, byteorder='little'))
        return file_path, file_type

    @staticmethod
    def decompress(path:str, file_type:str):
        '''Read, decode, write to file'''
        with open(path, 'rb') as file:
            encoded_data = []
            while (byte := file.read(3)):
                encoded_data.append(int.from_bytes(byte, byteorder='little'))
        decoded = LZW.decoding(encoded_data)
        file_path = '.'.join(path.split('.')[:-1])+'_decoded.'+ file_type
        with open(file_path, 'wb') as file:
            file.write(decoded)
