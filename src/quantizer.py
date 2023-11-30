import numpy as np

class Quantizer:

    def __init__(self):
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


    # Each value in the DCT spectrum is divided by the corresponding value in the Low_compression table, and the result rounded to the nearest integer.
    def Low_compression_box(self, img):
        Quantized = (img / self._Low_compression_table).astype(int)
        return Quantized  
    # Each value in the DCT spectrum is divided by the corresponding value in the High_compression table, and the result rounded to the nearest integer.
    def High_compression_box(self, img):
        Quantized = (img / self._High_compression_table).astype(int)
        return Quantized
    # Each value in the Decoder spectrum is multiplied by the corresponding value in the Low_compression table, and the result rounded to the nearest integer.
    def reverse_Low_compression_box(self, img:np.array):
        Quantized = (img * self._Low_compression_table).astype(int)
        return Quantized   
    # Each value in the Decoder spectrum is multiplied by the corresponding value in the High_compression table, and the result rounded to the nearest integer.
    def reverse_High_compression_box(self, img):
        Quantized = (img * self._High_compression_table).astype(int)
        return Quantized

    def Low_compression(self,img):
        y = np.zeros(img.shape)
        for i in range(0, img.shape[0], 8):
            for j in range(0, img.shape[1], 8):
                X_slice = img[i:i+8, j:j+8]
                y[i:i+8, j:j+8] = self.Low_compression_box(X_slice)
        return y
    
    def High_compression(self,img):
        y = np.zeros(img.shape)
        for i in range(0, img.shape[0], 8):
            for j in range(0, img.shape[1], 8):
                X_slice = img[i:i+8, j:j+8]
                y[i:i+8, j:j+8] = self.High_compression_box(X_slice)
        return y

    def reverse_Low_compression(self,img):
        y = np.zeros(img.shape)
        for i in range(0, img.shape[0], 8):
            for j in range(0, img.shape[1], 8):
                X_slice = img[i:i+8, j:j+8]
                y[i:i+8, j:j+8] = self.reverse_Low_compression_box(X_slice)
        return y

    def reverse_High_compression(self,img):
        y = np.zeros(img.shape)
        for i in range(0, img.shape[0], 8):
            for j in range(0, img.shape[1], 8):
                X_slice = img[i:i+8, j:j+8]
                y[i:i+8, j:j+8] = self.reverse_High_compression_box(X_slice)
        return y
    

