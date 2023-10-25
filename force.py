import numpy as np
# Define the gravitational constant (G) in the specified units
G = 1.0  # Solar mass * parsec^3 / year^2
num_particles = 100  # Number of particles
# box_size = 10.0  # Size of the simulation box
softening = 0.1  # Softening length to prevent singularities
# time_step = 0.01  # Time step for the simulation
# num_steps = 100  # Number of simulation steps

# Generate random initial positions and velocities in a single 6-array
# particle_data = np.random.rand(num_particles, 6)
#uniform distribution

# Function to compute gravitational force between two particles
def gforce(particle1, particle2):
    r = particle2["position"] - particle1["position"]  # Position components in parsecs
    distance = np.linalg.norm(r) 
    if distance < softening:
        force_magnitude = G * (particle1["mass"] * particle2["mass"]) / (distance +softening)** 3 #Be careful! If you need the magnitude of force you have to edit this!
    else:
        force_magnitude = G * (particle1["mass"] * particle2["mass"]) / (distance)**3
    force = force_magnitude * r
    return force

# Loop through all pairs of particles
def total_force_on_particle(particle_index, particle_data):
    total_force = np.zeros(3) # Initialize the total force on each particle to zero
    for i in range(len(particle_data)):
        if i != particle_index:
            force = gforce(particle_data[particle_index], particle_data[i])
            total_force += force
    return total_force