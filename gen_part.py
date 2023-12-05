import numpy as np

def generate_particle_info(N):
    '''to generate values for position and velocity of particles
    from a Gaussian distribution'''
    pos = np.random.randn(N, 3)
    vel = np.random.randn(N, 3)
    # masses = np.ones(N)

    ids = np.arange(0, N) 

    particle_data = {} # outer dictionary
    '''defining a general dictionary to have all particle info in one'''

    for i, particle_id in enumerate(ids): #ids for each of the particles
        position = pos[i]
        velocity = vel[i]

        particle_info = {
            "id": particle_id,
            "position": position,
            "velocity": np.zeros(3), #FIXME! Make this not zero!
            "mass": 1
        } # generates a small dict for each particle

        particle_data[particle_id] = particle_info # adds the particle info dict to the particle data dict. Using id as keys
    print(particle_data)
    
def gen_particle_plummer(N):
    '''This function generates particle positions and velocities based on Plummer model: https://articles.adsabs.harvard.edu/pdf/1974A%26A....37..183A'''
    X1 = np.random.uniform(size=N)
    r = np.power(np.power(X1, -2/3)-1, -0.5) #calculates the radial distance based on plummer model. eq no. A2 of the paper.
    
    X2 = np.random.uniform(size=N) # generate more random numbers needed in plummer model for spherical coordinates calculations.
    X3 = np.random.uniform(size=N)
    z = (1-2*X2)*r #calculates cartesian coordinates based on plummer 
    x = np.power(r**2 - z**2, 1/2) * np.cos(2*np.pi*X3)
    y = (r**2 - z**2)**(0.5) * np.sin(2*np.pi*X3)

    velocities = [] #velocity generation
    i = 0
    while len(velocities)<N:

        X4 = np.random.uniform()
        X5 = np.random.uniform()
        if 0.1*X5 < (X4**2 * (1 - X4**2))**(7/2):    
            X6 = np.random.uniform()
            X7 = np.random.uniform()
            V = X4 * 2**(1/2) * (1 + r[i]**2)**(-1/4)
            w = (1-2*X6) * V #based on eq A6 of the paper.
            u = (V**2 - w**2)**(1/2) * np.cos(2 * np.pi * X7)
            v = (V**2 - w**2)**(1/2) * np.sin(2 * np.pi * X7)
            velocities.append([u, v, w])
            i +=1 
    velocities = np.array(velocities)
    
    ids = np.arange(N)

    particle_data = {}
    '''defining a general dictionary to have all particle info in one'''

    for i, particle_id in enumerate(ids):

        particle_info = {
            "id": particle_id,
            "position": np.array([x[i], y[i], z[i]]),
            "velocity": velocities[i]/1e2,
            "mass": 1
        }

        particle_data[particle_id] = particle_info
    # print(particle_data)
    return particle_data


