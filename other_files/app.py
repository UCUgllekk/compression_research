'''App for compression'''
import tkinter as tk
from tkinter import filedialog
from threading import Thread
import os
import sys
sys.path.insert(0, '/home/gllekk/all_the_code/default/DISCRETE/compression_research')
from algorithms import LZW, HuffmanCompression, LZ77, LZ78, Deflate

class CompressionProgramGUI:
    '''Compression app'''
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Compression App")
        self.root.geometry("800x300")
        self.root.resizable(False, False)

        self.app_label = tk.Label(self.root, text="Choose an algorithm for compression",
                                    font=('Fira Code', '12'))
        self.app_label.pack()

        self.algorithm_var = tk.StringVar()

        self.menu_button = tk.Menubutton(self.root, text="Select Algorithm", relief="raised",
                                            font=('Fira Code', '10'))
        self.menu = tk.Menu(self.menu_button, tearoff=False)

        self.menu.add_radiobutton(label="Huffman", variable=self.algorithm_var,
                                  value="huffman", command=self.update_algorithm_text_field,
                                  font=('Fira Code', '10'))

        self.menu.add_radiobutton(label="LZW", variable=self.algorithm_var,
                                value="lzw", command=self.update_algorithm_text_field,
                                font=('Fira Code', '10'))

        self.menu.add_radiobutton(label="LZ77", variable=self.algorithm_var,
                                value="lz78", command=self.update_algorithm_text_field,
                                font=('Fira Code', '10'))

        self.menu.add_radiobutton(label="LZ78", variable=self.algorithm_var,
                                value="lz77", command=self.update_algorithm_text_field,
                                font=('Fira Code', '10'))

        self.menu.add_radiobutton(label="Deflate", variable=self.algorithm_var,
                                value="deflate", command=self.update_algorithm_text_field,
                                font=('Fira Code', '10'))

        self.menu_button["menu"] = self.menu
        self.menu_button.pack()

        self.algorithm_label = tk.Label(self.root, text="Algorithm chosen: None",
                                        font=('Fira Code', '12'))
        self.algorithm_label.pack()

        self.button = tk.Button(self.root,
                                text="Compress File",
                                state="disabled",
                                font=('Fira Code', '12'))

        self.compressed_file_label = tk.Label(self.root,
                                              text="",
                                              font=('Fira Code', '12'))

        self.compressed_file_path_label = tk.Entry(self.root,
                                                   font=('Fira Code', '10'),
                                                   width=97,
                                                   state="disabled")

        self.size_label = tk.Label(self.root, text="", font=('Fira Code', '10'))

        self.button.pack()

    def update_algorithm_text_field(self):
        '''Algorithm chosen text'''
        self.algorithm_label.config(text=f"Algorithm chosen: \
{self.algorithm_var.get().capitalize()}", font=('Fira Code', '12'))
        self.button.config(state="normal", command=self.compress_file)

    def compress_file(self):
        '''Open file'''
        file_path = filedialog.askopenfilename()
        thread = Thread(target=self.run_compression, args=(file_path,))
        thread.start()

    def run_compression(self, file_path):
        '''Compress'''
        if self.algorithm_var.get() == 'huffman':
            compression_algorithm = HuffmanCompression()
            compressed_file_path = compression_algorithm.compress(file_path)

        elif self.algorithm_var.get() == 'lzw':
            compression_algorithm = LZW()
            compressed_file_path = compression_algorithm.compress(file_path)

        elif self.algorithm_var.get() == 'lz77':
            compression_algorithm = LZ77()
            compressed_file_path, _ = compression_algorithm.compress(file_path)

        elif self.algorithm_var.get() == 'lz78':
            compression_algorithm = LZ78()
            compressed_file_path, _ = compression_algorithm.compress(file_path)

        elif self.algorithm_var.get() == 'deflate':
            compression_algorithm = Deflate()
            compressed_file_path, _ = compression_algorithm.compress(file_path)

        self.compressed_file_label.pack()
        self.compressed_file_label.config(text="Compressed file path:")
        self.compressed_file_path_label.config(state="normal")
        self.compressed_file_path_label.delete(0, tk.END)
        self.compressed_file_path_label.insert(0, compressed_file_path)
        self.compressed_file_path_label.config(state="readonly")
        self.compressed_file_path_label.pack()
        self.size_label.pack()

        original_size = round(os.path.getsize(file_path) / 1024, 2)
        compressed_size = round(os.path.getsize(compressed_file_path) / 1024,2)
        compression_percentage = 100 * (original_size - compressed_size) / original_size

        self.size_label.config(text=f"Original file size: {original_size} kb\n\
Compressed file size: {compressed_size} kb\nCompression percentage: {compression_percentage:.2f}%")

    def start(self):
        '''Open app'''
        self.root.mainloop()

if __name__=="__main__":
    gui = CompressionProgramGUI()
    gui.start()
