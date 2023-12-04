"""Simple Octtree class. An Octtree sub-divides space recursively into 8 subsections, splitting each axis in half. The tree stops splitting when there are a maximum of 8 particles in a cell. It is thus deeper in denser areas."""

import numpy as np
from force import gforce
from binary import *

class OctreeNode:
    """This is a single node of the OctTree. These nodes will have child nodes."""
    def __init__(self, center, size):
        self.center = center  # Center of the current node
        self.size = size      # Length of this node's sides
        self.mass = 0         # Total mass in this node
        self.com = np.zeros(3)  # Center of mass
        self.children = []  # Child nodes
        self.is_leaf = True
        self.particles = []  # Particles contained in this node (if it's a leaf)

    def insert_particle(self, particle, mean):
        """Add a particle to the tree. Subdivide current node if necessary."""
        #Need to keep moments up to date!
        
        self.update_mass_and_com(particle)
        #Add the particle if a non-full leaf node
        if self.is_leaf and len(self.particles) < 8:
            # self.check_merg(particle, mean)
            self.particles.append(particle)
            return
        # If it's not a leaf node, or full,
        # subdivide and then insert the particle to the right child node.
        if self.is_leaf:
            self.make_children()
            #Need to re-attach all children.
            for p in self.particles:
                child = self.find_child_node(p["position"])
                # self.check_merg(particle, mean)
                self.children[child].insert_particle(p, mean)
            self.particles = []
            self.is_leaf = False
        child = self.find_child_node(particle["position"])
        self.children[child].insert_particle(particle, mean)
        
    def check_merg(self, particle, mean):
        # Calculate distances between the new particle and each existing particle in the node
        if len(self.particles)<1:
            return
        distances =	[spatial(particle, particle2, mean) for particle2 in self.particles]
        # Sort the distances 
        distances_sorted_args = np.argsort(distances)
        # Iterate through the particles in order of increasing distance
        for particle2 in np.array(self.particles)[distances_sorted_args]:
            # Check if the particles are gravitationally bound using the grav_bound function
            if  grav_bound(particle, particle2, spatial(particle, particle, mean))  is True:
                 # If certain distance conditions are met, merge the particles
                if distances[distances_sorted_args[0]]<mean/100 and distances[distances_sorted_args[1]]>2*distances[distances_sorted_args[0]]:
                    # Merge the particles by updating mass, position, and velocity
                    self.particles[distances_sorted_args[0]]['mass'] += particle["mass"]
                    self.particles[distances_sorted_args[0]]['position'] = (particle["position"]* particle["mass"]+  self.particles[distances_sorted_args[0]]['position'] * self.particles[distances_sorted_args[0]]['mass']) /( particle["mass"]+ self.particles[distances_sorted_args[0]]['mass'])
                    self.particles[distances_sorted_args[0]]['velocity'] = (particle["velocity"]* particle["mass"]+  self.particles[distances_sorted_args[0]]['velocity'] * self.particles[distances_sorted_args[0]]['mass']) /( particle["mass"]+ self.particles[distances_sorted_args[0]]['mass'])
                    # Return True to indicate a merge occurred
                    return True
                else:
                    return False

    			
    
    def particle_in_node(self, particle_pos):
        """Check whether a particle is inside the volume covered by a node,
        by checking whether each dimension is close enough to center (L1 metric)."""
        inside = 1
        for i in range(3):
            inside *= (abs(particle_pos[i] - self.center[i]) <= self.size/2)
        return inside

    def find_child_node(self, particle_pos):
        """Find the index of the child within which the party belongs. There is a faster way to do this!"""
        for i, c in enumerate(self.children):
            if c.particle_in_node(particle_pos):
                return i
        raise ValueError("Particle is not in tree!")

    def make_children(self):
        """Create 8 child nodes in this node's children list."""
        for index in range(8):
            #The bitshifting tricks are why binary trees are more convenient!
            #The idea is that each index can shift a different axis by 1/2 a step.
            offset = [(-0.5 + ((index >> i) % 2))  * self.size / 2 for i in range(3)]
            new_center = np.array(self.center) + np.array(offset)
            self.children.append(OctreeNode(new_center, self.size/2))

    def update_mass_and_com(self, particle):
        """Update the center of mass and total mass of this node"""
        new_com = (self.com * self.mass + particle['position'] * particle['mass']) / (self.mass + particle['mass'])
        self.com = new_com
        self.mass += particle['mass']
    

    def compute_total_force_tree(self, part, theta0):
        """Find the total force from all particles in this section of the tree, recursively."""
        theta = self.size/ np.linalg.norm(self.com - part["position"])
        #No need to open the node! We are done.
        if theta < theta0:
            nodedata = {"position" : self.com, "mass": self.mass}
            return np.array(gforce(part, nodedata))
        #If we are a leaf node, need to do forces for all particles
        if self.is_leaf:
            force_leaf = np.zeros(3)
            for p in self.particles:
                force_leaf += np.array(gforce(part, p))
            return force_leaf
            # return np.sum(np.array([np.array(gforce(part, p)) for p in self.particles]), axis = 0)
        #Otherwise recursively compute the force for the children
        return np.sum([c.compute_total_force_tree(part, theta0) for c in self.children], axis = 0)

class Octree:
    """Build the octree! Note that the boundary_center and boundary_size needs to include all particles in the space."""
    def __init__(self, boundary_center, boundary_size):
        self.root = OctreeNode(boundary_center, boundary_size)
        #Opening angle
        self.theta0 = 0.3

    def insert_particles(self, all_particles, mean):
        """Add all particles to the tree and compute moments."""
        for pp in all_particles.values():
            self.root.insert_particle(pp, mean)
            # print(self.root.particles, "\n")


    def compute_total_force_tree(self, part):
        """Compute the total force on a particle."""
        return self.root.compute_total_force_tree(part, self.theta0)
