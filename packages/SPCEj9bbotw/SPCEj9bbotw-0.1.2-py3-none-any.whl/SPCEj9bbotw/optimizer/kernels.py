import cupy as cp

def ker_main_(N, NR_epoch):
    num_thread = int(11*N)
    str_ = r"""
    #define _X (blockDim.x * blockIdx.x + threadIdx.x)
    #define _Y (blockDim.y * blockIdx.y + threadIdx.y)    
    #define _Coor (_X + _Y*gridDim.x*blockDim.x)
    #include <cooperative_groups.h>
    namespace cg = cooperative_groups;
    
    typedef struct {
        int u;
        int x;
        int sig;
        int z;
    } IDXS;
    
    typedef struct {
        float rho1;
        float rho2;
    } COND;
    
    /*typedef struct {
        float theta;
        float sig;
        float u;
        float z;
        float pos ;
        float vel ;
        float socb;
        float exp1;
        float exp2;
    } SCALE;*/

    __device__ float y[""" + repr(num_thread) + r"""] ={0.0} ;

    __device__ float buff_y[""" + repr(num_thread) + r"""] ={0.0} ;

    __device__ float w["""+ repr(num_thread) +r"""]={0.0}  ;

    __device__ float buff_w["""+ repr(num_thread) +r"""]={0.0} ;

    __device__ float buff["""+ repr(num_thread) +r"""]={0.0} ;

    __device__ float ys["""+ repr(num_thread) +r"""] ={0.0};

    __device__ int NR_epoch = """+repr(NR_epoch)+r""";

    __device__ int NR_eps = 0.001;
    
    //__device__ SCALE scale ={0, 10, 1, 1, 100, 10, 0.1, 0.1*0.2*24000, 0.1*0.8*24000};
    

    __device__ float NR_f(float x, float a, float b, float rho, float c){

        return expf(c*x)*(x - a) - powf(rho, 2)*c*expf(-c*x) + rho*(b)*c;
    }

    __device__ float NR_fdot(float x, float a, float b, float rho, float c){

        return expf(c*x)*(c*x - c*a + 1) + powf(rho, 2)*expf(-c*x)*powf(c,2);
    }

    __device__ float func_matmulvec(float* x, float* y, int act_len){

        float result = 0;

        for(int i=0; i < act_len; i++){
            result += x[i]*y[i];
        }

        return result;
    }

    __device__ float func_norm(float* ptr){

        float norm=0;

        for(int i=0; i < 3; i++){
            norm += ptr[i]*ptr[i];
        }

        return sqrt(norm);
    }

    __device__ void proj_lb(float* x, float lb){

        if(*x < lb){
            *x = lb;
        }
    }

    __device__ void Gcone_(float* u, float* sig, float t){

        float norm = func_norm(u);

        if(*sig <= -1/t*norm && *sig < 0){
            *sig = 0;
            for(int i=0; i<3; i++){
                u[i] = 0;
            }
        }
        else if(norm != 0){

            float temp = (norm + (*sig)*t)/(1+powf(t,2));

            for(int i=0; i<3; i++){
                u[i] = (temp/norm)*u[i];
                *sig = temp*t;
            }
        }

    }
    
    
    
    __device__ float NR(float* a, float* b, float rho, float c){

        float x = *a;
        
        for(int i=0; i < NR_epoch; i++){
            x = x - NR_f(x, *a, *b, rho, c)/NR_fdot(x, *a, *b, rho, c);
            if(fabsf(NR_f(x, *a, *b, rho, c)) <= NR_eps){
                return x;
            }
        }

        return x;
    }

    __device__ void itv_exp(float* sig, float* z, float rho1, float rho2, float scl_z){

        if(*sig < rho1*expf(- scl_z*(*z))){
            *z = NR(z, sig, rho1, scl_z);
            *sig = rho1*expf(- scl_z*(*z));

        }
        else if(*sig > rho2*expf(- scl_z*(*z))){
            *z = NR(z, sig, rho2, scl_z);
            *sig = rho2*expf(- scl_z*(*z));

            
        }

    }


    extern "C"
    __global__ void main_(float* y_out, float* y_fix, float* tilde_C, float* z_lb, float* z_ub, int N, 
    int epoch, float* acc_cmd, float* scales){

        int idx = _Coor;
        int len_var = 11*N;
        int len_dual = 9*N;
        int shr_idx = idx % 11;
        int res_idx = idx % N;
        
        //SCALE scale;
        
        float scl_z = scales[0];
        float scl_coeff_exp_lb = scales[1];
        float scl_coeff_exp_ub = scales[2];
        float scl_coeff_cone = scales[3];
        float scl_coeff_poiniting = scales[4];
        
        

        IDXS idxs;
        idxs.u = 11*idx; idxs.x = 11*idx+3; idxs.sig = 11*idx+9; idxs.z = 11*idx+10;

        IDXS res_idxs;
        res_idxs.u = 11*res_idx; res_idxs.x = 11*res_idx+3; res_idxs.sig = 11*res_idx+9; res_idxs.z = 11*res_idx+10;
        
        float* th_proj1;
        float* th_proj2;
        float* th_ys;

        cg::grid_group grid = cg::this_grid();
        
        /*buff[idx] = 0;
        buff_w[idx] = 0;
        ys[idx] = 0;
        w[idx] = 0;*/
        
        sync(grid);

        /*-----------------------------------------------------------------*/
        
        if(idx < 3*N){
            float a = 3;
        }
        else if(3*N <= idx && idx < 4*N){
            th_proj1 = &buff_w[3*N+res_idx*4];   // u
            th_proj2 = &buff_w[3*N+res_idx*4+3]; // sig
            th_ys = &ys[3*N+res_idx*4];
        }
        else if(4*N <= idx && idx < 5*N){ //projection for exponential inequality
            th_proj1 = &buff_w[7*N+res_idx*2];   // sig
            th_proj2 = &buff_w[7*N+res_idx*2+1]; // z
            th_ys = &ys[7*N+res_idx*2];
            
        }

        /*-----------------------------------------------------------------*/
        for(int iter_=0; iter_ < epoch; iter_++){
            if(idx < len_dual){
                buff[idx] = w[idx] - ys[idx];
            }
            sync(grid);
                
            if(idx < 11*N){
                buff_y[idx] = y_fix[idx] + func_matmulvec(&tilde_C[len_dual*idx], buff, len_dual);
                
            }
        
            sync(grid);

            /*-----------------projection--------------------------------------*/

            /*-----------------linear inequality--------------------------------------------*/
            
            if(idx < N){
                buff_w[idx] = buff_y[res_idxs.z] - z_lb[res_idx+1] + ys[idx];
                proj_lb(&buff_w[idx], 0);
                ys[idx] = ys[idx] + buff_y[res_idxs.z] -z_lb[res_idx+1] - buff_w[idx];   
            }
            else if(N <= idx && idx < 2*N){
                buff_w[idx] = - buff_y[res_idxs.z]  + z_ub[res_idx+1] + ys[idx];
                proj_lb(&buff_w[idx], 0);
                ys[idx] = ys[idx]  -buff_y[res_idxs.z] +z_ub[res_idx+1] - buff_w[idx];
            }
            else if(2*N <= idx && idx < 3*N){
                buff_w[idx] = buff_y[res_idxs.u] - scl_coeff_poiniting*buff_y[res_idxs.sig] + ys[idx];
                proj_lb(&buff_w[idx], 0);
                ys[idx] = ys[idx] + buff_y[res_idxs.u] - scl_coeff_poiniting*buff_y[res_idxs.sig] - buff_w[idx];
            }

            /*-----------------socbp----------------------------------*/
            else if(3*N <= idx && idx < 4*N){
                for(int i=0; i < 3; i++){
                    th_proj1[i] = buff_y[res_idxs.u+i] + th_ys[i];
                }
                *th_proj2 = buff_y[res_idxs.sig] + th_ys[3];
                //Gcone_(th_proj1, th_proj2, scale.socb);
                Gcone_(th_proj1, th_proj2, scl_coeff_cone);  //
                
                for(int i=0; i < 3; i++){
                    th_ys[i] = th_ys[i] + buff_y[res_idxs.u+i] - th_proj1[i];
                }
                th_ys[3] = th_ys[3] + buff_y[res_idxs.sig] - *th_proj2;
                

            }
           
            else if(4*N <= idx && idx <5*N){
                if(res_idx == 0){
                    *th_proj1 = buff_y[res_idxs.sig] + th_ys[0];
                    *th_proj2 = z_lb[0] + th_ys[1];
       
                }
                else{
                    *th_proj1 = buff_y[res_idxs.sig] + th_ys[0];
                    *th_proj2 = buff_y[res_idxs.z-11] + th_ys[1];
     
                }
                itv_exp(th_proj1, th_proj2, scl_coeff_exp_lb, scl_coeff_exp_ub, scl_z);    //
                
                
                if(res_idx == 0){
                    th_ys[0] = th_ys[0] + buff_y[res_idxs.sig] - *th_proj1;
                    th_ys[1] = th_ys[1] + z_lb[0] - *th_proj2;
        
                }
                else{
                    th_ys[0] = th_ys[0] + buff_y[res_idxs.sig] - *th_proj1;
                    th_ys[1] = th_ys[1] + buff_y[res_idxs.z-11] - *th_proj2;
                    
                }
                
            }
            sync(grid);
            
            y[idx] = buff_y[idx];
            w[idx] = buff_w[idx];
            sync(grid);  
        }
        //y[idx] = buff_w[idx];
        sync(grid);
        if(idx == 0){
            for(int i=0; i < 3; i++){
                acc_cmd[i] = y[i];
            }
            acc_cmd[3] = y[9];
        }

        sync(grid);
        if(epoch == 0){
            y_out[idx] = y[idx];
            
        }
    }
    """
    SM_main_ = cp.RawKernel(str_, 'main_', enable_cooperative_groups=True)
    return SM_main_
