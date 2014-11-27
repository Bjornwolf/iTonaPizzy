#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Depickles the data and filters it."""

import cPickle as pickle
import sys
from emotiv import EmotivPacket

from matplotlib.pylab import figure, clf, plot, xlabel, ylabel, xlim, ylim, title, grid, axes, show, subplots
from scipy.signal import kaiserord, lfilter, firwin, freqz
from numpy import arange, pi, absolute, sqrt
from fft import stripes

name = 'data4'
senName = 'AF3 F7 F3 FC5 T7 P7 O1 O2 P8 T8 FC6 F4 F8 AF4'.split(' ')

filterAtt = 80
filterW = 0.01
sample_rate = 128.0


def main( plik ):

    
    
    fname = 'data/'+plik+'.txt'
    f = open(fname,'rb')
    
    val = {}
    
    input = pickle.load(f)
    
    delta = []
    theta = []
    alpha = []
    beta = []
    gamma = []
        
    for sens in senName:  
        data = []
        for x in input:
            data.append(x.sensors[sens]['value'])
                    
        #print '\n',sens
         
        dataF = filterFFT(data[0:],512)
        val[sens] = dataF
        #print dataF
        
        delta.append(val[sens][0])
        theta.append(val[sens][1])
        alpha.append(val[sens][2])
        beta.append(val[sens][3])
        gamma.append(val[sens][4])
    
    print val
    
    # --------------------------------
    # | Rysowanie wykresu:
    # --------------------------------
    
    width = 0.15
    ind = arange(14)
    
    fig, ax = subplots()
    
    
    deltaB = ax.bar(ind+width*0.0,delta,width,color='#ff00ff')
    thetaB = ax.bar(ind+width*1.0,theta,width,color='#00ff00')
    alphaB = ax.bar(ind+width*2.0,alpha,width,color='#0000ff')
    betaB  = ax.bar(ind+width*3.0,beta, width,color='#ffff00')
    gammaB = ax.bar(ind+width*4.0,gamma,width,color='#ff0000')
    
    ax.set_title(fname)
    ax.set_xticks(ind+width*3.0)
    ax.set_xticklabels(senName)
    ax.legend((deltaB[0],thetaB[0],alphaB[0],betaB[0],gammaB[0]),('Delta','Theta','Alpha','Beta','Gamma'))
    
    show()
    
    
    
    return val
    
    
    
   

def filterFFT(data,length):
    """Filters the signal, then counts alpha, beta, gamma, delta, theta.

    **Keyword arguments:**
        * data -- the signal (list of samples)
        * length -- maximum signal size
    
    Returns [delta, theta, alpha, beta, gamma] of the signal."""
    N, beta = kaiserord(filterAtt, filterW)
    nyq_rate = sample_rate / 2.0
    delay = 0.5 * (N-1) / sample_rate
    
    

    # liczenie pochodnej:
    dataD = []
    prev = data[0]

    for x in data[1:length+1]:
        temp = x - prev
        if temp < -64: temp = -64
        if temp > 64: temp = 64
        dataD.append(temp)
        prev = x 
    
    t = arange(len(dataD)) / sample_rate
    
    # przygotowanie filtra:
    fir = firwin(N, cutoff = 0.3/nyq_rate, window=('hanning'))
    fir = -fir
    fir[N/2] = fir[N/2]+1
    
    dataDF = lfilter(fir,1.0,dataD)
    
    
    
    #dataDfft = stripes(dataD,None)
    dataDFfft = hot_winges(dataDF[delay:length+delay],None)
    #print len(dataDFfft)
    dataDFfft = map(lambda x: sqrt(x),dataDFfft)
    
    ft = arange(len(dataDFfft)) / (  length / sample_rate)
    
    delta = 0
    theta = 0
    alpha = 0
    beta = 0
    gamma = 0
    
    sum = 0
    for i in range(2,len(ft)):
        if ft[i] < 4:
            delta += dataDFfft[i]
        elif ft[i] < 7:
            theta += dataDFfft[i]
        elif ft[i] < 15:
            alpha += dataDFfft[i]
        elif ft[i] < 31:
            beta += dataDFfft[i]
        else:
            gamma += dataDFfft[i]
        sum += dataDFfft[i]
        
    sum = float(sum)
    if sum < 1: sum = 1
    

    return map(lambda x:x/sum,[delta,theta,alpha,beta,gamma])
    
if __name__ == "__main__":
    main(name)
#main(name)