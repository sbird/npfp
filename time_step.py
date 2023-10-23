import numpy as np 

def get_timestep(part_data, c = 1):
	'''
	Args:
	c: This is a constant that we need to vary to check convergene

	Returns:
	The timestep for next iteration of KDK
	'''
	acc = gforce(part_data) #This has to be checked again
	pos_x = part_data[:, 0]
	pos_y = part_data[:, 1]
	pos_z = part_data[:, 2]
	pos_mean = np.sum(np.sqrt(pos_x ** 2 + pos_y ** 2 + pos_z ** 2))/len(pos_x) #This is to calculate the mean distance of the particles
	dt = c*np.sqrt(np.mean(pos_mean)/min(acc)) #This is the relation for timestep
	return 



# def check_convergence():


# 	return None