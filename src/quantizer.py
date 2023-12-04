import numpy as np

class Quantizer:

    def __init__(self,type='low'):
        self.type =type

        self._Low_compression_table = np.array([[ 1,  1,  1,  1,  1,  2,  2,  4],
        [ 1,  1,  1,  1,  1,  2,  2,  4],
        [ 1,  1,  1,  1,  2,  2,  2,  4],
        [ 1,  1,  1,  1,  2,  2,  4,  8],
        [ 1,  1,  2,  2,  2,  2,  4,  8],
        [ 2,  2,  2,  2,  2,  4,  8,  8],
        [ 2,  2,  2,  4,  4,  8,  8, 16],
        [ 4,  4,  4,  4,  8,  8, 16, 16]])

        self._High_compression_table = np.array([[  1,   2,   4,   8,  16,  32,  64, 128],
        [  2,   4,   4,   8,  16,  32,  64, 128],
        [  4,   4,   8,  16,  32,  64, 128, 128],
        [  8,   8,  16,  32,  64, 128, 128, 256],
        [ 16,  16,  32,  64, 128, 128, 256, 256],
        [ 32,  32,  64, 128, 128, 256, 256, 256],
        [ 64,  64, 128, 128, 256, 256, 256, 256],
        [128, 128, 128, 256, 256, 256, 256, 256]])


    # Each value in the DCT spectrum is divided by the corresponding value in the corresponding compression table, and the result rounded to the nearest integer.
    def _quantization(self,img:np.array,table:np.array):
        quantized_img = np.zeros(img.shape)
        box_dim = 8
        for i in range(0, img.shape[0], box_dim):
            for j in range(0, img.shape[1], box_dim):
                box = img[i:i+box_dim, j:j+box_dim]
                quantized_img[i:i+box_dim, j:j+box_dim] = box / table
        return quantized_img.astype(int)
    
    # Each value in the Decoder spectrum is multiplied by the corresponding value in the Low_compression table, and the result rounded to the nearest integer.
    def _reverse_quantization(self,img:np.array,table:np.array):
        quantized_img = np.zeros(img.shape)
        box_dim = 8
        for i in range(0, img.shape[0], box_dim):
            for j in range(0, img.shape[1], box_dim):
                box = img[i:i+box_dim, j:j+box_dim]
                quantized_img[i:i+box_dim, j:j+box_dim] = box * table
        return quantized_img.astype(int)
    
    # select the box function based on the its type
    def quantization(self,img):
        if self.type == 'low':
            return self._quantization(img,self._Low_compression_table)
        else:
            return self._quantization(img,self._High_compression_table)
            
    def reverse_quantization(self,img):
        if self.type == 'low':
            return self._reverse_quantization(img,self._Low_compression_table)
        else:
            return self._reverse_quantization(img,self._High_compression_table)
    
    
    
    

    

