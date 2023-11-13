import numpy as np 
from .DCT import DCT

class JPEG:
    def __init__(self) -> None:
        pass

    @staticmethod
    def img2vector(img:np.array)->np.array:
        rows, cols = img.shape
        vector = np.zeros(rows*cols)
        curr_index = 0
        
        for d in range(rows+cols-1):
            d1 = d%rows + d//rows
            d2 = d-d1
            diff = np.abs(d1-d2)

            if d%2 != 0 & d1>=d2:
                 d1, d2 = d2, d1

            for i in range(0,diff+1):
                if d1>=d2:
                    vector[curr_index] = img[d1-i][d2+i]
                else:
                    vector[curr_index] = img[d1+i][d2-i]

                curr_index += 1
            
      
        
        return vector

    
