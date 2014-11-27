#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Finding optimal SVM parameters.

It uses a simple genetic algorithm from SciKit Python library.
"""

import cPickle as pickle
import sys
from sklearn import svm
import depikelpowers
import fft
from random import Random
from time import time
from ecspy import ec,terminators

if __name__ == '__main__':
    sample_time = 0.5
    depikelpowers.freq0 = 4.0
    depikelpowers.freq1 = 13.0
    depikelpowers.freq2 = 60.0



    # Loadin learning and testing data
    
    ll = open('learndata/lf_learn.txt','rb')
    rl = open('learndata/rf_learn.txt','rb')
    cl = open('learndata/cf_learn.txt','rb')

    rt = open('learndata/rf_test.txt','rb')
    lt = open('learndata/lf_test.txt','rb')
    ct = open('learndata/cf_test.txt','rb')

    l_data_p = pickle.load(ll)
    r_data_p = pickle.load(rl)
    c_data_p = pickle.load(cl)

    l_test_p = pickle.load(lt)
    r_test_p = pickle.load(rt)
    c_test_p = pickle.load(ct)


    # First parameters initialization 
    
    sample_time = 0.5
    depikelpowers.freq0 = 4.0
    depikelpowers.freq1 = 13.0
    depikelpowers.freq2 = 60.0
    
    i = 0

#c_test_p = depikelpowers.convert_to_pow(pickle.load(ct),sample_time)

def generate(random, args):
    """ Generates a random individual.
    
    **Keyword arguments:**
        * random -- a random number generator from Python's Random library
        * args -- used for scikit compatibility
        
    Returned value is an individual represented by a list of values.
    """
    
    # All elements are from range 0-1 and are rescaled later
    
    nu = random.uniform(0.0,1.0)            #c[0]
    tol = random.uniform(0.0,1.0)           #c[1]
    degree = random.uniform(0.0,1.0)        #c[2]
    gamma = random.uniform(0.0,1.0)         #c[3]
    sample_time = random.uniform(0.0,1.0)   #c[4]
    freq0 = random.uniform(0.0,1.0)         #c[5]
    freq1 = random.uniform(0.0,1.0)         #c[6]
    
    return [nu,tol,degree,gamma,sample_time,freq0,freq1]
#    gamma = random.uniform(0.0,10.0)
def eval(candidates, args):
    """ For a given list of individuals returns its fit function.
    
    **Keyword arguments**
        * candidates -- list of individuals
        * args -- used for scikit compatibility
        
    Returns a list of corresponding fitness values.
    """
    global i
    i+=1
    print '\n',i,
    fit = []
    try:
        for c in candidates:
            sample_time = c[4]
            
            
            #print depikelpowers.freq0,depikelpowers.freq1,depikelpowers.freq2
            
            # There is better version in git repo.
            
            l_data = fft.convert_to_fft(l_data_p,sample_time)
            r_data = fft.convert_to_fft(r_data_p,sample_time)
            c_data = fft.convert_to_fft(c_data_p,sample_time)
            
            
            
            l_test = fft.convert_to_fft(l_test_p,sample_time)
            r_test = fft.convert_to_fft(r_test_p,sample_time)
            c_test = fft.convert_to_fft(c_test_p,sample_time)
            
            fft_len = len(l_data[0])
            print '|',
            
            f1 = int(fft_len * (1.0-0.5*c[6]))
            f0 = int(fft_len * (0.5*c[5]))
            if f0 == f1:
                #f0 = 0
                f1 += 1
            
            
            
            l_data = map(lambda x: x[f0:f1],l_data)
            r_data = map(lambda x: x[f0:f1],r_data)
            c_data = map(lambda x: x[f0:f1],c_data)
            l_test = map(lambda x: x[f0:f1],l_test)
            r_test = map(lambda x: x[f0:f1],r_test)
            c_test = map(lambda x: x[f0:f1],c_test)
            
            
            
            y = [0] * len(c_data) + [1] * len(l_data) + [2] * len(r_data)
            
            clf = svm.NuSVC(
                probability = True,
                kernel = 'rbf', 
                cache_size = 1000, 
                nu=c[0], 
                tol=c[1]*1e-6, 
                degree=int(3+15.0*c[2]), 
                gamma=10.0*c[3]
                )    # Inicjowanie klasyfikatora SVM
           
            
            clf.fit(c_data+l_data+r_data,y)
                
            c = 0
            for x in c_test:
                p = clf.predict(x)
                if p == [0]: c += 1
                
            l = 0    
            for x in l_test:
                p = clf.predict(x)
                if p == [1]: l += 1
                
            r = 0
            for x in r_test:
                p = clf.predict(x)
                if p == [2]: r += 1
                
            fit.append((c+l+r)/float(len(c_test)+len(r_test)+len(l_test)))
        print max(fit)
    except:
        print 'emergency dump',sys.exc_info()
        em = open('emergency.dump.txt','wb')
        pickle.dump(candidates,em)
        em.close()
        raise
    return fit
    

def main():
    """ Initiates and runs the genetic algorithm.
    Parameters can be changed inside the source file.
    
    See :doc:`parameters`
    """
    rand = Random()
    rand.seed(int(time()))

    es = ec.ES(rand)
    es.terminator = terminators.user_termination
    es.terminator.termination_response_timeout = 1

    final_pop = es.evolve(
        generator = generate,
        evaluator = eval,
        pop_size=50,
        bounder=ec.Bounder(1e-2,1.0),
        max_evaluations=20,
        mutation_rate=0.25)

    final_pop.sort(reverse=True)

    f = open('output.txt','w')
    f.write(str(final_pop))
    f.close()
    print final_pop
    
if __name__ == "__main__":
    main()

