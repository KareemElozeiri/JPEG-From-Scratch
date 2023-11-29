import numpy as np 
from .DCT import DCT

class JPEG:
    def __init__(self) -> None:
        pass

    @staticmethod
    def img2vector(img:np.array)->np.array:
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
    
    @staticmethod
    def vector2img(vector:np.array, img_shape):
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
    
 
    def compress(self, img)->str:
        pass 

    def decompress(self, stream)->np.array:
        pass 

    
