import numpy as np
# Define the gravitational constant (G) in the specified units
# G = 6.6e-11  # Units: SI
G = 1
num_particles = 100  # Number of particles
softening = 0.01  # Softening length to prevent singularities

# Function to compute gravitational force between two particles
def gforce(particle1, particle2):
    r = particle2["position"] - particle1["position"]  # Position components in parsecs
    distance = np.linalg.norm(r)
    if distance == 0:
        return np.zeros(3)
    if distance < softening:
        force_magnitude = G * (particle1["mass"] * particle2["mass"]) / (softening)** 3 #Be careful! If you need the magnitude of force you have to edit this!
    else:
        force_magnitude = G * (particle1["mass"] * particle2["mass"]) / (distance)**3
    force =  force_magnitude * r
    return force

# Loop through all pairs of particles
def total_force_on_particle(particle_index, particle_data):
    '''
    This function gives the total force on one particle
    '''
    total_force = np.zeros(3) # Initialize the total force on each particle to zero
    for i in range(len(particle_data)):
        if i != particle_index:
            force = gforce(particle_data[particle_index], particle_data[i])
            total_force += force
    return total_force


def acceleration(particle_index, particle_data):
    '''
    This funciton gives the acceleration vector for one particle
    '''
    acc = total_force_on_particle(particle_index, particle_data) / particle_data[particle_index]["mass"]
    return acc
