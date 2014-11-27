#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module performs a variety of FFT-related operacions."""

from numpy.fft import rfft
from cmath import polar
import emotiv

def normalise(data, small, big):
    """Normalises data in a list to fit range [small,big).

    **Keyword arguments:**
        * data -- list of values
        * small -- minimum value
        * big -- maximum value
    
    Returns a list of normalised values."""
    
    min_d = min(data)
    max_d = max(data)
    if min_d == max_d:
        return map(lambda x: (big + small) / 2, data)
    f = lambda x: small + (x - min_d) * (big - small) / (max_d - min_d)
    return map(f, data)

def stripes(signal, window):
    """Performs fft conversion.
    The data are normalised.
    
    **Keyword arguments:**
        * signal -- list of signal values
        * window -- window size in # of samples
    
    Returns a list of fft values."""
    n = normalise(map(lambda x: polar(x)[0], rfft(signal, window))[1:], 0, 255)
    return bytearray(map(lambda x: int(round(x)), n))
    
def hot_winges(signal, window):
    """Performs fft conversion.
    The data are NOT normalsed.
    
    **Keyword arguments:**
        * signal -- list of signal values
        * window -- window size in # of samples
    
    Returns a list of fft values."""
    
    return map(lambda x: polar(x)[0], rfft(signal, window))[1:]


def phases(signal, window):
    """."""
    return map(lambda x: polar(x)[1], rfft(signal, window))
    
def avg(values):
    """Computes the average value of list elements.
    
    **Keyword arguments:**
        * values -- list of values to be averaged
    
    Returns a value."""
    return reduce(lambda x, y: x + y, values) / len(values)
    
def avg_fft(fouriers):
    """Computes the average values from list of lists.
    
    **Keyword arguments:**
        * fouriers -- list of lists of values
    
    Returns a list of averaged values."""
    if fouriers[0] == []:
        return []
    return [avg([l[0] for l in fouriers])] + avg_fft(map(lambda x: x[1:], fouriers))
    
    
def convert_to_fft(data, sample_time):
    """Converts signal to a list of averaged fourier values.
    
    **Keyword arguments:**
        * data -- list of EmotivPackets
        * sample_time -- length of a window
    
    Returns a list of averaged fourier values.    
    """
    i = 0
    out_data = []
    tmp = [[], [], [], [], [], [], [], [], [], [], [], [], [], []]
    sample_size = int(128.0 * sample_time)
    
    
    for x in data:
        i += 1
        
        for (j,n) in enumerate(emotiv.channels):
            tmp[j].append(x.sensors[n]['value'])
        
        if i == sample_size:
            i = 0
            dumpable = []
            
            average_fft_vals = avg_fft(map(lambda x: hot_winges(x,sample_size),tmp))
            # data Sample = [Float]
            # avg_fft :: [Sample] -> [Float]

            for n in range(14): 
                tmp[n] = []
  
            out_data.append(dumpable)
    return out_data
            
    

