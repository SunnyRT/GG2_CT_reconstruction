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
	y_ideal = 

	# save some meaningful results
	save_draw(y, 'results', 'test_1_image')
	save_draw(p, 'results', 'test_1_phantom')

	# how to check whether these results are actually correct?
	# check that the 2 drawings of reconstructed scan image and direct phantom image are identical
	

def test_2():
	"""Compare 1-line plot the scanned and reconstructed image with the original phantom 2 of a point attenuator located at origin
	using a lower energy source packet"""

	# work out what the initial conditions should be
	p = ct_phantom(material.name, 256, 2)
	s = source.photon('80kVp, 1mm Al')
	y = scan_and_reconstruct(s, material, p, 0.01, 256)

    # FIXME: what are the units of the output????
	# save some meaningful results
	save_plot(y[128,:], p[128,:], 'results', 'test_2_plot', labels = ['reconstucted image', 'phantom'])
	# save some meaningful results
	save_draw(y, 'results', 'test_2_image')
	save_draw(p, 'results', 'test_2_phantom')

	# how to check whether these results are actually correct?

def test_3():
	"""Output the mean value of the scanned and reconstructed image of a simple circle with varying radius (phantom 1) 
	using an ideal source packet"""

	# work out what the initial conditions should be
	p = ct_phantom(material.name, 256, 1)
	s = fake_source(source.mev, 0.1, method='ideal')
	y = scan_and_reconstruct(s, material, p, 0.1, 256)

	# save some meaningful results
	f = open('results/test_3_output.txt', mode='w')
	f.write('Mean value is ' + str(np.mean(y[64:192, 64:192])))
	f.write('Reconstructed value of entire phatom 1' + str(y)) #TODO:(RT) write the entire constructed image
	f.close()

	# how to check whether these results are actually correct?


# # Run the various tests
# print('Test 1')
# test_1()
# print('Test 2')
# test_2()
# print('Test 3')
# test_3()
