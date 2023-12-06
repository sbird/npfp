from bhtree import OctreeNode, Octree
from gen_part import gen_particle_plummer
from time_step import get_mean_ip_dist
import numpy as np
import matplotlib.pyplot as plt
from kdk import kdk
from time_step import get_mean_ip_dist, get_timestep
import matplotlib.animation as animation
from PIL import Image


def print_OctreeNode(node, depth = 0):
    '''
    This prints all the the children and particles of a given node
    looks bad for large N
    '''
    if node.is_leaf: #if it is a leaf node
        print('\t'*depth + f'OctreeNode at {node.center} and size {node.size} has {len(node.particles)} particles')
    else:
        print('\t'*depth + f'OctreeNode at {node.center} and size {node.size} has {len(node.children)} children')
        for i, c in enumerate(node.children):
            print_OctreeNode(c, depth = depth + 1)
    return None

def plot_xy(part_data, center, alpha):
    '''
    This function is for plotting the x and y positions

    Args:
    center(pc): This is the com of the system at this time

    Returns None
    '''
    global t
    pos_ar = np.array([part_data[pid]["position"] for pid in part_data.keys()]) #in pc
    pos_x = pos_ar[:, 0] - center[0]
    pos_y = pos_ar[:, 1] - center[1]
    pos_z = pos_ar[:, 2] - center[2]
    plt.clf()
    if len(pos_x == 2):
        plt.plot(pos_x[0], pos_y[0], marker = '.', color = 'pink', alpha = alpha, lw = 0, ms = 5)
        plt.plot(pos_x[1], pos_y[1], marker = '.', color = 'lightblue', alpha = alpha, lw = 0, ms = 5)
        acc1 = part_data[0]['acc']
        vel1 = part_data[0]['velocity']
        plt.text(0.05, 1, f'a_pink = {np.round(acc1*1e3, 3)}', ha = 'left', va = 'top', color = 'white', transform=ax.transAxes)
        plt.text(0.05, 0.95, f'v_pink = {np.round(vel1*1e3, 3)}', ha = 'left', va = 'top', color = 'white', transform=ax.transAxes)
    else:
        plt.plot(pos_x, pos_y, marker = '.', color = 'white', alpha = alpha, lw = 0, ms = 1)
    # plt.plot(pos_x, pos_z, marker = '.', color = 'black', alpha = alpha, lw = 0)
    lim = min(1.25 * max(np.append(np.abs(pos_x), np.abs(pos_y))), 100 )
    plt.xlim(-lim, lim)
    plt.ylim(-lim, lim)
    plt.xlabel('x (pc)')
    plt.ylabel('y (pc)')
    plt.title(f't = {round(t, 2)} Gyrs') #printing the time
    plt.tight_layout()
    # plt.show()
    return None



def update(i):
    '''
    This function needs to be passed to the animation
    '''
    tree = Octree([0,0,0], boxsize) # Initializing the Octree class
    tree.insert_particles(part_data, get_mean_ip_dist(part_data)) # Updating the tree
    acc_ar = None
    for (pid, part) in part_data.items():
        acc_this_part = tree.compute_total_force_tree(part)/part['mass'] #this is the len 3 array of accelerations
        part_data[pid]['acc'] = acc_this_part
        acc_this_part = np.reshape(acc_this_part, (1,3))
        if acc_ar is None:
            acc_ar = acc_this_part
        else:
            acc_ar = np.concatenate([acc_ar, acc_this_part])
    global t
    dt = get_timestep(ipd, acc_ar, c=1e-2) #this is the timestep for next iteration
    # print(f'Change in time is {dt* 3.17098e-8 * 1e-9} Gyrs')
    # print(f'Change in time is {dt} seconds')
    t = t + dt * 3.17098e-8 * 1e-9 #this would be the updated time
    pids = list(part_data.keys())
    center = tree.root.com #This is the center of all the particles that we have
    # print(center)
    for pid in pids:
        part_data[pid] = kdk(part_data[pid], part_data[pid]['acc'], dt) #!!! update the index of acc_ar later
        pos = np.array(part_data[pid]['position'])
        if any(np.abs(pos - np.array(center)) > boxsize/2): #removing any particles that go outside the box
            part_data.pop(pid)
    # print(part_data)
    plot_xy(part_data, center, alpha=1)

    progress = (i+1) / frames
    print(f"\rProgress: [{'#' * int(progress * 20):20s}] {progress * 100:.2f}%", end='', flush=True)
    if i>100:
        return True



N = int(100) #This is the number of particles
boxsize = 1e3 #This is the boxsize in pc
part_data = gen_particle_plummer(N) #This line generates the particles

# print(part_data)
# vel_arr = np.array([part_data[pid]["velocity"] for pid in part_data.keys()])
# vel_mag = np.linalg.norm(vel_arr, axis = 1)
# print(f'Velocity has a median of {np.median(vel_mag)}, 5% = {np.percentile(vel_mag, 5)} and 95% = {np.percentile(vel_mag, 95)}')

tree = Octree([0,0,0], boxsize) # Initializing the Octree class
tree.insert_particles(part_data, get_mean_ip_dist(part_data)) # Making a tree with initial particles


# breakpoint() 
# Let us evolve the system now

ipd = get_mean_ip_dist(part_data) #This is the mean interparticle distance in pc


i = 0
t = 0
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize = (5, 5))
frames = 500
ani = animation.FuncAnimation(fig=fig, func=update, frames=frames, interval=10)
ani.save('animation.gif', writer='pillow', fps=10)

print('')

