import cupy as cp
import numpy as np
import numpy.linalg as lg
import matplotlib.pyplot as plt


def plot(database):
    y = cp.asnumpy(database.y_gpu)
    
    u = database.scale['u']@(y.reshape(-1,11)[:,:3]).T
    
    x = database.scale['x']@(y.reshape((-1, 11))[:,3:9]).T
    x = np.hstack((database.x_0, x))
    
    sigma = database.scale['sig']*y.reshape(-1,11)[:,-2]
    z = database.scale['z']*y.reshape(-1,11)[:,-1]
    z = z.reshape(-1)
    z = np.hstack(([np.log(database.cond['m_0'])],z))
    
    norm_u = lg.norm(u, axis=0)
    mass = np.exp(z[:-1])
    throttle = norm_u*mass
    theta = np.rad2deg(np.arccos(u[0,:]/norm_u))
    

    fig, axes = plt.subplots(3,3, figsize=(16,16))
    axes[0,0].plot(theta, label=r'$\theta$')
    axes[0,0].plot([np.rad2deg(database.cond['theta'])]*database.n, 
                   label=str(np.rad2deg(database.cond['theta']))+u'\N{DEGREE SIGN}')
    axes[0,0].legend()

    axes[0,1].plot([database.cond['rho1']]*database.n)
    axes[0,1].plot([database.cond['rho2']]*database.n)
    axes[0,1].plot(throttle, label='throttle')
    axes[0,1].legend()

    axes[0,2].plot(x[1,:], x[2,:])
    axes[0,2].plot(0, 0, '*')
    axes[0,2].set_xlabel('Y(m)')
    axes[0,2].set_ylabel('Z(m)')
    axes[0,2].set_title('Surface Tragectory')

    ax = axes[1,0]
    axes[1,0].plot(database.scale['z']*database.z_lb_scl, label='lb')
    axes[1,0].plot(database.scale['z']*database.z_ub_scl, label='ub')
    axes[1,0].plot(z, label='z')
    ax.set_ylim([np.min(z) - 1, np.max(z) + 1])
    axes[1,0].legend()

    ax = axes[1,1]
    axes[1,1].plot(sigma, label='sigma', alpha=0.1,  linewidth='10')
    axes[1,1].plot(norm_u, label='||u||')
    ax.set_ylim([np.min(sigma) - 1, np.max(sigma) + 1])
    axes[1,1].legend()

    axes[1,2].plot(database.cond['rho1']*np.exp(-z[:-1]), label='lb')
    axes[1,2].plot(database.cond['rho2']*np.exp(-z[:-1]), label='ub')
    axes[1,2].plot(sigma, label='sigma')
    axes[1,2].legend()

    ax = axes[2,0]
    axes[2,0].plot(np.cos(database.cond['theta'])*sigma, label=r'$\cos90^{\degree}\sigma$')
    axes[2,0].plot(u[0,:], label=r'$u_{0}$')
    axes[2,0].legend()

    axes[2,1].plot(np.hstack((z[0], z[:-1]-database.cond['alpha']*database.dt*sigma)), linewidth='10', alpha=0.1, label='dynamic')
    axes[2,1].plot(z, label='opt_z')
    axes[2,1].legend()
    axes[2,1].set_title(r'$\sigma - z \ dynamics$')
    axes[2,1].set_ylim([np.min(z) - 1, np.max(z) + 1])

    dynamic_x = database.A@x[:,:-1]+database.B@(np.array(database.g)[:,np.newaxis]+u)
    dynamic_x = np.hstack((database.x_0, dynamic_x))
    axes[2,2].plot(x[1,:], label='px')
    axes[2,2].plot(dynamic_x[1, :], linewidth='10', alpha=0.1, label='dynamic')
    axes[2,2].legend()
    axes[2,2].set_title(r'$x \ dynamics$')


    print('required fuel', np.exp(z[0]) - np.exp(z[-1]))
    plt.show()


def traj_3D(database):
    y = cp.asnumpy(database.y_gpu)
    x = database.scale['x']@(y.reshape((-1, 11))[:,3:9]).T
    
    plt.rcParams['lines.linewidth'] = 0.7
    fig = plt.figure()

    ax = plt.axes(projection='3d')
    ax.xaxis._axinfo["grid"].update({"linewidth":0.5})
    ax.yaxis._axinfo["grid"].update({"linewidth":0.5})
    ax.zaxis._axinfo["grid"].update({"linewidth":0.5})

    ax.grid(alpha=0.1, linestyle='--') 
    ax.w_xaxis.pane.fill = False
    ax.w_yaxis.pane.fill = False
    ax.w_zaxis.pane.fill = False

    idx_guidance_out = database.n - 10

    ax.plot(x[2,:], x[1,:], x[0,:], color='black')
    ax.plot(x[2,:idx_guidance_out], x[1,:idx_guidance_out], x[0,:idx_guidance_out], color='black', alpha=0.3, linewidth='5')
    ax.plot(x[2,idx_guidance_out-1], x[1,idx_guidance_out-1], x[0,idx_guidance_out-1], 'x', color='black',  label='guidance out(-10 step)')
    
    
    ax.plot(x[2,-1], x[1,-1], x[0,-1], 'o', color='lightgray')

    ax.plot(x[2,-0], x[1,0], x[0,0], 'o', color='skyblue')
    ax.legend()
    plt.show()