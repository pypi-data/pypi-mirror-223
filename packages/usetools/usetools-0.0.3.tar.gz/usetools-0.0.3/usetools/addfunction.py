#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  9 15:48:16 2023

@author: lucas

Additional Functions
"""
# %% System function
import os
def checkcreate(directory):
    if not os.path.exists(directory): 
        os.makedirs(directory)
        print(f'created directory: {directory}')

# %% Pulses functions
import numpy as np

def gaussian_pulse(t, b, cvt=1, sigma=None, FWHM=None, area=1, mu=1):
    '''Gaussian pulse function'''
    # g(t) = a.exp(-(t-b)**2/2.c**2)
    # t = time range [s]
    # b = pulse maximum time shift [s]
    # c = 2.sqrt(2ln2)*FWHM [s] (FFT: c = sqrt(2ln2)/pi/FWHM_freq)
    # cvt = time conversion rate
    if sigma: 
        c = sigma*cvt
    elif FWHM:
        c = FWHM/2/np.sqrt(2*np.log(2))*cvt
    else:
        c = 1/2/np.sqrt(2*np.log(2))*cvt
   
    # normalization
    # a = 1/np.sqrt(2*np.pi)/c # np.trapz(pulse, dx=(t[1]-t[0])) = 1
    a = (area/mu)/np.sqrt(2*np.pi)/c # area has units of GigaJoules if mu is Cm
    b = b*cvt
    # Pulse
    g = a*np.exp( -(t - b)**2/(2*c**2) )

    # return a gaussian pulse with time duration equals to area (eg. pi-pulse)
    # depends on the dipole moment, usually not time variable
    # if area: g = area*g/mu*cvt #np.trapz(mu*g, dx=(t[1]-t[0]))
    
    return g

def const_wave(t, w, t0=0, wtype='sine', phase=0):
    '''Contant wave function'''
    # t = time range [s]
    # w = frequency [Hz]
    # phase = initial phase angle [-]
    arg = np.pi*( w*(t-t0) + phase/2)
    #
    if wtype == 'sine':
        p = np.imag(np.exp(1j*arg))
    elif wtype == 'cos':
        p = np.real(np.exp(1j*arg))
    else:
        raise TypeError("choose cosine or sine wave")
    return p/abs(p).max()

def savedict2pars(dictionary, folder, fname=''):
    
    text = " Parameters for calculations \n"\
    "__________________________________________________\n"
        
    for key, value in dictionary.items():
        text += f"{key} : {value}\n"
    
    with open(folder + f'/Parameters{fname}.txt', 'w') as f:
        f.write(text)

