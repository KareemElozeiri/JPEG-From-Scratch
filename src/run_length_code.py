import numpy as np

class RunLengthCode:
    
    @staticmethod
    def encode(vector: np.array)->np.array:
        out_vect = ""

        i = 0
        while i<len(vector):
            out_vect += str(vector[i]) + ","
            i += 1
            if vector[i-1]==0:
                count = 1
                
                while i<len(vector) and vector[i]==0:
                    count += 1
                    i+= 1

                out_vect += str(count) + ","

        return out_vect


    @staticmethod
    def decode(vector: np.array)->np.array:
        out_vect = np.array([])

        i = 0
        while i<len(vector):
            if vector[i] != 0:
                out_vect = np.append(out_vect, vector[i])
                i += 1
            else:
                out_vect = np.append(out_vect, np.zeros(int(vector[i+1])))
                i +=2


        return out_vect

