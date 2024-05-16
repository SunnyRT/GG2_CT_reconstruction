import math
import numpy as np
import numpy.matlib

def ramp_filter_rt(sinogram, scale, alpha=0.001):
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
	# FIXME: I think sample spacing should be scale, which is the distance (in cm) between each pixel of data
	# FIXME: unsure whether needs to sort order of omega_ary. coz documentations gives example output: array([ 0.  ,  1.25,  2.5 , ..., -3.75, -2.5 , -1.25])
	omega_ary = 2*np.pi*np.fft.fftfreq(m, scale) 
	f_ary = np.zeros(m)
	for (i, omega) in enumerate(omega_ary):
		f_ary[i] = np.abs(omega) / (2*math.pi) * (np.cos(omega * math.pi / m))**alpha
	
	# take Fourier transform of sinogram p(theta, r) in r direction (i.e.samples direction)
	FT = np.fft.fft(sinogram, n = m, axis=1) # FIXME: unsure about output length n=m
	FT_filtered = np.multiply(FT, f_ary)
	sinogram = np.fft.ifft(FT_filtered, n=n, axis=1)

	print('Ramp filtering')
	
	return sinogram

# TODO:(attempted by YQ)
def ramp_filter(sinogram, scale, alpha=0.001): # FIXME: Not sure where to use the parameter "scale"
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
	#ramp[0] = (1/6)*ramp[1]
	#ramp = np.array(ramp)

	#f_ary = np.zeros(ramp)
	#for (i, ramp_coefficient) in enumerate(ramp):
	#	f_ary[i] = ramp_coefficient * (np.cos(omega_list[i] * math.pi / (2*omega_max)))**alpha
	cosine_window = (np.cos(omega_list * np.pi / (2 * omega_list.max())))**alpha
	ramp = ramp * cosine_window
	
	# take Fourier transform of sinogram p(theta, r) in r direction (i.e.samples direction)
	FT = np.fft.fft(sinogram, n = m, axis=1) #FIXME: unsure about output length n=m
	FT_filtered = np.multiply(FT, ramp)
	sinogram = np.fft.ifft(FT_filtered, n=m, axis=1)

	print('Ramp filtering')
	
	return sinogram