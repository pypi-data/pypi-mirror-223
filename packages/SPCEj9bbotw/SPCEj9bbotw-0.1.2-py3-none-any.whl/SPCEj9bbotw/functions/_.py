import numpy as np
import scipy.sparse as sp


class transformation:
    def __init__(self):
        return
    
    def extract(block_shape, ext_elem, n):  
        b_r, b_c = block_shape
        block = np.zeros(block_shape)
        tf = (list(range(b_r)), ext_elem)
        block[tf] = 1
        data = np.tile(block, (n,1)).reshape((n,)+block_shape)
        return sparse.block(data, block_shape, n)
    
    def intersect(data):
        #data: (x,y,z...)
        # x = [x0, x1, ...], y = [y0, y1, ...] -> [x0, y0, x1, y1, ...]
        # shape of x, y: (n,)
        temp = np.vstack(data)
        temp = temp.T.reshape(-1,1)
        return temp
    
    def insert(block_shape, ist_elem, n):
        b_r, b_c = block_shape
        block = np.zeros(block_shape)
        tf = (ist_elem, np.arange(b_c))
        block[tf] = 1
        data = np.tile(block, (n,1)).reshape((n,)+block_shape)
        return sparse.block(data, block_shape, n)
    
    def add_zero(shape):
        mtrx = np.zeros(shape)
        mtrx[:shape[1],:shape[1]] = np.eye(shape[1])
        return mtrx
    
    def cross_product(x):
        return np.array([[0, -x[2], x[1]],
                          [x[2], 0, -x[0]], 
                          [-x[1], x[0], 0]])
    
    def band(block, n, itv):
        # x: band matrix with block
        block_shape = np.array(block.shape)
        b_r, b_c = block_shape
        x = np.zeros((n*b_r, n*b_c-(n-1)*itv))
        for i in range(n):
            x[b_r*i:b_r*(i+1), itv*i:itv*i+b_c] = block
        return x

class matrix:
    def __init__(self):
        return
    
    def band(block, n, itv):
        # x: band matrix with block
        block_shape = np.array(block.shape)
        b_r, b_c = block_shape
        x = np.zeros((n*b_r, itv*(n-1)+b_c))
        print(x.shape)
        for i in range(n):
            x[b_r*i:b_r*(i+1), itv*i:itv*i+b_c] = block
        return x
        
    def fill_diag(mtrx, *arr_num):   #copy?
        for i in arr_num:
            arr, num = i    
            if num >= 0:
                limit = mtrx.shape[1]      
                idx_c = np.arange(num, limit)
                idx_r = idx_c - num
                mtrx[(idx_r, idx_c)] = arr
                
            else:
                num = np.abs(num)
                limit = mtrx.shape[0]      
                idx_r = np.arange(num, limit)
                idx_c = idx_r - num
                mtrx[(idx_r, idx_c)] = arr


        
class sparse:
    def __init__(self):
        return
    
    def block(data, blocksize, n):
        indptr = np.arange(n+1)
        indices = np.arange(n)
        return sp.bsr_array((data,indices, indptr), blocksize=blocksize, shape=n*np.array(blocksize)).tocsr()


class INDEX:
    def __init__(self):
        return
    
    def IDXV(tf_n):  #return index arr for vec
        idxv = []
        for tf, n in tf_n:
            idxv += [tf]*n
        return np.array(idxv)
