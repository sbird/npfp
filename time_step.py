import numpy as np 

def get_timestep(part_data):
	'''
	Args:
	c: This is a constant that we need to vary to check convergene

	Returns:
	The timestep for next iteration of KDK
	'''
	pos_x = part_data[:, 0]
	pos_y = part_data[:, 1]
	pos_z = part_data[:, 2]
	dt = c*np.sqrt(np.mean(x)/)
	return 



# def check_convergence():


# 	return None