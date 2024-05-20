
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

def test_4():
    """contrast reconstructed image using real vs ideal source packet"""

    pic = int(input("Enter the phantom type: "))
    metal = input("Enter the metal type: ")
    p = ct_phantom(material.name, 256, pic, metal=metal) 

    # convert phantom where each pixel stores material index to attenuation coefficient mu at the peak energy value
    peak_energy = 0.07 # MeV
    p_mu = phantom_mu(p, material, peak_energy)

    s_real = source.photon('100kVp, 3mm Al')
    y_real = scan_and_reconstruct(s_real, material, p, 0.01, 256)
    y_harden_w = scan_and_reconstruct(s_real, material, p, 0.01, 256, harden_w = True)
    s_ideal = fake_source(source.mev, 0.1, method='ideal')
    y_ideal = scan_and_reconstruct(s_ideal, material, p, 0.01, 256)
    

    # save some meaningful results
    save_draw(y_real, 'results', 'test_4_p'+ str(int(pic))+ '_image_real', caxis=[-1,2])
    save_draw(y_ideal, 'results', 'test_4_p'+ str(int(pic))+ '_image_ideal', caxis=[-1,2])
    save_draw(y_harden_w, 'results', 'test_4_p'+ str(int(pic))+ '_image_hardening_correction', caxis=[-1,2])
    save_draw(p_mu, 'results', 'test_4_p'+ str(int(pic))+ '_phantom_mu', caxis=[-1,2])

    # how to check whether these results are actually correct?
    # check that the 2 drawings of reconstructed scan image and direct phantom image are identical


def test_5():
    """Check that the water calibration function in ct_calibrate.py 
    generates the correct result when scanning a disk made entirely of water, as well as other materials"""
    metal = input("Enter the metal type: ")
    p = ct_phantom(material.name, 256, 1, metal=metal) # type 1 phantom generates a disk of uniform material
 
    s = source.photon('100kVp, 3mm Al')

    # Find actual coefficients for the phantom
    peak_energy = 0.07 # MeV, 70% of 100kVp
    energy_idx = np.nonzero(material.mev==peak_energy)[0][0]
    mu = material.coeff(metal)[energy_idx]
    
    y = scan_and_reconstruct(s, material, p, 0.01, 256)
    y_mean = np.mean(y[64:192, 64:192])
    y_w = scan_and_reconstruct(s, material, p, 0.01, 256, harden_w = True)
    y_w_mean = np.mean(y_w[64:192, 64:192])

    f = open('results/test_5_output.txt', mode='a')
    f.write(f'Actual attenuation coefficient for {metal} disk are {mu}.\n')
    f.write(f'Detected attenuation coefficient without beam hardening calibration for {metal} disk are {y_mean}.\n')
    f.write(f'Detected attenuation coefficient with beam hardening calibration (using water) for {metal} disk are {y_w_mean}.\n')
    f.close()

    # save_draw(p_mu, 'results', 'test_5_p'+ str(int(pic))+ '_phantom_mu', caxis=[-1,2])
    # save_draw(y, 'results', 'test_5_p'+ str(int(pic))+ '_' + metal + '_image', caxis=[-1,2])
    # save_draw(y_w, 'results', 'test_5_p'+ str(int(pic))+ '_' + metal + '_image_hardening_correction', caxis=[-1,2])
