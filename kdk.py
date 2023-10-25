## This is a sub-routin to do the Kick-Drift-Kick time integration 
## K(dt/2) = (x_t, v_t) --> (x_t, v_t+1)
## D(dt) = (x_t, v_t) --> (x_t+1, v_t)
import numpy as np

def kick(particle_data, dt):
    """
        Input is a single particle dictionary. expects the keys 'position', 'velocity', and 'mass'.
        Kicks the particles velocity one step forward. 
        K(dt/2) = (x_t, v_t) --> (x_t, v_t+1) 
      
      """
    acc = gforce(particle_data["id"])/particle_data["mass"]
    particle_data["velocity"] += acc*dt
    return particle_data


def drift(paticle_data, dt):
    """
        Input is a single particle dictionary. expects the keys 'position', 'velocity', and 'mass'.
        Drifts the particles position one step forward. 
        K(dt/2) = (x_t, v_t) --> (x_t, v_t+1) 
      
        """
    acc = gforce(particle_data["id"])/particle_data[]
    particle_data["position"] += particle_data["position"]*dt
    return particle_data

def kdk(particle_data, dt):
    """
        Input is a single particle dictionary. expects the keys 'position', 'velocity', and 'mass'.
        Drifts and kicks the particles position one step forward. 
        (x_t, v_t) --> (x_t+1, v_t+1)

    """
    particle_data = kick(particle_data, dt/2)
    particle_data = drift(particle_data, dt)
    particle_data = kick(particle_data, dt/2)

    return particle_data
