#!/usr/bin/python
# -*- coding: utf-8 -*-

"""The class that represents a cell automaton."""

import pygame
class CellAutomaton(object):
    def __init__(self, (x,y), cells, rules, max_state):
        """Assigns a colour to the node.
        
        **Keyword arguments:**
            * (x,y) -- horizontal and vertical size of the cell block
            * cells -- a list of lists (rows) of (STATE, RULESET) describing the starting state of the cells
            * rules -- list of functions describing the change of states
            * max_state -- highest state number

        Returns a triple RGB."""
        self.x = x
        self.y = y
        self.cells = cells # [[(state, ruleset)]]
        self.rules = rules
        self.max_state = max_state

    def next_state(self):
        """Switches the automaton to the next state."""
        neighs = []
        for j in range(self.y):
            t_neighs = [self.neighbourhood(i,j) for i in range(self.x)]
            neighs.append(t_neighs)
        for j in range(self.y):
            for i in range(self.x):
                (state, ruleset) = self.cells[j][i]
                self.cells[j][i] = (self.rules[ruleset](state,neighs[j][i]),ruleset)

        
    def neighbourhood(self,i,j):    
        """Collects data about neighbours of a given cell.
        
        **Keyword arguments:**
            * i -- X coordinate (int)
            * j -- Y coordinate (int)
            
        Returns a list of occurences of states."""
        v =  map(lambda x: x[max(i-1,0):i+2],self.cells[max(j-1,0):j+2])
        x = self.x
        y = self.y
        if i == 0 and j == 0:
            v = [v[0][1]] + v[1]
        elif i == 0 and j == y - 1:
            v = v[0] + [v[1][1]]
        elif i == 0:
            v = v[0] + [v[1][1]] + v[2]
        elif i == x - 1 and j == 0:
            v = [v[0][0]] + v[1]
        elif i == x - 1 and j == y - 1:
            v = v[0] + [v[1][0]]
        elif i == x - 1:
            v = v[0] + [v[1][0]] + v[2]
        elif j == 0:
            v = [v[0][0], v[0][2]] + v[1]
        elif j == y - 1:
            v = v[0] + [v[1][0], v[1][2]]
        else:
            v = v[0] + [v[1][0], v[1][2]] + v[2]

        ct = [0 for i in range(self.max_state + 1)]
        for (e,r) in v:
            ct[e] += 1
        return ct
    
    def draw(self, surface):
        """Draws the current state on the surface.
        
        **Keyword arguments:**
            * surface -- a pygame surface to draw the cells on

        Returns nothing."""
        brightness = [255.0 * i/self.max_state for i in range(self.max_state + 1)]
        for j in range(self.y):
            for i in range(self.x):
                c = brightness[self.cells[j][i][0]]
                pygame.draw.rect(surface, (c,c,c), (10 * i, 10 * j, 10, 10))

