#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Displaying the charts and the state of the device."""

import pygame
from pygame import FULLSCREEN
import cPickle as pickle
import sys
import os.path
import socket
import select
import json


black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)
orange = (255,165,0)
    
host = 'localhost'
port = 31415 
    
def draw_arrows(surface, colours):
    """Listens for a new client, then attaches it as a new thread.

    **Keyword arguments:**
        * surface -- the surface the arrows will be drawn on
        * colours -- list of (R,G,B) values (length: at least 3)
    
    Returns nothing; just draws the arrows."""
    pygame.draw.circle(surface, colours[0], (1300,700), 10)
    pygame.draw.line(surface, colours[1], (1220,700), (1280,695), 3)
    pygame.draw.line(surface, colours[1], (1220,700), (1280,705), 3)
    pygame.draw.line(surface, colours[2], (1380,700), (1320,695), 3)
    pygame.draw.line(surface, colours[2], (1380,700), (1320,705), 3)
        
class Grapher(object):
    """The chart and FFT drawer corresponding to one of the sensors."""
    def __init__(self, screen, name, i, sensor_position):
        """Constructs the Grapher object.
    
        **Keyword arguments:**
            * screen -- the surface the charts will be drawn on
            * name -- the name of the sensor
            * i -- determines the position on the screen
            * sensor_position -- where the conductivity will be displayed"""
        self.screen = screen
        self.name = name
        self.xoff = 40  
        
        self.y = i * gheight
        self.buffer = []
        font = pygame.font.Font(None, 24)
        self.text = font.render(self.name, 1, red)
        self.text2 = font.render(self.name, 1, white)
        self.textpos = self.text.get_rect()
        self.textpos.centery = self.y + gheight * 2
        self.color = white
        (self.hx,self.hy) = sensor_position
        self.fourier = []
    
    def assign_color(self,quality):
        """Assigns colour according to the quality.
    
        **Keyword arguments:**
            * quality -- integer value
        Returns a triple of RGB values."""
        if quality >= 8: return green
        if quality >= 5: return yellow
        if quality >= 3: return orange
        if quality > 0: return red
        return black
    
    def update(self, new_data): #(quality, value, stripes, alpha, beta)
        """Assigns colour according to the quality.
    
        **Keyword arguments:**
            * new_data -- data packet"""
        (quality, value, fourier, alpha, beta) = new_data[self.name]
        if len(self.buffer) == 800 - self.xoff: # cleaning the least recent record
            self.buffer = self.buffer[1:]
        value *= 2.0 # WTF
        self.buffer.append(self.calcY(value) + self.y)
        self.fourier = fourier
        self.alpha = alpha
        self.beta = beta
        self.color = self.assign_color(quality)
        
    def calcY(self, val):
        """TODO"""
        return int(2 * gheight * val / float(1 << 13) - 2 * gheight)
         
    def draw_chart(self):
        """Draws a value chart."""
        self.screen.blit(self.text, self.textpos)
        xs = [self.xoff + i for i in range(len(self.buffer))]
        pygame.draw.lines(self.screen, self.color, False, zip(xs,self.buffer))
        
    def draw_fourier(self, x):
        """Draws FFT stripes.
    
        **Keyword arguments:**
            * x -- horizontal coordinate of the beginning
        Returns a new horizontal coordinate right of the stripes."""
        max_stripes = max(self.fourier)
        for num in self.fourier:
            stripe_bot = self.y + 2 * gheight
            stripe_height = num * (gheight / (2 * max_stripes + 1e-8))
            pygame.draw.line(self.screen, (255,0,0), (x, stripe_bot), (x, stripe_bot - stripe_height))
            x += 3
        return x
    
    def draw_alphabeta(self, x):
        """Draws alpha and beta power levels.
    
        **Keyword arguments:**
            * x -- horizontal coordinate of the beginning
        Returns a new horizontal coordinate right of the power levels."""
        for wave in [self.alpha, self.beta]:
            pygame.draw.line (self.screen, (0,255,0), (x, self.y + 2 * gheight), (x, self.y + 2 * gheight - wave * 50.0))
            x += 3
        return x

    def draw_head(self):
        """Draws a battery level and sensor position."""
        pygame.draw.circle(self.screen, self.color, (self.hx,self.hy), 10)
        self.screen.blit(self.text2, (self.hx-13,self.hy-30))
        
    def draw(self):
        """Draws all components."""
        if len(self.buffer) < 2:
            return   
        self.draw_chart()
        x = 800 + self.xoff
        if self.fourier != []: x = self.draw_fourier(x) + 10
        x = self.draw_alphabeta(x)
        self.draw_head()             

def draw_battery(screen,val):
    """Draws the battery meter
    **Keyword arguments:**
        * screen -- the surface the battery level will be drawn on
        * val -- a number from 0 to 100
    
    Returns nothing; just draws the battery level."""
    font = pygame.font.Font(None, 24)
    text = font.render('Battery: '+str(val)+'%', 1, green)
    screen.blit(text, (100,10))
        
    
    
        
def main(debug=False):
    global gheight
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.send("RENDER")
    if s.recv(65536) != 'OKK':
        print 'Server error'
        return
    else:
        print 'Server connection established'
    #s.setblocking(0)
    pygame.init()
    res = (1600, 900)
    screen = pygame.display.set_mode(res)
    graphers = []
    updated = False
    dir_color = [black, black, black]
    sensorPos = {
        'AF3': (1136, 76),
        'F3': (1166, 120),
        'F7': (1093, 126),
        'FC5': (1120, 157),
        'T7': (1076, 200),
        'P7': (1122, 299),
        'O1': (1163, 347),
        'AF4': (1264, 76),
        'F4': (1234, 120),
        'F8': (1307, 126),
        'FC6': (1280, 157),
        'T8': (1324, 200),
        'P8': (1278, 299),
        'O2': (1237, 347)}
    for name in 'AF3 F7 F3 FC5 T7 P7 O1 O2 P8 T8 FC6 F4 F8 AF4'.split(' '):
        graphers.append(Grapher(screen, name, len(graphers), sensorPos[name]))
    fullscreen = False

    while True:
        #sock = []
        #sock, [], [] = select.select([s],[],[],60)
        #if sock[0] != s:
        #    continue
            
        data_block = s.recv(32768)
        while data_block[0] != b'D':
            print 'kulawy',len(data_block)
            data_block = s.recv(32768)
        data_block = data_block[2:]
        #print 'received'+str(len(data_block))
        try:
            unpacked_data = pickle.loads(data_block)
        except:
            continue
        # (state, battery, [(quality, value, stripes, alpha, beta)])
        (state, battery, sensors) = unpacked_data
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                s.close()
                pygame.display.quit()
                return
            if (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_ESCAPE):
                    s.close()
                    pygame.display.quit()
                    return
                elif (event.key == pygame.K_f):
                    if fullscreen: screen = pygame.display.set_mode(res)
                    else: screen = pygame.display.set_mode(res, FULLSCREEN, 16)
                    fullscreen =  not fullscren  
        for i in range(len(graphers)):
            graphers[i].update(sensors)
        
        screen.fill( (75, 75, 75) )
        draw_battery(screen,battery)
        map(lambda x: x.draw(), graphers)
        dir_color[state] = white
        draw_arrows(screen, dir_color)
        dir_color[state] = black              
        pygame.display.flip()


gheight = 600 / 14+15
hgheight = gheight >> 1
if __name__ == "__main__":
    main(*sys.argv[1:])

