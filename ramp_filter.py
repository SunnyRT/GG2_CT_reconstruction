import math
import numpy as np
import numpy.matlib


# TODO:(attempted by YQ)
def ramp_filter(sinogram, scale, alpha=0.001): 
	""" Ram-Lak filter with raised-cosine for CT reconstruction

	fs = ramp_filter(sinogram, scale) filters the input in sinogram (angles x samples)
	using a Ram-Lak filter.

	fs = ramp_filter(sinogram, scale, alpha) can be used to modify the Ram-Lak filter by a
	cosine raised to the power given by alpha."""

	# get input dimensions
	angles = sinogram.shape[0]
	n = sinogram.shape[1]

	#Set up filter to be at least twice as long as input
	m = np.ceil(np.log(2*n-1) / np.log(2))
	m = int(2 ** m)

	freqs = np.fft.fftfreq(m, scale)
	# the np.fft.fftfreq(m) function calculates the frequency bins that correspond to the FFT of an array of length m
	# These bins represent the frequencies that each FFT coefficient corresponds to.
	omega_list = freqs*2*np.pi
	omega_max = max(omega_list)
	ramp = np.abs(omega_list)/(2*np.pi)

	# Approximate correction: replacing the zero at k = 0 with 1/6 of the value at k=1
	ramp[0] = (1/6)*ramp[1]
	ramp = np.array(ramp)

	# Ram-Lak filter with raised-cosine window	
	raised_cosine = np.cos(omega_list * np.pi / (2 * omega_max))
	raised_cosine = np.maximum(raised_cosine, 0)  # Ensure no negative values
	raised_cosine[raised_cosine == 0] = 1  # Avoid zero values to prevent invalid power operations
	raised_cosine = raised_cosine ** alpha
	ramp = ramp * raised_cosine
	
	# take Fourier transform of sinogram p(theta, r) in r direction (i.e.samples direction)
	FT = np.fft.fft(sinogram, n = m, axis=1) 
	FT_filtered = FT * ramp
	sinogram = np.fft.irfft(FT_filtered, n=m, axis=1)[:,:n]


	print('Ramp filtering')
	
	return sinogram