import numpy as np
import numpy.linalg as lg
import cupy as cp
from _ import *


'''
coefficient matrix of primal variable is calculated by cupy inverse function.
'''
class gpu_optimizer:
    def __init__(self, x_0, n, dt, rho, cond, g, ang_vel, epoch, func_gpu):
        self.x_0 = x_0
        self.n = n
        self.dt = dt
        self.rho = rho
        self.g = g
        self.ang_vel = ang_vel
        self.cond = cond
        self.epoch = np.int32(epoch)
        self.eps_r = 0.001
        self.eps_s = 0.001
        self.func_main_ = func_gpu
        # self.make_mtrx/()
        # self.init_gpu()
        # self.func_GPU()
        
        # self.func_main_ = ker_main_(self.n)///
        
    def next_opt(self, x_0, n, cond):
        self.x_0 = x_0
        self.n = n
        self.cond = cond
        
        
    def scaling(self, scales):
        scl_pos, scl_vel, scl_u, scl_sig, scl_z = scales
        
        self.scale = {}
        self.scale['x'] = np.diag([scl_pos]*3+[scl_vel]*3)
        self.scale['inv/x'] = lg.inv(self.scale['x'])
        self.scale['u'] = np.diag([scl_u]*3)
        self.scale['inv/u'] = lg.inv(self.scale['u'])
        self.scale['sig'] = scl_sig
        self.scale['inv/sig'] = 1/self.scale['sig']
        self.scale['z'] = scl_z
        self.scale['inv/z'] = 1/self.scale['z']
        
        self.A = np.eye(6)
        matrix.fill_diag(self.A, (self.dt, 3))
        self.tA = self.A.T
        self.B = np.zeros((6,3))
        matrix.fill_diag(self.B, (0.5*self.dt**2,0), (self.dt, -3))
        self.tB = self.B.T       
        
        self.A_scl = self.scale['inv/x']@self.A@self.scale['x']
        self.tA_scl = self.A_scl.T
        self.B_scl = self.scale['inv/x']@self.B@self.scale['u']
        self.tB_scl = self.B_scl.T
        self.g_scl = self.scale['inv/x']@self.B@self.g
        self.cond['alpha_scl'] = self.scale['inv/z']*self.cond['alpha']*self.scale['sig']
        
        self.z_lb_scl = self.scale['inv/z']*np.array([np.log(self.cond['m_0'] - self.cond['alpha']*self.cond['rho2']*
                                                             self.dt*i) for i in range(self.n+1)])
        self.z_ub_scl = self.scale['inv/z']*np.array([np.log(self.cond['m_0'] - self.cond['alpha']*self.cond['rho1']*
                                                             self.dt*i) for i in range(self.n+1)])
        
        
    def make_mtrx(self):
        self.TM = {}      
        self.TM['y2u-sig'] = transformation.extract((4,11), [0,1,2,9], self.n)
        block = np.zeros((2, 2*11))
        block[0, 20] = 1
        block[1,10] = 1
        self.TM['y2sig-z'] = transformation.band(block, self.n, 11)
        self.TM['y2sig-z'] = self.TM['y2sig-z'][:, 11:]
         
            
        ##make alpha##        
        block = np.block([[np.zeros((6,3)), self.A_scl, np.zeros((6,2)), self.B_scl, -np.eye(6), np.zeros((6,2))],
                          [np.zeros(10), np.array([1]), np.zeros(9), np.array([-self.cond['alpha_scl']*self.dt, -1])]])
        self.alpha = transformation.band(block, self.n, 11)
        self.alpha = self.alpha[:,11:]
        self.alpha = sp.csr_array(self.alpha)
        self.talpha = self.alpha.T

        ##beta##     
        self.beta = np.tile(np.hstack((-self.g_scl, [0])), self.n)[:, np.newaxis]
        self.beta[:6,:] = self.beta[:6,:] - self.scale['inv/x']@self.A_scl@self.x_0 
        self.beta[6,:] = -self.scale['inv/z']*np.log(self.cond['m_0'])
        
        #################################################################################################
        ##gamma##
        tmp1 = np.zeros((self.n,1,3))
        tmp1[:,:,-1] = 1
        tmp1 = sparse.block(tmp1, (1,3), self.n)

        tmp2 = np.zeros((self.n,1,3))
        tmp2[:,:,-1] = -1
        tmp2 = sparse.block(tmp2, (1,3), self.n)

        tmp3 = np.zeros((self.n,1,3))
        tmp3[:,:,0] = 1
        tmp3 = sparse.block(tmp3, (1,3), self.n)


        self.gamma = sp.vstack([tmp1, tmp2, tmp3])
        self.gamma = sp.csr_array(self.gamma)@transformation.extract((3,11), [0,9,10], self.n)
        self.tgamma = self.gamma.T
        ###############################################################################################

        ## zeta ##
        self.zeta = np.hstack((self.z_lb_scl[1:], -self.z_ub_scl[1:], np.zeros(self.n)))[:,np.newaxis]

        ## C ##
        self.C = sp.csr_array(sp.vstack([self.gamma, self.TM['y2u-sig'], self.TM['y2sig-z']]))
        self.tC = sp.csr_array(self.C.T)

        
        ##b3
        self.b3 = sp.csr_array((2*self.n, 1))
        self.b3[1] = -self.scale['inv/z']*np.log(self.cond['m_0'])
        
        # ||xn||^2 - Zn
        self.coeff_y = self.rho*self.C.T@self.C
        self.coeff_y[-8:-2, -8:-2] = self.coeff_y[-8:-2, -8:-2] + sp.csr_array(sp.diags([1000, 100, 100, 10, 1, 1]))
        a = sp.hstack([self.coeff_y, self.talpha])
        b = sp.hstack([self.alpha, sp.csr_array((7*self.n,7*self.n))])
        self.coeff_y = sp.vstack([a,b])
        self.tilde_C_gpu = cp.array(self.coeff_y.toarray().astype(np.float32))
        self.tilde_C_gpu = cp.linalg.inv(self.tilde_C_gpu)
        

        ##fixed matrix for updating y
        h = sp.csr_array((11*self.n,1))
        h[-1] = -1*10

        q_tilde = sp.vstack([self.zeta, sp.csr_array((4*self.n,1)), self.b3])
        self.y_fix = sp.csr_array(sp.vstack([-h + self.rho*self.tC@q_tilde, self.beta]))
        self.y_fix_gpu = self.tilde_C_gpu[:11*self.n, :]@cp.array(self.y_fix.toarray().astype(np.float32))        
        self.tilde_C_gpu = self.tilde_C_gpu[:11*self.n, :11*self.n]@cp.array((self.rho*self.tC).toarray().astype(np.float32))
        
    def init_gpu(self):
        # self.y_gpu =  cp.array(p.zeros((11,self.n, 1)).astype(np.float32))
        self.acc_cmd_gpu = cp.array(np.zeros(4).astype(np.float32) )
        self.z_lb_gpu = cp.array(self.z_lb_scl.astype(np.float32))
        self.z_ub_gpu = cp.array(self.z_ub_scl.astype(np.float32))
        self.N_gpu = np.int32(self.n)
        self.scale_gpu = cp.array(np.array([self.scale['z'], self.scale['inv/sig']*self.cond['rho1'], 
                                            self.scale['inv/sig']*self.cond['rho2'],
                                            self.scale['inv/sig']*self.scale['u'][0,0]]).astype(np.float32))
        
    def admm_main(self):
        self.func_main_((1, 11, 1), (1, self.n, 1), (self.y_fix_gpu, self.tilde_C_gpu, 
                                                     self.z_lb_gpu, self.z_ub_gpu, self.N_gpu, self.epoch, 
                                                     self.acc_cmd_gpu, self.scale_gpu))



