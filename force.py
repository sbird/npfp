import numpy as np
# Define the gravitational constant (G) in the specified units
G = 1.0  # Solar mass * parsec^3 / year^2
num_particles = 100  # Number of particles
softening = 0.1  # Softening length to prevent singularities

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

# Test data (sample particle data)
particle_data = [
    {"position": np.array([0.0, 0.0, 0.0]), "mass": 1.0},
    {"position": np.array([1.0, 0.0, 0.0]), "mass": 2.0},
    {"position": np.array([0.0, 1.0, 0.0]), "mass": 3.0},
]

# Test the total force calculation for a specific particle
total_force = total_force_on_particle(0, particle_data)

# Expected total force for the first particle
expected_force = np.array([2, 3, 0])

# Check if the calculated total force matches the expected force
if np.allclose(total_force, expected_force, rtol=1e-6):
    print("Test passed: Total force calculation is correct.")
else:
    print("Test failed: Total force calculation is incorrect.")