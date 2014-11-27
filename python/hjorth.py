#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Contains Hjorth analysis functions."""

import random

samples_per_timeframe = 256
sampling_period = 1.0 / 128.0

def derivative(values):
    """Counts the signal's derivative.

    **Keyword arguments:**
        * values -- signal (list of samples)
    
    Returns the first derivative of the signal."""
    derivs = []
    derivs.append((values[1] - values[0]) / sampling_period)
    l = len(values)
    for i in range(1,l-1):
        derivs.append((values[i+1] - values[i-1]) / (2 * sampling_period))
    derivs.append((values[l-1] - values[l-2]) / sampling_period)
    return derivs

def average(values):
    """Counts the average value of a given list.

    **Keyword arguments:**
        * values -- list of values
    
    Returns the average of the values."""
    return reduce(lambda x, y: x + y, values) / len(values)

def variance(values):
    """Counts the variance of a given list.

    **Keyword arguments:**
        * values -- list of values
    
    Returns the variance of the values."""
    avg = average(values)
    return average(map(lambda x: (x - avg)**2,values))

def activity(signal):
    """Counts the activity coefficient of Hjorth's signal analysis.

    **Keyword arguments:**
        * signal -- list of samples
    
    Returns the signal's activity."""
    return variance(signal)
    
def mobility(signal):
    """Counts the mobility coefficient of Hjorth's signal analysis.

    **Keyword arguments:**
        * signal -- list of samples
    
    Returns the signal's mobility."""
    return (variance(derivative(signal)) / variance(signal)) ** 0.5

def complexity(signal):
    """Counts the complexity coefficient of Hjorth's signal analysis.

    **Keyword arguments:**
        * signal -- list of samples
    
    Returns the signal's complexity."""
    return mobility(derivative(signal)) / mobility(signal)
    
def avg_hjorth(values):
    """Counts the list's average of Hjorth's coefficients.

    **Keyword arguments:**
        * values -- list of tuples (activity, mobility, complexity)
    
    Returns the (average activity, average mobility, average complexity) tuple."""
    (a,b,c) = reduce(lambda (x,y,z), (t,u,v): (x + t, y + u, z + v), values)
    l = len(values)
    return (a/l, b/l, c/l)
