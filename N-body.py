import numpy as np

N = 100

pos = np.random.randn(N, 3)
vel = np.random.randn(N, 3)

ids = np.arange(N)

for i, particle_id in enumerate(ids):
    position = pos[i]
    velocity = vel[i]

    print(f"Particle ID: {particle_id}")
    print(f"Position: {position}")
    print(f"Velocity: {velocity}")
    print("---")