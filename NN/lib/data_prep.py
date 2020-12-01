'''
data_prep - functions pre-processing velocity fields for NN input.
'''

import os
import numpy as np
from astropy.io import fits
import cv2


def channel_dictionary(hdu, ext):
    '''
    Function internal to MaNGA data that enables access to 
    different emission line channels. Used here to find mask 
    for emission line h-alpha.
    '''
    channel_dict = {}
    for k, v in hdu[ext].header.items():
        if k[0] == 'C':
            try:
                i = int(k[1:])-1
            except ValueError:
                continue
            channel_dict[v] = i
    return channel_dict


def processed_vfields(plateifu, data_dir, shape=(32, 32)):
    '''
    returns normalised [-1, 1] pixel value range and standard size (defined by shape)
    velocity (stars and gas) for a given MaNGA galaxy. For use with input to NN.
        
    ----------
    Parameters
    
    plateifu : str
        Plateifu identifier of MaNGA galaxy.    
    
    data_dir : str
        Directory containing VOR10-GAU-MILESHC velocity 
        fields from MaNGA.
        
    shape : (int, int)
        Shape of output velocity field images.
        
    -------
    Returns
    
    stel_vfield : np.array(shape)
        Normalised stellar velocity field. Pixels range from
        -1 to 1, and has been resized to shape input param.
         
    gas_vfield : np.array(shape)
        Normalised gas velocity field. Pixels range from
        -1 to 1, and has been resized to shape input param.
    
    '''
    # Finding base MAPS directory and pulling individual files. 
    file_name = 'manga-' + plateifu + '-MAPS-VOR10-MILESHC-MILESHC.fits.gz'
    file_path = os.path.join(data_dir, plateifu.split("-")[0], 
                             plateifu.split("-")[1], file_name)
    
    # checking if file exists, then returning exception error if not.
    if os.path.isfile(file_path) == False: 
        raise FileNotFoundError(plateifu +' not found!')
        return
    
    # loading fits object + finding emission line velocity.
    hdu = fits.open(file_path)
    emlc = channel_dictionary(hdu, 'EMLINE_GVEL')
    
    # stellar velocity field
    smask_ext = hdu['STELLAR_VEL'].header['QUALDATA']
    stel_vfield = np.ma.MaskedArray(hdu['STELLAR_VEL'].data, 
                                    mask = hdu[smask_ext].data > 0)
    
    # normalising to -1, 1 range.
    stel_vfield = stel_vfield.data / np.abs(stel_vfield).max()
    # rescaling to target shape.
    stel_vfield = cv2.resize(stel_vfield, dsize=shape, interpolation=cv2.INTER_CUBIC)
    
    # ionized gas velocity field
    gmask_ext = hdu['EMLINE_GVEL'].header['QUALDATA']
    halpha_vfield = np.ma.MaskedArray(hdu['EMLINE_GVEL'].data[emlc['Ha-6564'],:,:], 
                                      mask = hdu[gmask_ext].data[emlc['Ha-6564'],:,:] > 0) 
    
    # normalising to -1, 1 range.
    halpha_vfield = halpha_vfield.data / np.abs(halpha_vfield).max()
    # rescaling to target shape.
    halpha_vfield = cv2.resize(halpha_vfield, dsize=shape, interpolation=cv2.INTER_CUBIC)
    
    return stel_vfield, halpha_vfield
