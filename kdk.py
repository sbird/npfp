## This is a sub-routin to do the Kick-Drift-Kick time integration 
## K(dt/2) = (x_t, v_t) --> (x_t, v_t+1)
## D(dt) = (x_t, v_t) --> (x_t+1, v_t)
import numpy as np


# def kick(particle_data, dt):
#     """
#         Input is a single particle dictionary. expects the keys 'position', 'velocity', and 'mass'.
#         Kicks the particles velocity one step forward. 
#         K(dt/2) = (x_t, v_t) --> (x_t, v_t+1) 
      
#       """
#     # acc = gforce(particle_data["id"])/particle_data["mass"]
#     particle_data["velocity"] += acc*dt
#     return particle_data

def kick(particle_data, acc, dt):
    """
        Input is a single particle dictionary. expects the keys 'position', 'velocity', and 'mass'.
        Kicks the particles velocity one step forward. 
        K(dt/2) = (x_t, v_t) --> (x_t, v_t+1) 
      [PS]: updating it with acc as input to the code
      dt SHOULD BE IN SECONDS
      """
    # print("vel:", particle_data["velocity"])
    # vel_no_update = np.array(particle_data["velocity"])
    # print(f"%change in velocity is {100 * np.round((np.array(acc*dt) * 3.24078e-14 /vel_no_update), decimals= 4)}") 
    particle_data["velocity"] += np.array(acc*dt) * 3.24078e-14 #This is in (km/s)
    return particle_data


def drift(particle_data, dt):
    """
        Input is a single particle dictionary. expects the keys 'position', 'velocity', and 'mass'.
        Drifts the particles position one step forward. 
        K(dt/2) = (x_t, v_t) --> (x_t, v_t+1) 
        dt SHOULD BE IN SECONDS  
    """
    # acc = gforce(particle_data["id"])/particle_data["mass"]
    # print("vel:",particle_data["velocity"]*dt)
    # pos_no_update = np.array(particle_data["position"])
    # vel = particle_data["velocity"]
    # print(f"%change in position is {100 * np.round((np.array(vel * dt *  3.24078e-14)  /pos_no_update), decimals= 4)}")
    particle_data["position"] += particle_data["velocity"] * dt *  3.24078e-14 #This gives out values in kpc
    return particle_data

def kdk(particle_data, acc, dt):
    """
        Input is a single particle dictionary. expects the keys 'position', 'velocity', and 'mass'.
        Drifts and kicks the particles position one step forward. 
        (x_t, v_t) --> (x_t+1, v_t+1)

    """
    particle_data = kick(particle_data, acc, dt/2)
    particle_data = drift(particle_data,dt)
    particle_data = kick(particle_data, acc, dt/2)
    return particle_data
