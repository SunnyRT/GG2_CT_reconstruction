import math
import numpy as np
import numpy.matlib

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



	# TODO:(RT)
	# apply filter to all angles
	omega_ary = np.linspace(-m/2, m/2, m+1) #FIXME: what should be sampling frequency???
	f_ary = np.zeros(m)
	for (i, omega) in enumerate(omega_ary):
		f_ary[i] = np.abs(omega) / (2*math.pi) * (np.cos(omega * math.pi / m))**alpha
	
	# take Fourier transform of sinogram p(theta, r) in r direction (i.e.samples direction)
	FT = np.fft.fft(sinogram, n = m, axis=1) #FIXME: unsure about output length n=m
	FT_filtered = np.multiply(FT, f_ary)
	sinogram = np.fft.ifft(FT_filtered, n=n, axis=1)


	print('Ramp filtering')
	
	return sinogram