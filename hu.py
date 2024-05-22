import numpy as np
from attenuate import *
from ct_calibrate import *
from ct_detect import *

def hu(p, material, reconstruction, scale):
	""" convert CT reconstruction output to Hounsfield Units
	calibrated = hu(p, material, reconstruction, scale) converts the reconstruction into Hounsfield
	Units, using the material coefficients, photon energy p and scale given."""

	
	# TODO: (by YQ)
	#print("Reconstuction shape", reconstruction.shape)
	n = reconstruction.shape[1] # number of r offset values i.e. number of dectors per angle
	depth = 2*n*scale # Total distance between source and detectors = double phantom size

	# use water to calibrate
	water_coeff = material.coeff('Water')

	I_tot = ct_detect(p, water_coeff, depth)
	# put this through the same calibration process as the normal CT data
	total_attenuation_water = ct_calibrate(p, material, np.array(I_tot, ndmin=2), scale)
	reconstruction_water = total_attenuation_water/depth
	print(reconstruction_water)

	# use result to convert to hounsfield units
	# limit minimum to -1024, which is normal for CT data.
	HU = 1000*(reconstruction - reconstruction_water)/reconstruction_water

	# For medical CT, Hounsfield Units are usually stored as integers between the 12-bit range of -1024 and 3072
	# with any values outside this range set to the nearest limit
	stored_HU = np.clip(HU, -1024.0, 3072.0).astype('int')


	return stored_HU
