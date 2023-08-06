import numpy as np
import scipy.sparse as sp


'''
- make sparse type array based row, col indexing
- return scipy sparse csr_matrix
'''

class Jsparse:
    
    def diag(shape, data, N):
        row = np.arange(N)
        col = np.arange(N)
        data = np.array(data*N)
        return sp.csr_matrix((data, (row, col)), shape=shape)


    def diags(diagonals, offsets, ashape):
        row = []
        col = []

        for idx, i in enumerate(diagonals):
            if offsets[idx] >= 0:
                col.append(np.arange(offsets[idx], offsets[idx] + len(i)))
                row.append(np.arange(0, len(i)))
            else:
                col.append(np.arange(0, len(i)))
                row.append(np.arange(np.abs(offsets[idx]), np.abs(offsets[idx]) + len(i)))
            

        row = np.hstack(row)
        col = np.hstack(col)

        data = np.hstack(diagonals)

        return sp.csr_matrix((data, (row, col)), shape=ashape)
        
        
    def band(shape, block, N):
        t_r, t_c = shape
        row = np.repeat(np.arange(t_r), 2)
        col = np.repeat(np.arange(t_c), 2)[1:-1]
        block = np.array(block*N)
        return sp.csr_matrix((block, (row, col)), shape=shape)


    def extract(ext_seq, ashape, N):
        # ashape = (4*n, 11*n)
        # ext_seq = [(0, 3*n), (9*n, 10*n)]
        row = np.arange(ashape[0])
        col = []
        for i in ext_seq:
            col.append(np.arange(*i))
        col = np.hstack(col)
        data = np.tile([1], 4*N)

        return sp.csr_matrix((data, (row, col)), shape=ashape)


    '''
    function for diagonal matrix
    diagonal elements consist of 0 or non-zero numbers
    '''
    def diag_part(st_idx, idx, shape, data, repeat=0) :
        if repeat != 0:
            row_col = np.where(np.tile(idx, repeat))[0] + st_idx
            data = np.tile(data, repeat)
        return sp.csr_matrix((data, (row_col, row_col)), shape=shape)
