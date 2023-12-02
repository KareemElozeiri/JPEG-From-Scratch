import numpy as np 
from .DCT import DCT
from .huffman import Huffman
from .quantizer import Quantizer
from .run_length_code import RunLengthCode

class JPEG:
    def __init__(self,img,type='low') -> None:
        self.img = img
        self.quantizer_object = Quantizer()
        self.type = type

    
    def _img2vector_box(self, img:np.array)->np.array:
        rows, cols = img.shape
        vector = np.zeros(rows*cols)
        current_index = 0

        for d in range(rows+cols-1):
            if d%2 == 0:
                d1, d2, limit = d, 0, d+1 
                if d>(rows-1):
                    d1 = rows - 1
                    d2 = d - d1
                    limit = d1-d2+1
            else:
                d1, d2, limit = 0, d, d+1

                if d>rows-1:
                    d2 = rows - 1
                    d1 = d - d2
                    limit = d2-d1 +1


            for i in range(limit):
                vector[current_index] = img[d1, d2]
                current_index += 1
                if d%2 == 0:
                    d1 -= 1
                    d2 += 1
                else:
                    d1 += 1
                    d2 -= 1         
            
        return vector
    
    
    def _vector2img_box(self, vector:np.array, img_shape):
        rows, cols = img_shape
        img = np.zeros(img_shape)
        current_index = 0

        for d in range(rows+cols-1):
            if d%2 == 0:
                d1, d2, limit = d, 0, d+1 
                if d>(rows-1):
                    d1 = rows - 1
                    d2 = d - d1
                    limit = d1-d2+1
            else:
                d1, d2, limit = 0, d, d+1
                if d>rows-1:
                    d2 = rows - 1
                    d1 = d - d2
                    limit = d2-d1 +1

            for i in range(limit):
                img[d1, d2] = vector[current_index]
                current_index += 1
                if d%2 == 0:
                    d1 -= 1
                    d2 += 1
                else:
                    d1 += 1
                    d2 -= 1         
        
        return img
    
    def img2vector(self, img:np.array)->np.array:
        rows, cols = img.shape
        vector = np.array([])
        box_dim = 8
        for i in range(0, rows, box_dim):
            for j in range(0, cols, box_dim):
                img_box = img[i:i+box_dim, j:j+box_dim]
                vector = np.append( vector, self._img2vector_box(img_box))

        return vector
    
    def vector2img(self, vector:np.array, img_shape):
        rows, cols = img_shape
        img = np.zeros(img_shape)
        curr_index = 0
        box_dim = 8
        for i in range(0, rows, box_dim):
            for j in range(0, cols, box_dim):
                vector_slice = vector[curr_index : curr_index + box_dim*box_dim]
                img[i:i+box_dim, j:j+box_dim] = self._vector2img_box(vector_slice,[box_dim,box_dim])
                curr_index += box_dim*box_dim

        return img    
    
    def zero_padding(self, img_gray):
        if (img_gray.shape[0]%8 != 0):
            no_padding_rows = 8-img_gray.shape[0]%8
            padding = np.zeros([no_padding_rows,img_gray.shape[1]])
            img_gray = np.concatenate((img_gray,padding),axis=0)

        if (img_gray.shape[1]%8 != 0):
            no_padding_cols = 8-img_gray.shape[1]%8
            padding = np.zeros([img_gray.shape[0],no_padding_cols])
            img_gray = np.concatenate((img_gray,padding),axis=1)

        return img_gray

    def compress(self, img)->str:
        img_padding = self.zero_padding(img)
        fig_dct = DCT.DCT(img_padding)
        if self.type == 'low':
            img_quantized = self.quantizer_object.Low_compression(fig_dct)
        else:
            img_quantized = self.quantizer_object.High_compression(fig_dct)
        reshaped2vector = self.img2vector(img_quantized).astype(np.int32)
        stream_run_lenght_encoded = RunLengthCode.encode(reshaped2vector)
        self.huffman_object = Huffman(stream_run_lenght_encoded)
        huffman_encoded = self.huffman_object.encode(stream_run_lenght_encoded)
        return huffman_encoded

    def decompress(self, stream)->np.array:
        huffman_decoder = self.huffman_object.decode(stream)
        stream_run_lenght_decoded = RunLengthCode.decode(huffman_decoder)
        reshaped2matrix = self.vector2img(stream_run_lenght_decoded,self.img.shape)
        if self.type == 'low':
            reverse_quantization = self.quantizer_object.reverse_Low_compression(reshaped2matrix)
        else:
            reverse_quantization = self.quantizer_object.reverse_High_compression(reshaped2matrix)
        fig_IDCT = DCT.IDCT(reverse_quantization)
        return fig_IDCT


    
