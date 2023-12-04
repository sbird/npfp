from bhtree import OctreeNode, Octree
from gen_part import gen_particle_plummer
from time_step import get_mean_ip_dist
import numpy as np
import matplotlib.pyplot as plt
from kdk import kdk
from time_step import get_mean_ip_dist, get_timestep
import matplotlib.animation as animation

N = 100
part_data = gen_particle_plummer(N)
tree = Octree([0,0,0], 100) # Initializing the Octree class 
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
    plt.plot(pos_x, pos_y, 'ko', alpha = alpha)
    plt.xlim(-50, 50)
    plt.ylim(-50, 50)
    plt.tight_layout()
    return None

i = 0

pid_ar = np.array(list(part_data.keys()), dtype = int)
print(pid_ar)

def update(i):
    global pid_ar
    tree = Octree([0,0,0], 100) # Initializing the Octree class 
    tree.insert_particles(part_data, get_mean_ip_dist(part_data)) # Updating the tree
    # print_OctreeNode(tree.root)
    # print(part_data)
    acc_ar = np.zeros(3)
    for (pid, part) in (part_data.items()):
        print(pid)
        acc_this_part = tree.compute_total_force_tree(part)/part['mass'] #this is the len 3 array of accelerations
        part_data[pid]['acc'] = acc_this_part
        print('This part', acc_this_part)
        print('Bigger array', acc_ar)
        acc_ar = np.append(acc_ar, acc_this_part, axis = 1)
        
    acc_ar = np.delete(acc_ar, 0)
    dt = get_timestep(ipd, acc_ar, c=0.0001) #this is the timestep for next iteration
    
    for pid in pid_ar:
        print(np.where(pid_ar == pid))
        part_data[pid] = kdk(part_data[pid], acc_ar[np.where(pid_ar == pid)], dt) #!!! update the index of acc_ar later
        pos = part_data[pid]['position']
        if any(np.abs(pos) > 50): #removing any particles that go outside the box
            part_data.pop(pid)
            pid_ar = np.delete(pid_ar, np.where(pid_ar == pid))
            print(f'the length of pid array {len(pid_ar)}')
        # print(acc_ar[pid])

    plot_xy(part_data, alpha=1)
    if i>100:
        return True

fig, ax = plt.subplots()
ani = animation.FuncAnimation(fig=fig, func=update, frames=4, interval=70)
plt.show()