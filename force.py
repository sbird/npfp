import numpy as np
# Define the gravitational constant (G) in the specified units
G = 1.0  # Solar mass * parsec^3 / year^2
num_particles = 100  # Number of particles
box_size = 10.0  # Size of the simulation box
softening = 0.1  # Softening length to prevent singularities
time_step = 0.01  # Time step for the simulation
num_steps = 100  # Number of simulation steps

# Generate random initial positions and velocities in a single 6-array
particle_data = np.random.rand(num_particles, 6)
# The first three elements (0-2) represent positions
# The last three elements (3-5) represent momenta (velocities)

# Function to compute gravitational force between two particles
def gforce(particle1, particle2):
    r = particle2[:3] - particle1[:3]  # Position components in parsecs
    distance = np.linalg.norm(r)
    if distance < softening:
        return np.zeros(3)  # Avoid singularities
    force_magnitude = G * (particle1[6] * particle2[6]) / (distance**2 + softening**2)
    force = force_magnitude * r
    return force