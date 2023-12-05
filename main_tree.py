from bhtree import OctreeNode, Octree
from gen_part import gen_particle_plummer
from time_step import get_mean_ip_dist
import numpy as np
import matplotlib.pyplot as plt
from kdk import kdk
from time_step import get_mean_ip_dist, get_timestep
import matplotlib.animation as animation
from PIL import Image

N = 100
boxsize = 50
part_data = gen_particle_plummer(N)
# part_data1 = part_data
tree = Octree([0,0,0], boxsize) # Initializing the Octree class
tree.insert_particles(part_data, get_mean_ip_dist(part_data)) # Making a tree with initial particles

# let us try to print the tree now

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

# print_OctreeNode(tree.root)


# Let us evolve the system now

ipd = get_mean_ip_dist(part_data) #This is the mean interparticle distance

def plot_xy(part_data, alpha):
    # plt.figure()
    pos_ar = np.array([part_data[pid]["position"] for pid in part_data.keys()])
    pos_x = pos_ar[:, 0]
    pos_y = pos_ar[:, 1]
    plt.clf()
    plt.plot(pos_x, pos_y, marker = '.', color = 'black', alpha = alpha, lw = 0)
    plt.xlim(-boxsize/2, boxsize/2)
    plt.ylim(-boxsize/2, boxsize/2)
    plt.tight_layout()
    return None

i = 0

def update(i):
    tree = Octree([0,0,0], boxsize) # Initializing the Octree class
    tree.insert_particles(part_data, get_mean_ip_dist(part_data)) # Updating the tree
    # print_OctreeNode(tree.root)
    # print(part_data)
    acc_ar = None
    for (pid, part) in part_data.items():
        acc_this_part = tree.compute_total_force_tree(part)/part['mass'] #this is the len 3 array of accelerations
        part_data[pid]['acc'] = acc_this_part
        acc_this_part = np.reshape(acc_this_part, (1,3))
        if acc_ar is None:
            acc_ar = acc_this_part
        else:
            acc_ar = np.concatenate([acc_ar, acc_this_part])
    # print('Bigger array', np.shape(acc_ar), acc_ar)

    dt = get_timestep(ipd, acc_ar, c=0.1) #this is the timestep for next iteration

    pids = list(part_data.keys())
    for pid in pids:
        part_data[pid] = kdk(part_data[pid], part_data[pid]['acc'], dt) #!!! update the index of acc_ar later
        pos = part_data[pid]['position']
        if any(np.abs(pos) > boxsize/2): #removing any particles that go outside the box
            part_data.pop(pid)
            print(f'the length of pid array {len(part_data.keys())}')
        # print(acc_ar[pid])
    print(len(part_data.keys()))
    plot_xy(part_data, alpha=1)
    # if i>100:
    #     return True

fig, ax = plt.subplots(figsize = (5, 5))
ani = animation.FuncAnimation(fig=fig, func=update, frames=50, interval=35)
ani.save('animation.gif', writer='pillow', fps=2)
# plt.show()
