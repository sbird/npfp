import numpy as np

def generate_particle_info(N):
    '''to generate values for position and velocity of particles
    from a Gaussian distribution'''
    pos = np.random.randn(N, 3)
    vel = np.random.randn(N, 3)
    # masses = np.ones(N)

    ids = np.arange(N)

    particle_data = {}
    '''defining a general dictionary to have all particle info in one'''

    for i, particle_id in enumerate(ids):
        position = pos[i]
        velocity = vel[i]

        particle_info = {
            "id": particle_id,
            "position": position,
            "momentum": np.zeros(3), #FIXME! Make this not zero!
            "mass": 1
        }

        particle_data[particle_id] = particle_info

    return particle_data


def gen_particle_plummer(N):
    X1 = np.random.uniform(size=N)
    r = np.power(np.power(X1, -2/3)-1, -0.5)
    
    X2 = np.random.uniform(size=N)
    X3 = np.random.uniform(size=N)
    z = (1-2*X2)*r
    x = np.power(r**2 - z**2, 1/2) * np.cos(2*np.pi*X3)
    y = (r**2 - z**2)**(0.5) * np.sin(2*np.pi*X3)

    velocities = np.array([])
    i = 0
    while len(velocities)<N:

        X4 = np.random.uniform()
        X5 = np.random.uniform()
        if 0.1*X5 < (X4**2 * (1 - X4**2))**(7/2):    
            X6 = np.random.uniform()
            X7 = np.random.uniform()
            V = X4 * 2**(1/2) * (1 + r[i]**2)**(-1/4)
            w = (1-2*X6) * V
            u = (V**2 - w**2)**(1/2) * np.cos(2 * np.pi * X7)
            v = (V**2 - w**2)**(1/2) * np.sin(2 * np.pi * X7)
            velocities = np.append(velocities, np.array([u, v, w]))
            i +=1 
    
    print(velocities)


gen_particle_plummer(3)