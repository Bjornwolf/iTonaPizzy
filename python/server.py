#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Data exchange hub."""

import socket
import threading
import cPickle as pickle
import time
import json
from graph import Graph
from select import select
from OSC import OSCClient, OSCMessage

clients = []
renderers = []
graphers = []
graph = []
current_state = 0
osc = OSCClient()
osc.connect( ("localhost", 31415) )
graph_file = 'graph_ex.pi'

def get_graph(graph):
    """Loads a pickled graph from a file.

    **Keyword arguments:**
        * graph -- file containing a pickled graph
    
    Returns an unpickled graph."""
    f = open(graph,'rb')
    return pickle.load(f)

def client_thread(c):
    """Handles the communication with a single client.

    **Keyword arguments:**
        * c -- communication channel
    
    Infinite loop; dies upon connection failure with the assigned client."""
    global clients
    global renderers
    global current_state
    global graphers
    global graph
    mode = "nc"
    ctr = 0
    while True:
        try:        
            x = c.recv(32768)
        except:
            return
        if mode == "nc":
            if x[0] == 'G':
                try:
                    c.send("G " + pickle.dumps(graph))
                except:
                    return
                mode = "g"
                graphers.append(c)
                print 'Grapher connected'

            elif x[0] == 'R':
                try:
                    c.send("OKK")
                except:
                    return
                mode = "r"
                renderers.append(c)
                print 'Renderer connected'

            elif x[0] == 'L':
                try:
                    c.send("OKK")
                except:
                    return
                mode = "l"
                print 'Learner connected'
        
        elif mode == "l":
        
            if x[0] == 'D':
                #print 'D',
                for sock in renderers:
                    try:
                        sock.send(x)
                    except:
                        pass
            else:
                print 'unknown packet', len(x)
            msg = OSCMessage()
            msg.setAddress("/user/1")
            msg.append(x[2:])
            try:
                osc.send( msg )
            except:
                pass

            (st,x1,x2) = pickle.loads(x[2:])
            print current_state, ctr
            if current_state != 0 and ctr == 150:
                print "SENDING C " + str(st)
                for sock in graphers:
                    try:
                        sock.send("C " + str(st))
                    except:
                        pass
            if current_state == st:
                ctr += 1
            else:
                ctr = 0
                current_state = st
            

def attach_clients(socket):
    """Listens for a new client, then attaches it as a new thread.

    **Keyword arguments:**
        * socket -- the socket to listen to
    
    Infinite loop."""
    global clients
    global renderers
    global graphers
    while True:
        c = socket.accept()
        print 'connection from', c[1]
        clients.append(c)
        threading.Thread(target = client_thread, args = [c[0]]).start()

    
def main(pickled_graph):
    global clients
    global renderers
    global graphers
    global graph

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host =  ''
    port = 31415          
    s.bind((host, port))
    graph = get_graph(pickled_graph)
    

    s.listen(5)
    t1 = threading.Thread(target=attach_clients, args = (s,))
    t1.start()
    
    

    print 'Server started'

    while True:
        time.sleep(1)
if __name__ == "__main__":
    main(graph_file)

         
