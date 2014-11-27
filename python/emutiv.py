#!/usr/bin/python
# -*- coding: utf-8 -*-

"""The module emulates device input using pickled data from a file. FOR TESTING PURPOSES ONLY."""

import gevent
import os
import pickle
from gevent.queue import Queue
from emotiv import Emotiv

fname = 'data/data5.txt'

sensorPos = {
    'AF3': (-64, -124),
    'F3': (-34, -80),
    'F7': (-107, -74),
    'FC5': (-80, -43),
    'T7': (-124, 0),
    'P7': (-78, 99),
    'O1': (-37, 147),
    'AF4': (64, -124),
    'F4': (34, -80),
    'F8': (107, -74),
    'FC6': (80, -43),
    'T8': (124, 0),
    'P8': (78, 99),
    'O2': (37, 147)}
    
class Emutiv():
    """Emotiv device emulator."""
    channels = ['F3','F4','P7','FC6','F7','F8','T7','P8','AF4','T8','AF3','O2','O1','FC5']
    def __init__(self,displayOutput=False):
        """Constructs an emulator instance."""
        self.file = open(fname,'rb')
        self.input = pickle.load(self.file)
        
        self.packets = Queue()
       
        
    def setup(self):
        """Sets an emulator up."""
        print 'started'
        while True:
            for x in self.input:
                x.__recovery__()
                self.packets.put_nowait(x)
                gevent.sleep(0.0078125)
                
    def dequeue(self):
        """Read another packet from the file."""
        try:
            return self.packets.get()
        except Exception, e:
            print e
        
    def empty(self):
        """Returns True if packet queue is empty."""
        try:
            return self.packets.empty()
        except Exception, e:
            print e
            
    def close(self):
        """Quits the emulator."""
        self.file.close()
        
