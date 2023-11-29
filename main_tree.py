from bhtree import OctreeNode, Octree
from gen_part import gen_particle_plummer
from time_step import get_mean_ip_dist

N = 100
part_data = gen_particle_plummer(N)
tree = Octree([0,0,0], 100)
tree.insert_particles(part_data, get_mean_ip_dist(part_data))