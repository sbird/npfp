"""A test case for the force calculation"""
import numpy as np
from force import *

def test_force_simple():
    """Test the force accuracy."""
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
    assert np.allclose(total_force, expected_force, rtol=1e-6), "Test failed: Total force calculation is incorrect."
