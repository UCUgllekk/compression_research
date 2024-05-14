"""LZ78 algorithm implementation"""
class LZ78:
    """LZ78 class"""
    name = 'lz78'
    def compress(self, path):
        res = bytearray()
        with open(path, "rb") as fl:
            data = fl.read()
        one = 1
        zero = 0
        dict_of_codes = {data[0]: one.to_bytes(3, "big")}
        res += zero.to_bytes(3, "big")
        res += bytes([data[0]])
        data = data[1:]
        b_str = b""
        code = 2
        file_path = path + f'.{self.name}'
        for byte in data:
            b_str += bytes([byte])
            if b_str not in dict_of_codes:
                dict_of_codes[b_str] = code.to_bytes(3, "big")
                if len(b_str) == 1:
                    res += zero.to_bytes(3, "big")
                    res += b_str
                else:
                    res += dict_of_codes[b_str[:-1]]
                    res += bytes([b_str[-1]])
                code += 1
                b_str = b""
        with open(file_path, "wb") as fil:
            fil.write(res)
        return file_path

    def decompress(self, file_path:str):
        with open(file_path, 'rb') as f:
            compressed_data = f.read()
        file_path = file_path[:-5][::-1].split('.', maxsplit=1)
        file_path = '.'.join([file_path[1][::-1] + "_decoded", file_path[0][::-1]])
        print(file_path)
        with open(file_path, "wb") as res:
            one = 1
            zero = 0
            dict_of_codes = {
                zero.to_bytes(3, "big"): b"",
                (one_ := one.to_bytes(3, "big")): bytes([compressed_data[3]]),
            }
            res.write(dict_of_codes[one_])
            compressed_data = compressed_data[4:]
            string = b""
            code = 2
            start_ind = True
            counter = 0
            for char in compressed_data:

                if start_ind:
                    string += bytes([char])
                    counter += 1
                    if counter == 3:
                        start_ind = False

                else:
                    dict_of_codes[code.to_bytes(3)] = dict_of_codes[string] + bytes([char])
                    res.write(dict_of_codes[string])
                    res.write(bytes([char]))
                    code += 1
                    string = b""
                    counter = 0
                    start_ind = True
        return file_path
