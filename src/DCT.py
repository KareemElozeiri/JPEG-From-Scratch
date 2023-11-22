import numpy as np 

class DCT:

    @staticmethod
    def get_base(u:int, v:int, base_dim=8) -> np.array:
        index_vect = np.arange(0, base_dim)
        r_vect = np.cos((2*index_vect+1)*u*np.pi/16)
        c_vect = np.cos((2*index_vect+1)*v*np.pi/16)
        basis = np.outer(r_vect, c_vect)

        return basis

    @staticmethod
    def get_basis(base_dim=8) -> np.array:
        basis = np.zeros((base_dim, base_dim, base_dim, base_dim))

        for u in range(base_dim):
            for v in range(base_dim):
                basis[u][v] = DCT.get_base(u, v, base_dim)

        return basis 
    
    @staticmethod
    def DCT(X:np.array, base_dim=8) -> np.array:
        y = np.zeros(X.shape)
        basis = DCT.get_basis(base_dim)

        for i in range(0, X.shape[0], base_dim):
            for j in range(0, X.shape[1], base_dim):
                X_slice = X[i:i+base_dim, j:j+base_dim]
                y[i:i+base_dim, j:j+base_dim] = np.sum(basis*X_slice, axis=(2,3))

                if i==0 and j==0:
                    y[i:i+base_dim, j:j+base_dim] /= 64
                elif i==0 or j==0:
                    y[i:i+base_dim, j:j+base_dim] /= 32
                else:
                    y[i:i+base_dim, j:j+base_dim] /= 16
                

  
        return y

    @staticmethod
    def IDCT(X:np.array, base_dim=8) -> np.array:
        y = np.zeros(X.shape)
        basis = DCT.get_basis(base_dim)

        for i in range(0, X.shape[0], base_dim):
            for j in range(0, X.shape[1], base_dim):
                X_slice = X[i:i + base_dim, j:j + base_dim]
                y[i:i + base_dim, j:j + base_dim] = np.sum(basis * X_slice[:, :, np.newaxis, np.newaxis], axis=(0, 1))

        return y