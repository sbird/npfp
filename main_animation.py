import numpy as np
import matplotlib.pyplot as plt
from gen_part import generate_particle_info 
from force import acceleration
from kdk import kdk
from time_step import get_mean_ip_dist, get_timestep
import matplotlib.animation as animation

tmax = 13.8 #Gyr
steps = 50
N = 3

part_data = generate_particle_info(N) #This is a dictionary of initial nested dictionary with each particle that can be accesses by id
# print(part_data.keys())
for pid in part_data.keys():
    part_data[pid]['momentum'] = np.zeros(3)

ipd = get_mean_ip_dist(part_data) #This is the mean interparticle distance
# print(ipd)


def plot_xy(part_data, alpha):
    # plt.figure()
    pos_ar = np.array([part_data[pid]["position"] for pid in part_data.keys()])
    pos_x = pos_ar[:, 0]
    pos_y = pos_ar[:, 1]
    plt.plot(pos_x, pos_y, 'ko', alpha = alpha)
    return None

i = 0

def update(i):
    acc_ar = np.array([acceleration(pid, part_data) for pid in part_data.keys()]) #this is the (N,3) array of accelerations
    dt = get_timestep(ipd, acc_ar, c=0.07) #this is the timestep for next iteration
    for pid in part_data.keys():
        part_data[pid] = kdk(part_data[pid], acc_ar[pid], dt) #!!! update the index of acc_ar later  
    plot_xy(part_data, alpha=1)
    if i>100:
        return True

fig, ax = plt.subplots()
ani = animation.FuncAnimation(fig=fig, func=update, frames=4, interval=70)
    # acc_all_part = np.zeros((N, 3)) #This is (N, 3) array of all particles' accelerations
    # acc_dict = {}
    
    # plot_xy(part_data, alpha = 1-i/steps)
    # i += 1
    # print("Time:", i)
    # print(part_data[pid]["position"])
    # print(part_data[pid]["position"][0]+ part_data[pid]["momentum"][0]*dt + 0.5*acceleration(pid, part_data)[0]*(dt**2))
    # if i >= steps:
    #     break

plt.show()
