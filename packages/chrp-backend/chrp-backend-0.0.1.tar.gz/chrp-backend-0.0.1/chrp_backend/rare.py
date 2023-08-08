import numpy as np

import torch
from torch import nn
import torch.nn.functional as F
from torch import optim

import os

import h5py

from .utils import *


class Solution(torch.nn.Module):
    def __init__(self, guess):
        super().__init__()
        self.x = nn.parameter.Parameter(guess, requires_grad=True)
        self.id = nn.Identity()

    def forward(self):
        return self.id(self.x)
    

class RARE():
    def __init__(self, prior_path, regularization_parameter=1, use_cuda=False):

        super().__init__()

        self.prior_path = prior_path
        self.regularization_parameter = regularization_parameter
        self.device = "cuda" if use_cuda==True else "cpu"
        self.prior = self.load_prior()

        self.history = []

    def load_prior(self):
        prior = CNNPrior(        
        in_channels=2,
        hidden_channels=64,
        n_layers=10,
        out_channels=2,
        kernel_size=3,
        stride=1,
        padding='same',
        groups=1).to(device=self.device)

        prior.load_state_dict(torch.load(self.prior_path, map_location=self.device))

        prior.eval()

        return prior
    
    def np_complex_to_tensor(self, arr):

        out = torch.view_as_real_copy(torch.tensor(arr, dtype=torch.cfloat))

        return out
    
    def standard_scaling(self, arr):
        
        out = (arr - arr.mean())/arr.std()

        return out
    
    def fit(self, kspace_data, iterations=500, learning_rate=10**(-10), print_every=100):

        kspace_tensor = self.np_complex_to_tensor(kspace_data).to(device=self.device)

        guess = ifft_func(kspace_tensor)

        self.xhat = Solution(guess=guess).to(device=self.device)
        self.optimizer = optim.Adam(self.xhat.parameters(), lr=learning_rate)

        for epoch in range(iterations):

            x = self.xhat()

            self.history.append(x.detach().cpu().numpy())

            fft_loss = F.mse_loss(  fft_func(x), kspace_tensor, reduction='mean' )

            scaled_x = self.standard_scaling(x.permute(3,0,1,2).unsqueeze(0))

            with torch.no_grad():

                denoised_x = self.prior(scaled_x)

            prior_loss = F.mse_loss(scaled_x, denoised_x) #fixed prior loss

            loss = fft_loss + self.regularization_parameter*prior_loss

            if epoch % print_every == 0:
                print(f'epoch: {epoch}')
                print(f'fft_loss: {fft_loss}')
                print(f'prior_loss: {prior_loss}')
                print(f'total loss: {loss}')

            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

        out = self.xhat()

        return out.detach().cpu().numpy()

    

class CNNPrior(nn.Module):
    def __init__(
        self,
        in_channels=2,
        hidden_channels=64,
        n_layers=10,
        out_channels=2,
        kernel_size=3,
        stride=1,
        padding='same',
        groups=1,
    ):
        super(CNNPrior, self).__init__()

        self.in_channels = in_channels
        self.hidden_channels = hidden_channels
        self.n_layers = n_layers
        self.out_channels = out_channels
        self.kernel_size = kernel_size
        self.stride = stride
        self.padding = padding
        self.groups = groups
        
        self.conv_layers = nn.ModuleList()
        
        # first layer
        self.conv_layers.append(nn.Conv3d(in_channels=self.in_channels, out_channels=self.hidden_channels, kernel_size=self.kernel_size, stride=stride, padding=padding, groups=groups))

        for ii in range(n_layers-2): # intermediate layers

            self.conv_layers.append(nn.Conv3d(in_channels=self.hidden_channels, out_channels=self.hidden_channels, kernel_size=self.kernel_size, stride=stride, padding=padding, groups=groups))
            
        # last layer
        self.conv_layers.append(nn.Conv3d(in_channels=self.hidden_channels, out_channels=self.out_channels, kernel_size=self.kernel_size, stride=stride, padding=padding, groups=groups))
        
        self.apply(self._init_weights)
        
    def _init_weights(self, module):
        
        if isinstance(module, nn.Conv3d):
            nn.init.dirac_(module.weight)
            module.bias.data.normal_(mean=0.0, std=0.000001)




    def forward(self, x):
        
        h = x

        for ind, layer in enumerate(self.conv_layers[:-1]):
            h = layer(h)
            h = F.leaky_relu(h)

        h = self.conv_layers[-1](h)

        return h
    



if __name__ == "__main__":

    rare = RARE(prior_path='./chrp/priors/cnn_prior_4_5_noise_level_0_1.pt', regularization_parameter=10**(-6), use_cuda=True)

    print(rare.prior)

    kspace_data = fastmri_file_load('./data/file_brain_AXFLAIR_200_6002425.h5')[0][:,6,...]

    thing = rare.fit(kspace_data=kspace_data, iterations=500, learning_rate=10**(-12))

    converge = [np.linalg.norm(x.flatten() - rare.history[-1].flatten()) for x in rare.history]

    import matplotlib.pyplot as plt

    plt.imshow(rare.history[-1][6,:,:,0], cmap='inferno')
    plt.show()

    #breakpoint()
