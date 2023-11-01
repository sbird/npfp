""" Some simple test routines for kdk.py """

from functions.kdk import *
import numpy as np

def test_sanity_kdk():


    single_particle = {

        "position" : np.zeros(3),
        "momentum" : np.zeros(3),

    }

    kick(single_particle, 1, 1/2)
    drift(single_particle, 1)
    kick(single_particle, 1, 1/2)
    print(single_particle)


    
test_sanity_kdk()