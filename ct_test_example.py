
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
	# explain what this test is for

	# work out what the initial conditions should be
	p = ct_phantom(material.name, 256, pic)
	s = source.photon('100kVp, 3mm Al')
	y = scan_and_reconstruct(s, material, p, 0.01, 256)

	# save some meaningful results
	save_draw(y, 'results', 'test_1_image')
	save_draw(p, 'results', 'test_1_phantom')

	# how to check whether these results are actually correct?


def test_2(pic):
	# TODO: (by YQ) 
	# explain what this test is for

	# work out what the initial conditions should be
	# 1 - simple circle for looking at calibration issues
	# 2 - point attenuator for looking at resolution
	#3 - single large hip replacement
	p_circle = ct_phantom(material.name, 256, 1)
	p_point = ct_phantom(material.name, 256, 2)
	p_hip = ct_phantom(material.name, 256, 3)

	s = source.photon('80kVp, 1mm Al')

	y_circle = scan_and_reconstruct(s, material, p_circle, 0.01, 256)
	y_point = scan_and_reconstruct(s, material, p_point, 0.01, 256)
	y_hip = scan_and_reconstruct(s, material, p_hip, 0.01, 256)
	
	# save some meaningful results
	save_plot(y_circle[128,:], 'results', 'test_2_plot_circle')
	save_plot(y_point[128,:], 'results', 'test_2_plot_point')
	save_plot(y_hip[128,:], 'results', 'test_2_plot_hip')

	# how to check whether these results are actually correct?

def test_3(pic):
	# explain what this test is for

	# work out what the initial conditions should be
	p = ct_phantom(material.name, 256, pic)
	s = fake_source(source.mev, 0.1, method='ideal')
	y = scan_and_reconstruct(s, material, p, 0.1, 256)

	# save some meaningful results
	f = open('results/test_3_output.txt', mode='a')
	f.write('Mean value is ' + str(np.mean(y[64:192, 64:192]))+ "\n" )
	f.close()

	# how to check whether these results are actually correct?


# Run the various tests
# print('Test 1')
# test_1()
# print('Test 2')
# test_2()
# print('Test 3')
# test_3()
