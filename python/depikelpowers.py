#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Depickles the data and counts powers."""

import pygame
import emotiv

from emotiv import EmotivPacket
from scipy import signal

freq0 = 26.6263433538
freq1 = 31.5718372336
freq2 = 33.3


def convert_to_pow(fdata=[],sample_time=0.5):

    """Converts the signal to a list of powers in alpha and beta bands.
        
    **Keyword arguments:**
        * fdata -- signal (list of samples)
        * sample_time -- interval between samples
    
    Returns a list of powers in alpha/beta bands over time."""
    N, beta = signal.kaiserord(80, 0.1)
    falpha = signal.firwin(N, [freq0, freq1], pass_zero=False, nyq = 64.0)
    fbeta = signal.firwin(N, [freq1, freq2], pass_zero=False, nyq = 64.0)

    sample_size = int(128.0 * sample_time)
    i = 0
    out_data = []
    tmp = {'F3':[], 'F4':[], 'P7':[], 'FC6':[], 'F7':[], 'F8':[], 'T7':[], 'P8':[], 'AF4':[], 'T8':[], 'AF3':[], 'O2':[], 'O1':[], 'FC5':[]}
    
    for x in fdata:
        i += 1
        for n in emotiv.channels:
            tmp[n].append(x.sensors[n]['value'])
            
        if i == sample_size:
            i = 0
            dumpable = []
            
            for n in emotiv.channels:
                sample = tmp[n]
                
                sample_alpha = signal.lfilter(falpha, 1.0, sample)
                sample_beta = signal.lfilter(fbeta, 1.0, sample)
                
                power_alpha = reduce(lambda x, y: x + y, map(lambda z: z * z, sample_alpha)) / (sample_size * 1000000.0)
                power_beta = reduce(lambda x, y: x + y, map(lambda z: z * z, sample_beta)) / (sample_size * 1000000.0)
                
                dumpable.append( power_alpha )
                dumpable.append( power_beta )
                
                tmp[n] = []
            
            out_data.append(dumpable)
            
    
    return out_data
    
