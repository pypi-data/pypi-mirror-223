import numpy as np

import torch
from torch import nn
import torch.nn.functional as F
from torch import optim

import os

import h5py

import pkg_resources

prior_path = 'priors'
prior_filepath = pkg_resources.resource_filename(__name__, prior_path)

def list_priors():

    filenames = [x.split('.')[0] for x in os.listdir(prior_filepath) if x[-3:] == '.pt']
    #noise_level_strings = [x.split('_noise_level_')[1] for x in filenames]
    #noise_level_values = [float(x.replace('_', '.')) for x in filenames]
    #names = [f'cnn prior, noise level {x}' for x in noise_level_values]
    return filenames

def name_to_path(name):

    return prior_filepath + name + '.pt'



def fastmri_file_load(filename):
    
    with h5py.File(filename, "r") as f:
        data_kspace = f.get('kspace')[...]
        data_reconstruction = f.get('reconstruction_rss')[...]
        
    return (data_kspace, data_reconstruction)
    

def fastmri_kspace_to_image(arr, coil):
    return np.fft.fftshift(np.fft.ifftn(np.fft.fftshift(arr[:,coil,:,:])))[:,320//2:640-320//2,:]


def fft_func(x):
    
    return torch.view_as_real(torch.fft.fftshift(torch.fft.fftn( torch.view_as_complex(x), dim=[0,1,2])))


def ifft_func(x):
    
    return torch.view_as_real( torch.fft.ifftshift (torch.fft.ifftn( torch.fft.ifftshift( torch.view_as_complex(x) ) ), dim=[0,1,2] ) )