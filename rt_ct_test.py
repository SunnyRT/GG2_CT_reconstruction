# TODO:(RT)


# these are the imports you are likely to need
import numpy as np
from material import *
from source import *
from fake_source import *
from ct_phantom import *
from ct_lib import *
from scan_and_reconstruct import *
from create_dicom import *

# create object instances
material = Material()
source = Source()

# define each end-to-end test here, including comments
# these are just some examples to get you started
# all the output should be saved in a 'results' directory

def test_1():
	"""Compare the scanned and reconstructed image with the original phantom 3 of single large hip replacement
	using a higher energy source packet"""

	# work out what the initial conditions should be
	p = ct_phantom(material.name, 256, 3)
	s = source.photon('100kVp, 3mm Al')
	y = scan_and_reconstruct(s, material, p, 0.01, 256)
	s_ideal = source.fake_source(source.mev, 0.1, method='ideal')
	y_ideal = scan_and_reconstruct(s_ideal, material, p, 0.01, 256)

	# save some meaningful results
	save_draw(p, 'results', 'test_1_phantom')
	save_draw(y, 'results', 'test_1_image')
	save_draw(y_ideal, 'results', 'test_1_image_ideal')

	# how to check whether these results are actually correct?
	# check that the 2 drawings of reconstructed scan image and direct phantom image are identical
	

def test_impulse_alpha():
	"""Investigate impulse response of ramp_filter function at different values of alpha"""

	# initial conditions: single point attenuator at origin
	p = ct_phantom(material.name, 256, 2)
	s = fake_source(source.mev, 0.1, method='ideal')
	sinogram_nofilter = scan_and_reconstruct(s, material, p, 0.01, 256, reconstruct=False, with_filter=False)
	

	alphas = np.array([0,0.0001,0.01,0.1,1])
	peak_mu = np.empty(len(alphas)+1)
	peak_mu[0] = back_project(sinogram_nofilter[128,:]) # No filter
	for (i,alpha) in enumerate(alphas):
		sinogram = ramp_filter(sinogram_nofilter, 0.01, alpha)
		reconstruction = back_project(sinogram)
		peak_mu[i+1] = np.max(reconstruction[128,:])

	# save some meaningful results
	f = open('ramp_filter_alpha.txt', mode='w')
	f.write('Peak value of non-filtered image is ' + str(np.max(peak_mu[0])) + '\n')
	f.write('Peak value of filtered image with alpha = ' + str(alphas) + ' is ' + str(peak_mu[1:]))
	f.close()

	# plot out peak reconstructed result with different alpha values
	plt.plot(alphas, peak_mu[1:], label='Ramp filter with alpha')
	plt.hlines(peak_mu[0], 0, 1, label='No filter')
	plt.xscale('log')

	# how to check whether these results are actually correct?
	return peak_mu


def test_3_rt():
	"""Output the mean value of the scanned and reconstructed image of a simple disc with different materials 
	using an ideal source packet"""

	# work out what the initial conditions should be
	
	s = fake_source(source.mev, 0.1, method='ideal')
	mat_test = ["Soft Tissue", "Water", "Titanium"]
	results = np.empty(len(mat_test))
	for (i,mat_name) in enumerate(mat_test):
		p =  ct_phantom(material.name, 256, 1, metal = mat_name)
		y = scan_and_reconstruct(s, material, p, 0.1, 256)
		results[i] = np.mean(y[64:192, 64:192])
		print("measured attenuation coefficient for ", mat_name, " is ", results[i])
	
	f = open('results/test_3_output.txt', mode='a')
	f.write(f'Detected mean attenuation coefficient for {mat_test} are {results}\n')
	# assume ideal fake_source peak at 0.07MeV
	f.write(f'Expected mean attenuation coefficient for {mat_test} are [0.204, 0.194, 2.472]\n') # assume ideal fake_source peak at 0.07MeV
	f.close()
	


	# how to check whether these results are actually correct?


# # Run the various tests
# print('Test 1')
# test_1()
# print('Test 2')
# test_2()
# print('Test 3')
# test_3()
