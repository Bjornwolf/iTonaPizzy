#!/usr/bin/python
# -*- coding: utf-8 -*-

"""The class that handles the graph."""

import pygame
import cPickle as pickle

    
    
class Graph(object):
    STOP = 0
    UP = 3
    DOWN = 4
    LEFT = 1
    RIGHT = 2
    def __init__(self):
        """Constructs the graph instance."""

        self.names = []
        self.edges = []
        self.coords = []
        self.n = 0
        self.current = 0
    
    def colour(self,t):
        """Assigns a colour to the node.
        
        **Keyword arguments:**
            * t -- one of of [UP, DOWN, LEFT, RIGHT]

        Returns a triple RGB."""
        if t == self.UP:
            return (0,255,0)
        if t == self.LEFT:
            return (255,0,0)
        if t == self.DOWN:
            return (255,255,0)
        if t == self.RIGHT:
            return (0,0,255)
        
        return (255,255,255)
    
    def draw_arrow(self,surface, col, (x1,y1), (x2,y2)):
        """Listens for a new client, then attaches it as a new thread.
        
        **Keyword arguments:**
        
            * surface -- the surface the arrow will be drawn on
            * col -- the colour of the arrow
            * (x1,y1) -- coordinates of the beginning of the arrow
            * (x2,y2) -- coordinates of the end of the arrow
            
        Returns nothing; just draws the arrow."""
        pygame.draw.line(surface, col, (x1,y1), (x2,y2), 2)
        length = ((x1 - x2)**2 + (y1 - y2)**2)**0.5
        sin = abs((y1 - y2) / length)
        cos = abs((x1 - x2) / length)
        dirX = 1
        if x1 < x2:
            dirX = -1
        dirY = 1
        if y1 < y2:
            dirY = -1
        p1 = (x2 + dirX * (10 * cos), y2 + dirY * (10 * sin))
        p2 = (x2 + dirX * (18 * cos + 4 * sin), y2 + dirY * (18 * sin - 4 * cos))
        p3 = (x2 + dirX * (18 * cos - 4 * sin), y2 + dirY * (18 * sin + 4 * cos))
        pygame.draw.polygon(surface, col, [p1,p2,p3])
        
    def draw_graph(self,surface):
        """Listens for a new client, then attaches it as a new thread.
        
        **Keyword arguments:**
        
            * surface -- the surface the graph will be drawn on

        Returns nothing; just draws the graph."""
        surface.fill( (75,75,75) )
        
        for i in range(self.n):
            for (j,t) in self.edges[i]:
                self.draw_arrow(surface, self.colour(t), self.coords[i], self.coords[j])
                
        for c in self.coords:
            pygame.draw.circle(surface, (255,255,255), c, 10)
        pygame.draw.circle(surface, (0,255,255), self.coords[self.current], 10)
        pygame.display.flip()
        
    def read_graph_file(self,filename):
        """Reads a plaintext representation of the graph.
        
        **Keyword arguments:**
        
            * filename -- file to read from

        Class values are set to correspond to a new graph.
        File format (each value in a new line):
        
        NUMBER_OF_VERTICES :: int
        
        NUMBER_OF_VERTICES times:
        
            NAME_OF_VERTEX :: string
            
            X_COORDINATE_OF_VERTEX :: int
            
            Y_COORDINATE_OF_VERTEX :: int
            
        NUMBER_OF_EDGES :: int
        
        NUMBER_OF_EDGES times:
        
            EDGE_START_VERTEX :: int
            
            EDGE_END_VERTEX :: int
            
            EDGE_STEP_SIGN :: int -- 3 (UP), 4 (DOWN), 1 (LEFT), 2 (RIGHT)"""
    
        self.coords = []
        self.names = []
        self.edges = []
        f = open(filename,'r')
        self.n = int(f.readline())
        for i in range(self.n):
            name = f.readline()
            x = int(f.readline())
            y = int(f.readline())
            self.coords.append( (x,y) )
            self.names.append(name)
            self.edges.append([])
            
        m = int(f.readline())
        for it in range(m):
            i = int(f.readline())
            j = int(f.readline())
            t = int(f.readline())
            self.edges[i].append((j,t))
        
        f.close()
    
    def read_graph_pickle(self,str):
        """Read a pickled graph from a string (the string is provided by the server).
        
        **Keyword arguments:**
        
            * str -- a string containing a pickled graph

        Class values are set to correspond to a new graph."""
        g = pickle.loads(str)
        self.names = g.names
        self.edges = g.edges
        self.coords = g.coords
        self.n = g.n
        self.current = g.current
        
    def set_current(self, direction):
        """Makes a step in the graph.
        
        **Keyword arguments:**
        
            * direction -- one of [STOP, UP, DOWN, LEFT, RIGHT]
            
            """
        next_step = direction
        print next_step
        possible_next = filter(lambda (v,t): t == next_step, self.edges[self.current])
        if possible_next == []:
            return
        else:
            self.current = possible_next[0][0]

