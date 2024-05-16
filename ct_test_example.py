
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

def test_1(pic):
	"""draw the reconstructed image and plot values of an impulse, simple disc or hip implant respectively using an '100kVp, 3mm Al' energy source packet"""

	# work out what the initial conditions should be
	p = ct_phantom(material.name, 256, pic)
	s = source.photon('100kVp, 3mm Al')
	y = scan_and_reconstruct(s, material, p, 0.01, 256)

	save_plot(y[128,:], 'results', 'test_1_p'+ str(int(pic))+ '_plot')
	# save some meaningful results
	save_draw(y, 'results', 'test_1_p'+ str(int(pic))+ '_image')
	save_draw(p, 'results', 'test_1_p'+ str(int(pic))+ '_phantom')

	# how to check whether these results are actually correct?
	"""Check that the 2 drawings of reconstructed scan image and direct phantom image are identical"""
	"""Check that cross-section values of the reconstructed image are consistent with the drawings"""


# def test_2_yq():
# 	# TODO: (by YQ) 
# 	# explain what this test is for

# 	# work out what the initial conditions should be
# 	# 1 - simple circle for looking at calibration issues
# 	# 2 - point attenuator for looking at resolution
# 	#3 - single large hip replacement
# 	p_circle = ct_phantom(material.name, 256, 1)
# 	p_point = ct_phantom(material.name, 256, 2)
# 	p_hip = ct_phantom(material.name, 256, 3)

# 	s = source.photon('80kVp, 1mm Al')

# 	y_circle = scan_and_reconstruct(s, material, p_circle, 0.01, 256)
# 	y_point = scan_and_reconstruct(s, material, p_point, 0.01, 256)
# 	y_hip = scan_and_reconstruct(s, material, p_hip, 0.01, 256)
	
# 	# save some meaningful results
# 	save_plot(y_circle[128,:], 'results', 'test_2_plot_circle')
# 	save_plot(y_point[128,:], 'results', 'test_2_plot_point')
# 	save_plot(y_hip[128,:], 'results', 'test_2_plot_hip')
	

# 	# how to check whether these results are actually correct?

def test_2():
	"""Output the mean value of the scanned and reconstructed image of a simple disc with different materials 
	using an ideal source packet"""

	# work out what the initial conditions should be
	
	s = fake_source(source.mev, 0.1, method='ideal')
	mat_test = ["Soft Tissue", "Water", "Bone"]
	results = np.empty(len(mat_test))
	for (i,mat_name) in enumerate(mat_test):
		p =  ct_phantom(material.name, 256, 1, metal = mat_name)
		y = scan_and_reconstruct(s, material, p, 0.1, 256)
		results[i] = np.mean(y[64:192, 64:192])
		print("measured attenuation coefficient for ", mat_name, " is ", results[i])
	
	f = open('results/test_3_output.txt', mode='a')
	f.write(f'Detected mean attenuation coefficient for {mat_test} are {results}\n')
	# assume ideal fake_source with peak at 0.07MeV
	f.write(f'Expected mean attenuation coefficient for {mat_test} are [0.204, 0.194, 0.502]\n') # assume ideal fake_source peak at 0.07MeV
	f.close()


# Run the various tests
# print('Test 1')
# test_1()
# print('Test 2')
# test_2()
# print('Test 3')
# test_3()
