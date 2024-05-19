import numpy as np
import math

def attenuate(original_energy, coeff, depth):
	"""calculates residual photons for a particular material and depth
	attenuate(original_energy, coeff, depth, mas) takes the original_energy
	(energy, samples) and works out the residual_energy (energy, samples)
	for a particular material with linear attenuation coefficients given
	by coeff (energies), and a set of depths given by depth (samples)

	It is more efficient to calculate this for a range of samples rather then
	one at a time
	"""

	# check original energy is energy x samples
	# TODO: (taz) reshape(1,1) has dimension = 2, eg. original_energy = np.array([1, 2, 3, 4, 5]) sample = 1; eg. original_energy = np.array([1, 2, 3, 4, 5])%([6, 7, 8, 9, 10]) sample =5
	if type(original_energy) != np.ndarray:
		original_energy = np.array([original_energy]).reshape((1, 1))
	elif original_energy.ndim == 1:
		original_energy = original_energy.reshape((len(original_energy), 1))
	elif original_energy.ndim != 2:
		raise ValueError('input original_energy has more than two dimensions')
	energies = original_energy.shape[0]
	samples = original_energy.shape[1]


	# check coeff is vector of energies
	if type(coeff) != np.ndarray:
		coeff = np.array([coeff])
	elif coeff.ndim != 1:
		raise ValueError('input coeffs has more than one dimension')
	if len(coeff) != energies:
		raise ValueError('input coeff has different number of energies to input original_energy')

	# check depth is vector of samples
	
	if type(depth) != np.ndarray:
		depth = np.array([depth])
	elif depth.ndim != 1:
		raise ValueError('input depth has more than one dimension')
	if len(depth) != samples:
		raise ValueError('input depth has different number of samples to input original_energy')

	# # TODO: by RT
	# # Work out residual 
	# # energy for each depth and at each energy
	# residual_energy = np.zeros((energies, samples))
	# for e in range(energies):
	# 	for s in range(samples):
	# 		residual_energy[e][s]=original_energy[e][s] * np.e**(-coeff[e]*depth[s])

	# TODO: update by RT 19/05/2024
	residual_energy = original_energy*np.exp(-np.matmul(coeff.reshape(energies,1),depth.reshape(1,samples)))	

	return residual_energy