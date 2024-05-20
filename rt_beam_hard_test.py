
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
    p = ct_phantom(material.name, 256, pic, metal=metal) # TODO: can try a different material type for pic = 1

    # convert phantom where each pixel stores material index to attenuation coefficient mu at the peak energy value
    peak_energy = 0.07 # MeV
    p_mu = phantom_mu(p, material, peak_energy)

    s_real = source.photon('100kVp, 3mm Al')
    y_real = scan_and_reconstruct(s_real, material, p, 0.01, 256)
    s_ideal = fake_source(source.mev, 0.1, method='ideal')
    y_ideal = scan_and_reconstruct(s_ideal, material, p, 0.01, 256)

    # save some meaningful results
    save_draw(y_real, 'results', 'test_4_p'+ str(int(pic))+ '_image_real', caxis=[-1,2])
    save_draw(y_ideal, 'results', 'test_4_p'+ str(int(pic))+ '_image_ideal', caxis=[-1,2])
    save_draw(p_mu, 'results', 'test_4_p'+ str(int(pic))+ '_phantom_mu', caxis=[-1,2])

    # how to check whether these results are actually correct?
    # check that the 2 drawings of reconstructed scan image and direct phantom image are identical


def test_4_2():
    """Check that the water calibration function in ct_calibrate.py 
    generates the correct result when scanning a disk made entirely of water, as well as other materials"""
    pic = int(input("Enter the phantom type: "))
    metal = input("Enter the metal type: ")
    p = ct_phantom(material.name, 256, pic, metal=metal)
