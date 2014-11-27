#!/usr/bin/python
# -*- coding: utf-8 -*-

from Tkinter import *
import threading
import gevent
import socket
import copy
import cPickle as pickle
from time import sleep
import tkMessageBox

emu = True

if emu:
    from emutiv import Emutiv as Emotiv
    import emotiv as emotiv
    import emutiv
    emutiv.fname = '../data/data4.txt'
else:
    from emotiv import Emotiv
    import emotiv
   
alive = True
    
prev = 0
cnt = 0
rcnt = 0
rtime = 0
buff = []

record = False



def updateFunction(app):
    global cnt, prev, alive, rcnt, alive, rtime
    tmp = []
    while alive:
        app.setCount(cnt)
        app.setRec(rcnt)
        tmp.append(cnt-prev)
        
        if len(tmp)==10:
            app.setPPS(reduce(lambda x,y: x+y, tmp))
            app.setTime(rtime)
            del tmp[0]    
            
        prev = cnt
        if record: rtime += 0.1
        
        sleep(0.1)
    
def emotivFunction():
    global cnt, buff, rcnt, alive, record, alive
    
    emotiv = Emotiv(displayOutput=False)
    gevent.spawn(emotiv.setup)
    gevent.sleep(0.5)
    
    while alive:
        
        packet = emotiv.dequeue()
        cnt += 1
        if(record):
            buff.append(copy.deepcopy(packet))
            rcnt += 1
     
    
class App(Frame):
    def __start(self):
        global record
        record = True
        
    def __stop(self):
        global record
        record = False
        
    def __clear(self):
        global buff,rcnt,rtime
        buff = []
        rcnt = 0
        rtime = 0
        
    def __save(self):
        global buff,rcnt,rtime
        try:
            file = open(self.inputEntry.get(),'wb')
            pickle.dump(buff,file)
            file.close()
            tkMessageBox.showinfo("Saved",str(rcnt)+' packets ('+str(rtime)+'s) saved to '+self.inputEntry.get()+'.')
        except:
            tkMessageBox.showerror("Error","Unknown error.")
        
        
    def createWidgets(self):
        self.buttonFrame = Frame(self)
        self.inputFrame = Frame(self)
        self.infoFrame = Frame(self)
        self.dataFrame = Frame(self)
        
        # -- buttonFrame: -- 
        self.startButton = Button(self.buttonFrame, text='Start', command=self.__start)
        self.stopButton = Button(self.buttonFrame, text='Stop', command=self.__stop)
        self.clearButton = Button(self.buttonFrame, text='Clear', command=self.__clear)
        self.saveButton = Button(self.buttonFrame, text='Save', command=self.__save)
        self.exitButton = Button(self.buttonFrame, text='Exit', command=self.quit)
        
        self.startButton.pack(padx=10, side=LEFT)
        self.stopButton.pack(padx=10, side=LEFT)
        self.clearButton.pack(padx=10, side=LEFT)
        self.saveButton.pack(padx=10, side=LEFT)
        self.exitButton.pack(padx=10, side=RIGHT)
        
        self.buttonFrame.pack(padx=10, pady=10, fill=X, side=BOTTOM)
        
        
        # -- inputFrame: -- 
        self.inputLabel = Label(self.inputFrame, text='File name:')
        self.inputEntry = Entry(self.inputFrame)
        self.inputEntry.insert(0,'tmp.txt')
        
        self.inputLabel.pack(side=TOP, anchor=W)
        self.inputEntry.pack(fill=X)
        
        self.inputFrame.pack(padx=10, pady=10, fill=X, side=TOP)
        
        # -- infoFrame: --
        self.countLabel = Label(self.infoFrame, text='Packet count: 0')
        self.ppsLabel = Label(self.infoFrame, text='Packets/second: 0')
               
        self.countLabel.pack(anchor=W,padx=20)
        self.ppsLabel.pack(anchor=W,padx=20)
        
        self.infoFrame.pack(padx=10, pady=10, fill=BOTH, expand=NO, side=LEFT)
        
        # -- dataFrame: --
        self.recordLabel = Label(self.dataFrame, text='Recorded packets: 0')
        self.timeLabel = Label(self.dataFrame, text='Recording time: 0s')
        
        self.recordLabel.pack(anchor=W,padx=20)
        self.timeLabel.pack(anchor=W,padx=20)
        
        self.dataFrame.pack(padx=10, pady=10, fill=BOTH, side=LEFT)
        
    def setCount(self, count):
        self.countLabel['text'] = 'Packet count: '+str(count)
        
    def setPPS(self, pps):
        self.ppsLabel['text'] = 'Packets/second: '+str(pps)
        
    def setRec(self, cnt):
        self.recordLabel['text'] = 'Recorded packets: '+str(cnt)
        
    def setTime(self, time):
        self.timeLabel['text'] = 'Recording time: '+str(time)+'s'
        
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack(fill=BOTH)
        self.createWidgets()
    
if __name__ == '__main__':

    root = Tk()
    root.resizable(0,0)
    app = App(master=root)
    app.master.title("Recorder")
    
    t1 = threading.Thread(target=emotivFunction)
    t2 = threading.Thread(target=updateFunction, args=(app,))
    
    t1.start()
    t2.start()
    
    app.mainloop()
        
    alive = False
    
    try:
        root.destroy()
    except:
        pass
    
    
