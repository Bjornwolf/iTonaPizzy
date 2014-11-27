#!/usr/bin/python
# -*- coding: utf-8 -*-

"""An actual graph application."""

import pygame
import socket
import threading
import cPickle as pickle
from graph import Graph

msg = ""
flag = False


    
def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 900))
    
    g = Graph()
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = 'localhost'
    port = 31415 
    s.connect((host, port))
    
    
    
    s.send('GRAPH')
    str = s.recv(65536)
    if str[0] == 'G':
        g.read_graph_pickle(str[2:])
    else:
        print 'Packet error'
        return
    
    s.setblocking(0)
    while True:
        g.draw_graph(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                return
        try:
            buf = s.recv(32)
            print buf
            if buf[0] == 'C':
            
                g.set_current(int(buf[2:]))
        except:
            pass
        
if __name__ == "__main__":
    main()