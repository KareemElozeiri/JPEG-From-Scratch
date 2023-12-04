import numpy as np

class RunLengthCode:

    '''
        compresses number of zeros by reprenting sequence of adjancent zeros by 0,n where n is their number
    '''
    
    @staticmethod
    def encode(vector: np.array)->np.array:
        out_vect = np.array([])

        i = 0
        while i<len(vector):
            out_vect =np.append(out_vect,vector[i])
            i += 1
            if vector[i-1]==0:
                count = 1
                #starting a loop to counts 0s
                while i<len(vector) and vector[i]==0:
                    count += 1
                    i+= 1

                out_vect = np.append(out_vect,count)

        return out_vect.astype(np.int32).astype(str)


    @staticmethod
    def decode(vector: np.array)->np.array:
        out_vect = np.array([])

        i = 0
        while i<len(vector):
            if vector[i] != 0:
                out_vect = np.append(out_vect, vector[i])
                i += 1
            else:
                #adding sequence of zeros with length equal to the encoded length which lies in the next position to the 0 position index
                out_vect = np.append(out_vect, np.zeros(int(vector[i+1])))
                i +=2


        return out_vect

