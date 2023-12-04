import numpy as np 
from sys import getsizeof
from .DCT import DCT
from .huffman import Huffman
from .quantizer import Quantizer
from .run_length_code import RunLengthCode

class JPEG:
    def __init__(self,type='low') -> None:
        self.quantizer_object = Quantizer(type)     # make an object of Quantizer class and set the type of quantization table
                                                    # the default is low compression
        self.no_padding_rows = 1                    # Initializing the no_padding_rows
        self.no_padding_cols = 1                    # Initializing the no_padding_cols

    # private funtion converts the given block to a vector in a zigzag way 
    def _img2vector_box(self, img:np.array)->np.array:
        # Inputs: 8by8 block np.array
        # Output: 8*8 np.vector after convertion
        
        rows, cols = img.shape                  # dims of the given img
        vector = np.zeros(rows*cols)            # Initializing the output vector
        current_index = 0                       # the index of the vector

        # looping over the sum of index of the rows and cols 
        for d in range(rows+cols-1):
            # when the sum is even, move from the row to the colum         
            if d%2 == 0:
                d1, d2, limit = d, 0, d+1       # set the first  index (d1) = the sum
                                                # set the second index (d2) = 0
                if d>(rows-1):
                    d1 = rows - 1               # decrement (d1)
                    d2 = d - d1                 # increment (d2)
                    limit = d1-d2+1
            # when the sum is odd, opposite the above process
            else:
                d1, d2, limit = 0, d, d+1       # set the second  index (d2) = the sum
                                                # set the first   index (d1) = 0

                if d>rows-1:
                    d2 = rows - 1               # decrement (d2)
                    d1 = d - d2                 # increment (d1)
                    limit = d2-d1 +1

            for i in range(limit):
                vector[current_index] = img[d1, d2]
                current_index += 1
                # when the sum is even, the direction of setting the elements will be to up
                if d%2 == 0:
                    d1 -= 1
                    d2 += 1
                # when the sum is odd, the direction of setting the elements will be to down
                else:
                    d1 += 1
                    d2 -= 1         
            
        return vector
    
    # private funtion converts the given vector to a matrix in a zigzag way
    def _vector2img_box(self, vector:np.array, img_shape):
        # Input: 8*8 np.vector after convertion, the dims of the output image
        # Output: 8by8 block np.array
        
        rows, cols = img_shape              # dims of the output img
        img = np.zeros(img_shape)           # Initializing the output matrix
        current_index = 0                   # the index of the vector

        # looping over the sum of index of the rows and cols of the output matrix
        # doing the same flow as _img2vector_box, but the difference in the allocating the elements in the matrix
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
    # public funtion takes the image and divide it into 8by8 blocks which is passed to the _img2vector_box fn
    def img2vector(self, img:np.array)->np.array:
        # Input: image as 2D np array
        # Output: vector as 1D np arrey

        rows, cols = img.shape      # dims of the given img
        vector = np.array([])       # Initializing the output vector
        box_dim = 8                 # the dim of the vector box

        # looping over the each 8by8 block in the image
        for i in range(0, rows, box_dim):
            for j in range(0, cols, box_dim):
                # slice 8by8 box
                img_box = img[i:i+box_dim, j:j+box_dim]
                # apply _img2vector_box fn at the box, then append to the output vector
                vector = np.append( vector, self._img2vector_box(img_box))

        return vector
    # public funtion takes the vector and divide it into 8*8 blocks which is passed to the _vector2img_box fn
    def vector2img(self, vector:np.array, img_shape):
        # Input: vector as 1D np arrey 
        # Output: image as 2D np array

        rows, cols = img_shape          # dims of the given img
        img = np.zeros(img_shape)       # Initializing the output matrix
        curr_index = 0                  # the index of the vector
        box_dim = 8                     # the dim of the vector box

        # looping over the each 8by8 block in the image
        for i in range(0, rows, box_dim):
            for j in range(0, cols, box_dim):
                # slice 8*8 box
                vector_slice = vector[curr_index : curr_index + box_dim*box_dim]
                # apply _vector2img_box fn at the box, then set to the output matirx
                img[i:i+box_dim, j:j+box_dim] = self._vector2img_box(vector_slice,[box_dim,box_dim])
                # increment the vector index to tkae the second box
                curr_index += box_dim*box_dim

        return img    
    
    # funtion takes the image and extends it with zeros to make its dim dividalbe by the block dim (8)
    def zero_padding(self, img_gray):
        # check if the number of rows is not dividable by 8
        if (img_gray.shape[0]%8 != 0):
            self.no_padding_rows = 8-img_gray.shape[0]%8                     # number of rows required for padding
            padding = np.zeros([self.no_padding_rows,img_gray.shape[1]])     # create a zeros matrix wtih the required dims for padding
            img_gray = np.concatenate((img_gray,padding),axis=0)        # concatenate the image with padding at the 0 axis
        # check if the number of cols is not dividable by 8
        if (img_gray.shape[1]%8 != 0):
            self.no_padding_cols = 8-img_gray.shape[1]%8                     # number of cols required for padding
            padding = np.zeros([img_gray.shape[0],self.no_padding_cols])     # create a zeros matrix wtih the required dims for padding
            img_gray = np.concatenate((img_gray,padding),axis=1)        # concatenate the image with padding at the 1 axis

        return img_gray
    
    def remove_zero_padding(self,img):
        return img[0:-1*self.no_padding_rows,0:-1*self.no_padding_cols]

    # function takes the image and does the whole compression functions on it
    def compress(self, img:np.array)->str:
        #Input: The image as 2D np.array
        #Output: Binary code of the compressed image as string 

        fig_dct = DCT.DCT(img)                          # apply DCT on the image after padding
        # lossy compression (quantization)
        img_quantized = self.quantizer_object.quantization(fig_dct)
        # convert the image to vector and apply run length code
        reshaped2vector = self.img2vector(img_quantized).astype(np.int32)
        stream_run_lenght_encoded = RunLengthCode.encode(reshaped2vector)
        # lossless compression (Huffman encoder)
        self.huffman_object = Huffman(stream_run_lenght_encoded)
        huffman_encoded = self.huffman_object.encode(stream_run_lenght_encoded)

        return huffman_encoded
    
    # A funtion takes the huffman code and image to calculate the compression ratio
    def compression_ratio(self, code:str, img)->float:
        #Input: The image and Huffman code
        #Output: compression ratio %
        return (len(code)/getsizeof(img)*100)

    # function takes the stream code and does the whole decompression functions on it
    def decompress(self, stream,img_shape)->np.array:
        # lossless decompression (Huffman decoder)
        huffman_decoder = self.huffman_object.decode(stream)
        # run length decoder and convert the vector to image
        stream_run_lenght_decoded = RunLengthCode.decode(huffman_decoder)
        reshaped2matrix = self.vector2img(stream_run_lenght_decoded,img_shape)
        # lossy decompression (reverse quantization)
        reverse_quantization = self.quantizer_object.reverse_quantization(reshaped2matrix)
        # apply IDCT on the image
        fig_IDCT = DCT.IDCT(reverse_quantization)

        return fig_IDCT


    
