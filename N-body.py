import numpy as np


def generate_particle_info(N):
    '''to generate values for position and velocity of particels
    form gaussian distribution'''
    pos = np.random.randn(N, 3)
    vel = np.random.randn(N, 3)

    ids = np.arange(N)

    for i, particle_id in enumerate(ids):
        position = pos[i]
        velocity = vel[i]

        particle_info = {
            "id": particle_id,
            "Position": position,
            "momentum": velocity
        }
        # put the prticle info into a general dictionary
        particle_data = {particle_id: particle_info}

        print(particle_data)
        #print("---")
