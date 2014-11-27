#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Receiving data from device, classification using SVM, data processing."""

emu = False          # TU WŁĄCZA SIĘ SYMULACJĘ EMOTIVA

import pygame
import gevent
import json
import socket
from select import select
import cPickle as pickle
import sys
from fft import *
import copy
import threading
from sklearn import svm


if emu:
    from emutiv import Emutiv as Emotiv
    import emotiv as emotiv
    import emutiv
    emutiv.fname = 'data/data4.txt'#'data/data5.txt'
else:
    from emotiv import Emotiv
    import emotiv
    
from depikelpowers import convert_to_pow

svm_name = 'svm_learner.pi'

tmp = {}
        
def count_fft(name, sensor, pow1, pow2):
    """Counts FFT of the signal to form a packet.

    **Keyword arguments:**
        * name -- name of the sensor
        * sensor -- sensor information from last packet
        * pow1 -- power of alpha band of the signal
        * pow2 -- power of beta band of the signal
    
    Returns nothing, it just sets the new data in a global structure."""
    global tmp
    global buffer
    fourier = stripes(map(lambda x: x.sensors[name]['value']*2.0,buffer[-128:]), 128)[1:]
                
    tmp[name] = (sensor['quality'],sensor['value'],fourier,pow1,pow2)
    


def main():
    global tmp
    global buffer
    connected = False
    pygame.init()                                            # Inicjowanie okna
    screen = pygame.display.set_mode((500,500))              
    
    emotiv = Emotiv(displayOutput=False)                     # Inicjowanie urządzenia Emotiv EPOC
    gevent.spawn(emotiv.setup)
    gevent.sleep(1)
    
    # +-----------------------------------
    # | Przygotowanie serwera
    # +-----------------------------------
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = 'localhost'
    port = 31415
    try:
        s.connect((host, port))
        
        s.send('LEARNER')
        x = s.recv(32768)
        if x == 'OKK':
            connected = True
            print 'Server connection established.'
        else:
            print 'One does not simply connect to a server.'
    except:
        print 'Server down or network error.'

    
    
    # +-----------------------------------
    # | Przygotowanie SVM
    # +-----------------------------------
    
    clf = svm.NuSVC(probability = True, kernel = 'rbf', cache_size = 1000, nu=0.01, tol=1e-6, degree=15,gamma=3.8614739171)    # Inicjowanie klasyfikatora SVM
            
    
    sample_time = 0.738877918824
    learn_time = 8.0
    
    
    learn_ticks = int(128.0*learn_time)
    
    left_data = []
    calm_data = []
    right_data = [] 
    
    pow = [0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    buffer = []
    cnt = 0
    timestamp = 0
    fourier = [0]
    
    font = pygame.font.SysFont('Arial',24)
    dir_color = [(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0)]
    
    txt_ready = font.render('GET READY',1,(0,255,0))
    txt_calm = font.render('CALM',1,(255,255,255))
    txt_left = font.render('LEFT',1,(255,255,255))
    txt_right = font.render('RIGHT',1,(255,255,255))
    txt_done = font.render('DONE',1,(0,255,255))
    txt_3 = font.render('3',1,(255,255,0))
    txt_2 = font.render('2',1,(255,255,0))
    txt_1 = font.render('1',1,(255,255,0))

    
    # +-----------------------------------
    # | Stan:
    # | 0 - przed uruchomieniem, wcisnąć -spację- aby przejść dalej
    # | 1 - odliczanie
    # | 2 - uczenie środek
    # | 3 - odliczanie
    # | 4 - uczenie lewo
    # | 5 - odliczanie
    # | 6 - uczenie prawo
    # | 7 - nauczono
    # +-----------------------------------  
    state = 0
    dir = 0
    battery = 0
    
    
    while True:
        # +-----------------------------------
        # | Wykrywanie zdarzeń (wciśnięcia klawiszy)
        # +-----------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                s.close()
                pygame.display.quit()
                emotiv.close()
                return
            if (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_ESCAPE):      # escape wyłącza program
                    s.close()
                    pygame.display.quit()
                    emotiv.close()
                    return
                if (event.key == pygame.K_SPACE):       # spacja rozpoczyna proces uczenia 
                    if state == 0: 
                        state = 1
                        timestamp = cnt
                    elif state == 7:
                        pygame.display.quit()
                        emotiv.close()
                        return
                        
                if (event.key == pygame.K_l):           # l pozwala załadować wcześniej wyuczony klasyfikator
                    file = open(svm_name,'rb')
                    clf = pickle.load(file)
                    file.close()
                    state = 8
        
        # +-----------------------------------
        # | Odczyt EEG
        # +-----------------------------------  
        
        packet = emotiv.dequeue()
        
        #while not emotiv.empty(): emotiv.dequeue()
        
        cnt += 1
        
        if emotiv.empty():
            buffer.append(copy.deepcopy(packet))
        else:
            buffer.append(packet)
         
        if cnt > 129.0 * learn_time: del buffer[0]
        
        
        battery = int(max(map(lambda x:x.battery_percent(), buffer)))
        
        # +-----------------------------------
        # | Przygotowanie pakietu do wysłania
        # +-----------------------------------
        
        if connected:
            tmp = {}
            for (i,name) in enumerate(emotiv.channels):
                count_fft(name, packet.sensors[name], float(pow[2*i]),float(pow[2*i+1]))
            
            out = pickle.dumps((dir,battery,tmp))
            a =s.send(b'D ' + out)
            
        # +-----------------------------------
        # | Rysowanie
        # +-----------------------------------    
        sx = 250
        sy = 200
        
        screen.fill((75, 75, 75))
        
        pygame.draw.circle(screen,dir_color[0],(sx,sy),10)
        
        pygame.draw.line(screen,dir_color[1],(sx-80,sy),(sx-20,sy-5),3)
        pygame.draw.line(screen,dir_color[1],(sx-80,sy),(sx-20,sy+5),3)
        
        pygame.draw.line(screen,dir_color[2],(sx+80,sy),(sx+20,sy-5),3)
        pygame.draw.line(screen,dir_color[2],(sx+80,sy),(sx+20,sy+5),3)
        
        pygame.draw.line(screen,dir_color[3],(sx,sy+80),(sx-5,sy+20),3)
        pygame.draw.line(screen,dir_color[3],(sx,sy+80),(sx+5,sy+20),3)
        
        pygame.draw.line(screen,dir_color[4],(sx,sy-80),(sx-5,sy-20),3)
        pygame.draw.line(screen,dir_color[4],(sx,sy-80),(sx+5,sy-20),3)
        
        
        
        # +-----------------------------------
        # | The Finite State Machine
        # +-----------------------------------    
        if state == 0:                          # Wyświetlanie napisu po uruchomieniu
            screen.blit(txt_ready, (200,400))
        elif state in [1,3,5]:
            dir_color = [(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0)]
            if cnt-timestamp > 128:
                if cnt-timestamp > 256:
                    if cnt-timestamp > 384:
                        state += 1
                        timestamp = cnt
                    else:
                        screen.blit(txt_1, (250,400))
                else:
                    screen.blit(txt_2, (250,400))
            else:
                screen.blit(txt_3, (250,400))
        elif state == 2:                    # uczenie się pozostania w miejscu
            if cnt-timestamp < learn_ticks:
                screen.blit(txt_calm, (200,400))
                dir_color = [(255,255,255),(0,0,0),(0,0,0),(0,0,0),(0,0,0)]
            else:
                state = 3
                timestamp = cnt
                calm_data = convert_to_pow(buffer[-int(128.0*learn_time):],sample_time)
                
                cf = open('cf.txt','wb')
                pickle.dump(buffer[-int(128.0*learn_time):],cf)
                cf.close()
        elif state == 4:                # uczenie się ruchu w lewo
            if cnt-timestamp < learn_ticks:
                screen.blit(txt_left, (200,400))
                dir_color = [(0,0,0),(255,255,255),(0,0,0),(0,0,0),(0,0,0)]
            else:
                state = 5
                timestamp = cnt
                left_data = convert_to_pow(buffer[-int(128.0*learn_time):],sample_time)
                print len(buffer[-int(128.0*learn_time):])
                
                lf = open('lf.txt','wb')
                pickle.dump(buffer[-int(128.0*learn_time):],lf)
                lf.close()
                
        elif state == 6:            # uczenie się ruchu w prawo
            if cnt-timestamp < learn_ticks:
                screen.blit(txt_right, (200,400))
                dir_color = [(0,0,0),(0,0,0),(255,255,255),(0,0,0),(0,0,0)]
            else:
                state = 7
                timestamp = cnt
                right_data = convert_to_pow(buffer[-int(128.0*learn_time):],sample_time)
                
                rf = open('rf.txt','wb')
                pickle.dump(buffer[-int(128.0*learn_time):],rf)
                rf.close()
        
        elif state == 7:            # przygotowywanie svma
            dir_color = [(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0)]
            
            print 'l',len(left_data),len(right_data),len(calm_data)
            y = [0] * len(calm_data) + [1] * len(left_data) + [2] * len(right_data)
            
            clf.fit(calm_data+left_data+right_data,y)
            
            
            file = open(svm_name,'wb')
            pickle.dump(clf,file)
            file.close()
            tmestamp = cnt
            
            state = 8
            
        elif state == 8:            # wyświetlanie klasyfikacji
            screen.blit(txt_done, (200,400))
            if cnt-timestamp > sample_time*128.0:
                timestamp = cnt
                pow = convert_to_pow(buffer[-int(128.0*sample_time):],sample_time)[-1]
                dir = int(clf.predict(pow))
                print clf.predict_proba(convert_to_pow(buffer[-int(128.0*sample_time):],sample_time)[-1])
                
                if dir == 0:
                    dir_color = [(255,255,255),(0,0,0),(0,0,0),(0,0,0),(0,0,0)]
                if dir == 1:
                    dir_color = [(0,0,0),(255,255,255),(0,0,0),(0,0,0),(0,0,0)]
                if dir == 2:
                    dir_color = [(0,0,0),(0,0,0),(255,255,255),(0,0,0),(0,0,0)]
                    

            
        pygame.display.flip()
        
        
if __name__ == "__main__":
    main()
