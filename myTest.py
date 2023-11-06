import numpy as np

def generate_random_velocities(N, sigma):
    u = np.random.uniform(0, 1, size=N)
    v = np.random.uniform(0, 1, size=N)
    
    theta = 2 * np.pi * u
    phi = np.arccos(2 * v - 1)
    
    x = np.sin(phi) * np.cos(theta)
    y = np.sin(phi) * np.sin(theta)
    z = np.cos(phi)
    
    r = (x**2 + y**2 + z**2)**0.5
    
    scale_factor = np.sqrt(-2 * sigma**2 * np.log(1 - u))
    vx = scale_factor * x / r
    vy = scale_factor * y / r
    vz = scale_factor * z / r
    
    return np.column_stack((vx, vy, vz))

# Example usage
N = 100  # Number of particles
sigma = 1.0  # Velocity dispersion

velocities = generate_random_velocities(N, sigma)
print(velocities)
