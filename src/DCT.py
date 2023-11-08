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

        y[0,0] = y[0,0]/64
        y[0, 1:] = y[0, 1:]/32
        y[1:, 0] = y[1:, 0]/32
        y[1:, 1:] = y[1:, 1:]/16

        return y

