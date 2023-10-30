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