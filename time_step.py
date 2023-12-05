import numpy as np


def get_mean_ip_dist(part_data):
	'''
	This funciton is to obtain the mean interparticle distance between the particles
	'''
	pos_ar = np.array([part_data[pid]["position"] for pid in part_data.keys()])
	# print(pos_ar)
	#Extract positions of the particles
	pos_x = pos_ar[:, 0]
	pos_y = pos_ar[:, 1]
	pos_z = pos_ar[:, 2]
	dist_sum = 0 #This is the variable for sum of all distances
	for i in range(len(pos_x)):
		'''
		This loop is to go through all the particles and get the interparticle distance
		'''
		dist_sum = dist_sum + np.sum(np.sqrt((pos_x[i + 1:] - pos_x[i])**2 + (pos_y[i + 1:] - pos_y[i])**2 + (pos_z[i + 1:] - pos_z[i]) ** 2)) #This line calculates the particle distance of all the particles after i from ith particle
	num_part = len(pos_x)
	num_pairs = num_part * ( num_part - 1 ) / 2
	return dist_sum/num_pairs #this is the mean distance

# ipart_dist = get_mean_ip_dist(part_data) #This line needs to go into main

def get_timestep(ipd, acc,c=1):
    """
    Args:
    acc: this has to be all particles
    c: This is a constant that we need to vary to check convergence

    Returns:
    The timestep for next iteration of KDK
    """
    acc_mag = np.linalg.norm(acc, axis = 1)
    assert np.shape(acc_mag) != 3
    # print(acc_mag)
    # acc = 1#Decide on how to input acceleration
    dt = c * np.sqrt(np.mean(ipd) / max(acc_mag))  # This is the relation for timestep
    return dt * 10**3 #return timestep for the next iteration of kdk in seconds


def check_convergence():
	'''
    We need to calculate the largest possible c value for which there is convergence.
	-o- The goal is to check the final configuration given the same initial configuration
	-o- What all are we going to check in the final configuration?
    Args:
	
	'''

	return


# 	return None
