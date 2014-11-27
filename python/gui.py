#!/usr/bin/python
# -*- coding: utf-8 -*-

# Experimental GUI for emokit

from Tkinter import *
from os import walk

alive = True

class Application(Frame):
    def say_hi(self):
        print "hi there, everyone!"
        
    def list(self):
        print map(int, self.filelist.curselection())
        
    def getDataFiles(self):
        f = []
        for (dirpath, dirnames, filenames) in walk('../data/'):
            f.extend(filter(lambda x:x[-4:]=='.txt',filenames))
            break
        return f

    def createWidgets(self):
        self.listFrame = Frame(self)
        self.rightFrame = Frame(self)
        self.methodFrame = Frame(self.rightFrame)
        
        # -- listFrame -- 
        self.listlabel = Label(self.listFrame,text='Select files:')
        self.scrollbar1 = Scrollbar(self.listFrame)
        self.filelist = Listbox(self.listFrame, selectmode=MULTIPLE, yscrollcommand=self.scrollbar1.set)
        self.scrollbar1.config(command=self.filelist.yview)
        for file in self.getDataFiles():
            self.filelist.insert(END,file)
        
        self.listlabel.pack(side=TOP)
        self.filelist.pack(side=LEFT, fill=BOTH, expand=YES)
        self.scrollbar1.pack(anchor=E, fill=Y, expand=YES)
        
        self.listFrame.pack(expand=NO,padx=10, pady=10, fill=BOTH, side=LEFT, anchor=W)
        
        # -- methodFrame -- 
        self.methodLabel = Label(self.methodFrame, text='Select method:')
        
        self.methodLabel.pack(side=TOP, anchor=W)
        
        self.methodSelect = StringVar()
        self.methodSelect.set('ab')
        
        for text,mode in [('FFT','fft'),('Hjorth','hj'),('Alpha/Beta','ab'),('D1','d1'),('E1','e1')]:
            b = Radiobutton(self.methodFrame, text=text, value=mode, variable=self.methodSelect)
            b.pack(anchor=W, side=TOP)
        
        
        self.methodFrame.pack(expand=YES, fill=BOTH, side=LEFT, anchor=E)
        
        self.rightFrame.pack(expand=YES, padx=10, pady=10, fill=BOTH, side=RIGHT)
        
        
        
        
        # -- rest --
        self.itemsButton = Button(self, text="List selected items", command=self.list)

        self.hi_there = Label(self)
        self.hi_there["text"] = "Hello",
        
        
        self.QUIT = Button(self, text='Exit', command=self.quit)
        
        
        
        #self.itemsButton.pack({"side": "left"})
        #self.QUIT.pack({"side": "right"})
        #self.hi_there.pack({"side": "left"})
        

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack(fill=BOTH, expand=1)
        self.createWidgets()

if __name__ == '__main__':
    root = Tk()
    app = Application(master=root)
    app.master.title("Data Explorer 1")
    app.mainloop()
    
    alive = False
    try:
        root.destroy()
    except:
        pass