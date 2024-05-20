
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

	# initial conditions
	p = ct_phantom(material.name, 256, pic)
	
	# convert phantom where each pixel stores material index to attenuation coefficient mu at the peak energy value
	peak_energy = 0.07 # MeV
	p_mu = phantom_mu(p, material, peak_energy)
	
	s = source.photon('100kVp, 3mm Al')
	y = scan_and_reconstruct(s, material, p, 0.01, 256)

	# plot the 1D cross-section of the reconstructed image
	save_plot(y[128,:], 'results', 'test_1_p'+ str(int(pic))+ '_plot')
	# display the drawings of the reconstructed image and the phantom
	save_draw(y, 'results', 'test_1_p'+ str(int(pic))+ '_image', caxis=[-1,2])
	save_draw(p_mu, 'results', 'test_1_p'+ str(int(pic))+ '_phantom_mu', caxis=[-1,2])

	# to check whether the results are correct, compare the images visually
	"""Check that the 2 drawings of reconstructed scan image and direct phantom image are identical"""
	"""Check that cross-section values of the reconstructed image are consistent with the drawings"""



def test_2():
	"""Output the mean value of the scanned and reconstructed image of a simple disc with different materials 
	using an ideal source packet"""

	# initial conditions
	s = fake_source(source.mev, 0.1, method='ideal')
	mat_test = ["Soft Tissue", "Water", "Bone"]
	results = np.empty(len(mat_test))
	
	# TODO: (RT) updated 19/05/2024
	# get the attenuation coefficient energy index for each material at 0.07MeV
	energy_idx = np.nonzero(material.mev==0.07)[0][0]
	mu = np.empty(len(mat_test))
	per_error = np.empty(len(mat_test))

	for (i,mat_name) in enumerate(mat_test):
		p =  ct_phantom(material.name, 256, 1, metal = mat_name)
		y = scan_and_reconstruct(s, material, p, 0.1, 256)
		results[i] = np.mean(y[64:192, 64:192])
		print("measured attenuation coefficient for ", mat_name, " is ", results[i])

		# TODO: (RT) updated 19/05/2024
		mu[i] = material.coeff(mat_name)[energy_idx]
		per_error[i] = (results[i] - mu[i]) / 0.2 * 100
	
	f = open('results/test_2_output.txt', mode='a')
	f.write(f'Detected mean attenuation coefficient for {mat_test} are {results}.\n')

	# TODO: (RT) updated 19/05/2024
	# assume ideal fake_source with peak at 0.07MeV
	f.write(f'Expected mean attenuation coefficient for {mat_test} are {mu}.\n') 
	# f.write(f'Expected mean attenuation coefficient for {mat_test} are [0.204, 0.194, 0.502]\n') # assume ideal fake_source peak at 0.07MeV
	f.write(f'Percentage error for {mat_test} are {per_error}%.\n')

	f.close()

def test_3(pic,source_string):
	
	"""Output the variance of the scanned and reconstructed image of with different materials """
	# Create the mapping dictionary for material indices and names
	material_index_map = {
		0: "Air",
		1: "Adipose",
		2: "Soft Tissue",
		3: "Breast Tissue",
		4: "Water",
		5: "Blood",
		6: "Bone",
		7: "Titanium",
		8: "Cobalt",
		9: "Chromium",
		10: "Iron",
		11: "Carbon",
		12: "Nickel",
		13: "Manganese",
		14: "Aluminium",
		15: "Copper",
		16: "Co-Cr",
		17: "Stainless Steel",
		18: "Acrylic"
	}
	# Initial conditions
	p = ct_phantom(material.name, 256, pic)
	
	s = source.photon(source_string)
	y = scan_and_reconstruct(s, material, p, 0.01, 256)
 	# Initialize a dictionary to hold coefficients for each unique material index
	coefficients_dict = {}

    # Iterate through 'p' and 'y' to populate the dictionary
	for i in range(p.shape[0]):
		for j in range(p.shape[1]):
			material_index = p[i][j]
			coefficient = y[i][j]

			# Initialize the list if the material index is not already in the dictionary
			if material_index not in coefficients_dict:
				coefficients_dict[material_index] = []

			coefficients_dict[material_index].append(coefficient)

    # Calculate the variance for the coefficients of each material
	variance_dict = {material_index: np.var(coefficients) for material_index, coefficients in coefficients_dict.items()}

    # Print the variances
	for material_index, variance in variance_dict.items():
		material_name = material_index_map.get(material_index, "Unknown material")
		print(f"Variance for material {material_name}: {variance}")
	
	#f = open('results/test_3_variance.txt', mode='a')
	#f.write(f'Detected variance for source {source_string} and material are {results}.\n')

	#f.close()


# Run the various tests
# print('Test 1')
# test_1()
# print('Test 2')
# test_2()
# print('Test 3')
# test_3()
