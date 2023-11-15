"""Simple Octtree class. An Octtree sub-divides space recursively into 8 subsections, splitting each axis in half. The tree stops splitting when there are a maximum of 8 particles in a cell. It is thus deeper in denser areas."""

import numpy as np
from force import gforce

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

    def insert_particle(self, particle):
        """Add a particle to the tree. Subdivide current node if necessary."""
        #Need to keep moments up to date!
        self.update_mass_and_com(particle)
        #Add the particle if a non-full leaf node
        if self.is_leaf and len(self.particles) < 8:
            self.particles.append(particle)
            return
        # If it's not a leaf node, or full,
        # subdivide and then insert the particle to the right child node.
        if self.is_leaf:
            self.make_children()
            #Need to re-attach all children.
            for p in self.particles:
                child = self.find_child_node(p["position"])
                self.children[child].insert_particle(p)
            self.particles = []
            self.is_leaf = False
        child = self.find_child_node(particle["position"])
        self.children[child].insert_particle(particle)

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
            #FIXME We do not understand how this works! It gives us an error of unsupported operator (& for float and int) when run separately. 
            new_center = self.center + ((-0.5 + (index >> i) & 1) * self.size / 4 for i in range(3))
            self.children.append(OctreeNode(new_center, self.size/2))

    def update_mass_and_com(self, particle):
        """Update the center of mass and total mass of this node"""
        new_com = (self.com * self.mass + particle['position'] * particle['mass']) / (self.mass + particle['mass'])
        self.com = new_com
        self.mass += particle['mass']

    def compute_total_force_tree(self, part, theta0):
        """Find the total force from all particles in this section of the tree, recursively."""
        theta = self.size/ np.sqrt(np.sum(self.com - part["position"])**2)
        #No need to open the node! We are done.
        if theta < theta0:
            nodedata = {"position" : self.com, "mass": self.mass}
            return gforce(part, nodedata)
        #If we are a leaf node, need to do forces for all particles
        if self.is_leaf:
            return np.sum([gforce(part, p) for p in self.particles])
        #Otherwise recursively compute the force for the children
        return np.sum([c.compute_total_force_tree(part, theta0) for c in self.children])

class Octree:
    """Build the octree! Note that the boundary_center and boundary_size needs to include all particles in the space."""
    def __init__(self, boundary_center, boundary_size):
        self.root = OctreeNode(boundary_center, boundary_size)
        #Opening angle
        self.theta0 = 0.3

    def insert_particles(self, all_particles):
        """Add all particles to the tree and compute moments."""
        for pp in all_particles:
            self.root.insert_particle(pp)

    def compute_total_force_tree(self, part):
        """Compute the total force on a particle."""
        return self.root.compute_total_force_tree(part, self.theta0)
