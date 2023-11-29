from bhtree import OctreeNode, Octree
from gen_part import gen_particle_plummer
from time_step import get_mean_ip_dist

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

print_OctreeNode(tree.root)


# Let us evolve the system now

ipd = get_mean_ip_dist(part_data) #This is the mean interparticle distance

# def update(i):
#     acc_ar = np.array([acceleration(pid, part_data) for pid in part_data.keys()]) #this is the (N,3) array of accelerations
#     dt = get_timestep(ipd, acc_ar, c=0.07) #this is the timestep for next iteration
#     for pid in part_data.keys():
#         part_data[pid] = kdk(part_data[pid], acc_ar[pid], dt) #!!! update the index of acc_ar later
#     plot_xy(part_data, alpha=1)
#     if i>100:
#         return True