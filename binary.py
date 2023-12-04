import numpy as np
def spatial(particle1,particle2,mean):
    
    '''
    This function checks for spatial closeness

    Args
    mean: Mean interparticle distance
    particle1, particle2: are particle dictionaries

    '''
    r = np.linalg.norm(particle2["position"] - particle1["position"])  
    return r

    
def grav_bound(particle1,particle2,b):
    '''
    This checks if particles are gravitationally bound
    THIS ASSUMES G IN SI UNITS
    '''
    c = 3e8 #m/s
    G = 1
    m1 = particle1['mass']
    m2 = particle2['mass']
    m = max(m1, m2) #because we want the biggest sch radius (anything inside sch rad won't survive).
    assert np.isclose(G, 1), "Check units of G"


    v1 = particle1['velocity']/m1 
    v2 = particle2['velocity']/m2 
    v = np.linalg.norm(v1 + v2) #what units?
    Rs =  2 * G * m / c**2 #This is in SI units
    if b< np.sqrt((np.pi)*(85*np.pi/3)**(2/7) * (Rs**2)*(v/c)**(-18/7) ):
        return True
    else:
        return False
    

