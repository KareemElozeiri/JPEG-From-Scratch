import heapq
from collections import Counter


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

    
    def encode(self, stream:str)->str:
        stream_length = len(stream)
        encoded_stream = ""
        i = 0
        while i<stream_length:
            for j in range(i+1,stream_length+1):
                if stream[i:j] in self._symbols_codes.keys():
                    encoded_stream += self._symbols_codes[stream[i:j]]
                    break
            
            i=j 

        return encoded_stream 

    def decode(self, stream:str)->str:
        stream_length = len(stream)
        decoded_stream = ""
        decoded_arr = []
        i = 0
        while i<stream_length:
            for j in range(i+1,stream_length+1):
                if stream[i:j] in self._codes_symbols.keys():
                    current_code = self._codes_symbols[stream[i:j]]
                    if current_code == ',':
                        decoded_arr.append(float(decoded_stream))
                        decoded_stream = ""
                    else:
                        decoded_stream += current_code                   
                    break
            i=j 

        return decoded_arr
