import heapq
from collections import Counter
import numpy as np

class TreeNode:
    def __init__(self, symbol=None, freq=None, left=None, right=None) -> None:
        self.symbol = symbol
        self.freq = freq
        self.left = left
        self.right = right
    
    def __lt__(self, other):
        return self.freq < other.freq

class Huffman:

    def __init__(self, data) -> None:
        self._symbols_frequencies = Counter(data)
        self._symbols_codes = self.compute_codes()
        self._codes_symbols = dict(map(reversed, self.compute_codes().items()))


    def _assign_code(self, node, code="", mapping={}):
        if node:
            if node.symbol:
                mapping[node.symbol] = code
            self._assign_code(node.left, code + '0', mapping)
            self._assign_code(node.right, code + '1', mapping)
        
        return mapping


    def compute_codes(self):
        pq = [TreeNode(s, f) for s, f in self._symbols_frequencies.items()]
        heapq.heapify(pq)
        
        while len(pq) > 1:
            left_child = heapq.heappop(pq)
            right_child = heapq.heappop(pq)
            internal_node = TreeNode(freq=left_child.freq + right_child.freq, left=left_child, right=right_child)
            heapq.heappush(pq, internal_node)


        root = pq[0]


        return self._assign_code(root)

    
    def encode(self, stream:np.array)->str:
        encoded_stream = ""
        
        for symbol in stream:
                if symbol in self._symbols_codes.keys():
                    encoded_stream += self._symbols_codes[symbol]            
    

        return encoded_stream 

    def decode(self, stream:str)->np.array:
        stream_length = len(stream)
        decoded_stream = []

        i = 0
        while i<stream_length:
            for j in range(i+1,stream_length+1):
                if stream[i:j] in self._codes_symbols.keys():

                    decoded_stream.append(self._codes_symbols[stream[i:j]])
                    break
            i=j

        decoded_stream = np.array(decoded_stream) 

        return decoded_stream
