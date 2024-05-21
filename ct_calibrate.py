import numpy as np
import scipy
from scipy import interpolate
from ct_detect import ct_detect


# # TODO: (RT)
# # from ct_detect import ct_detect
# def ct_calibrate(photons, material, sinogram, scale):

# 	""" ct_calibrate convert CT detections to linearised attenuation
# 	sinogram = ct_calibrate(photons, material, sinogram, scale) takes the CT detection sinogram
# 	in x (angles x samples) and returns a linear attenuation sinogram
# 	(angles x samples). photons is the source energy distribution, material is the
# 	material structure containing names, linear attenuation coefficients and
# 	energies in mev, and scale is the size of each pixel in x, in cm."""

# 	# Get dimensions and work out detection for just air of twice the side
# 	# length (has to be the same as in ct_scan.py)
# 	n = sinogram.shape[1] # number of r offset values i.e. number of detectors per angle
# 	depth = np.array([2*n*scale]) # Total distance between source and detectors = double phantom size
# 	angles = sinogram.shape[0]

# 	scan_air = np.zeros((angles, n))
# 	for angle in range(sinogram.shape[0]):
# 		# FIXME: how to know the argument value of mas????
# 		scan_air[angle] = ct_detect(photons, material.coeff('Air'), depth)

# 	# perform calibration based on eqn(4) in the handout
# 	sinogram = -np.log(sinogram / scan_air)
# 	return sinogram


# TODO: (RT) updated 19/05/2024
from attenuate import attenuate

def ct_calibrate(photons, material, sinogram, scale, harden_w = False):

	""" ct_calibrate convert CT detections to linearised attenuation
	sinogram = ct_calibrate(photons, material, sinogram, scale) takes the CT detection sinogram
	in x (angles x samples) and returns a linear attenuation sinogram
	(angles x samples). photons is the source energy distribution, material is the
	material structure containing names, linear attenuation coefficients and
	energies in mev, and scale is the size of each pixel in x, in cm."""


	# Get dimensions and work out detection for just air of twice the side
	# length (has to be the same as in ct_scan.py)
	n = sinogram.shape[1]
	depth = 2*n*scale
	scan_air = sum(attenuate(photons, material.coeff('Air'), depth)) # scalar calibration value: sum over all energy bins

	# perform calibration based on eqn(4) in the handout
	sinogram = -np.log(sinogram / scan_air)


	if harden_w:
		"""Apply water hardening correction to sinogram"""
		t_w = np.arange(0, 100.1, 0.1) # thickness of water in cm

		# FIXME: should the source be photons, or ideal version with same peak energy?
		p_w = ct_detect(photons, material.coeff('Water'), t_w) # attenuation of water for each thickness
		p_w = -np.log(p_w / scan_air) # convert number of photons to attenuation

		# Fit a function f to map p_w to t_w
		f = interpolate.interp1d(p_w, t_w)

		# Determine equivalent water thickness for each measured sinogram value p_m
		t_wm = f(sinogram)
		C = 0.194 # C is a chosen constant so that p ~= p_m at some arbitrary low thickness of material
		sinogram = t_wm * C

	return sinogram
