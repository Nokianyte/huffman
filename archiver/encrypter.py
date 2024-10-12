import os
from collections import Counter
from heapq import heapify, heappop, heappush
from string import hexdigits

class Node:

    def __init__(self, letter=None, freq=0, children=None):
        self.letter = letter
        self.freq = freq
        self.children = children or []

    def tuple(self):
        return (self.freq, ord(self.letter) if self.letter else -1)

    def __lt__(self, other):
        return self.tuple() < other.tuple()

    def __eq__(self, other):
        return self.tuple() == other.tuple()


def encoding_table(node, code=''):

    if node.letter is None:
        mapping = {}
        for child, digit in zip(node.children, hexdigits):
            mapping.update(encoding_table(child, code + digit))
        return mapping
    else:
        return {node.letter: code}


def huffman_encode(text, arity=2):

    nodes = [Node(letter, freq) for letter, freq in Counter(text).items()]
    heapify(nodes)

    # Строит n-арное дерево
    while len(nodes) > 1:
        list_children = [heappop(nodes) for _ in range(arity)]
        freq = sum([node.freq for node in list_children])

        node = Node(None, freq)
        node.children = list_children

        heappush(nodes, node)

    root = nodes[0]
    codes = encoding_table(root)
    print(root)

    return root, ''.join([codes[letter] for letter in text])

q = input('Введите "1" чтобы скомпрессовать или "0" чтобы восстановить файл:')

if q == "1":

    orig = open('decompressed.txt','r')
    comp = open('compressed.txt','wb')

    text = orig.read()
    table = ''
    dict = encoding_table(huffman_encode(text)[0])
    for i in range(len(dict)):
        for j in range(2): table+=list(dict.items())[i][j]
    comp.write(table)
    n = int(huffman_encode(text)[1], 2)
    comp.write(n.to_bytes((n.bit_length() + 7) // 8, 'big'))

    orig.close()
    comp.close()

    orig_size = os.path.getsize('decompressed.txt')
    comp_size = os.path.getsize('compressed.txt')
    print('Размер оригинального файла:', orig_size, 'байт')
    print('Размер скомпрессованного файла:', comp_size, 'байт')

elif q == "0":

    orig = open('decompressed.txt','w')
    comp = open('compressed.txt','rb')

    orig.close()
    comp.close()

    orig_size = os.path.getsize('original.txt')
    comp_size = os.path.getsize('compressed.txt')
    print('Размер оригинального файла:', orig_size, 'байт')
    print('Размер скомпрессованного файла:', comp_size, 'байт')

