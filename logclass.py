from tkinter import *
import tkinter.ttk as ttk
from datetime import datetime
import globalvar


class debuglog():
    def __init__(self,frame):
        # Init the main GUI window
        self.debuglog = LabelFrame(frame,text = "Log",height=15,width=100)
        self.log      = Text(self.debuglog,height = 15, width = 80, bg = "white" , fg = "black")
        globalvar.text_log = self.log
        self.scrollb  = Scrollbar(self.debuglog, orient=VERTICAL)
        self.scrollb.config(command = self.log.yview) 
        self.log.config(yscrollcommand = self.scrollb.set)
        # Grid & Pack
        self.log.grid(column=0, row=0)
        self.scrollb.grid(column=1, row=0, sticky=W)
        self.debuglog.pack()


def logst(msg):
        # Write on GUI
        globalvar.text_log.insert('end', msg + '\n')
        globalvar.text_log.see('end')