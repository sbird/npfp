## This is a sub-routin to do the Kick-Drift-Kick time integration 
## K(dt/2) = (x_t, v_t) --> (x_t, v_t+1)
## D(dt) = (x_t, v_t) --> (x_t+1, v_t)
import numpy as np

def kick(paticle_data, dt):
    """ inp"""
    acc = gforce(particle_data)/particle_data[7]
    particle_data[3:6] += acc*dt
    return particle_data


def drift(paticle_data, dt):
    """ inp"""
    acc = gforce(particle_data)/particle_data[7]
    particle_data[0:3] += particle_data[3:6]*dt
    return particle_data

def kdk(particle_data, dt):
    particle_data = kick(particle_data, dt/2)
    particle_data = drift(particle_data, dt)
    particle_data = kick(particle_data, dt/2)

    return particle_data
