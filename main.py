import numpy as np
import matplotlib.pyplot as plt
from gen_part import generate_particle_info 
from force import acceleration
from kdk import kdk
from time_step import get_mean_ip_dist, get_timestep

tmax = 13.8 #Gyr

N = 5
part_data = generate_particle_info(N) #This is a dictionary of initial nested dictionary with each particle that can be accesses by id
# print(part_data.keys())

ipd = get_mean_ip_dist(part_data) #This is the mean interparticle distance
# print(ipd)


def plot_xy(part_data):
    return None


i = 1

#this loop is for timesteps
while i == 1:
    # acc_all_part = np.zeros((N, 3)) #This is (N, 3) array of all particles' accelerations
    # acc_dict = {}
    acc_ar = np.array([acceleration(pid, part_data) for pid in part_data.keys()]) #this is the (N,3) array of accelerations
    dt = get_timestep(ipd, acc_ar) #this is the timestep for next iteration
    for pid in part_data.keys():
        part_data[pid] = kdk(part_data[pid], acc_ar[pid], dt) #!!! update the index of acc_ar later  
    print(part_data)
    i = 0

