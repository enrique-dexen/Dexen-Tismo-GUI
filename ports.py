##
# @file ports.py
#
# @brief To implement the options to select the COM port and baudrate to connect to the device

# Imports
from tkinter import *
import uartAPI
import commands
import packetProcess
import logclass
import globalvar
import serial.tools.list_ports

##
# @class comports
# @brief To define the option to select the COM port of the device and the baudrate
#        Once the port and baudrate is selected , option to connec with the device is given 
class comports():
    ## To design the option with port and baud rate selection
    def __init__(self, frame):
        self.comportFrame = LabelFrame(frame,text = 'COM Port Selection',height=15,width=100) 
        self.infobutton = Button(self.comportFrame, text = 'Connect', command = self.portConnect).grid(row=0,column=2,padx=2,pady=5)
        self.infobutton = Button(self.comportFrame, text = 'DisConnect', command = self.portDisConnect).grid(row=0,column=3,padx=2,pady=5)
        self.portName = StringVar()
        self.baudrate = StringVar()
        self.portName.set('PORT')
        self.baudrate.set('BD')
        self.portName_list = self.getPorts()
        if(globalvar.is_port_available == 1):
            self.portName_dropdown = OptionMenu(self.comportFrame,self.portName,*self.portName_list)
        else:
            self.portName_dropdown = OptionMenu(self.comportFrame,self.portName,"NO PORTS")
        self.portName_dropdown.config (width = 7)
        self.portName_dropdown.grid(row=0,column=0,padx=2, pady=2)
        self.baudrate_val = [9600, 19200, 38400, 56000, 57600]
        self.baudrate_dropdown = OptionMenu(self.comportFrame,self.baudrate,*self.baudrate_val)
        self.baudrate_dropdown.config (width = 10)
        self.baudrate_dropdown.grid(row=0,column=1,padx=2, pady=2)
       
        self.comportFrame.grid(row=0,column=0,columnspan=4,padx=2,pady=2,sticky = NW)

    ##
    #  @brief To get the available ports in the device and show the options in the drop down menu
    #  @param self The object pointer
    def getPorts(self):
        ports = serial.tools.list_ports.comports()
        available_ports = []
        if(len(ports) > 0):
            globalvar.is_port_available = 1
            for p in ports:
                available_ports.append(p.device)  # to get the available ports in the device
        else:
            logclass.logst('\nCOM Ports are not available in the system')
        return available_ports

    ##
    #  @brief To connect with the selected port and the baudrate
    #  @param self The object pointer
    def portConnect(self):
        if(globalvar.is_port_available == 1):
            payload = []
            payload.append(16)
            port = self.portName.get() # to get the selected port
            baud = self.baudrate.get() # to get the selected baud rate
            logclass.logst('\nSelect Port Config : PORT {} BD: {}'.format(port,baud))
            uartAPI.setBaudrate(baud)   # to connect to the port
            uartAPI.connectPort(port)   # to connect to the baud rate
            uartAPI.uart_write(payload)
        else:
            logclass.logst('\nNo Ports are available to connect')

    ##
    #  @brief To get disconnected with the baudrate
    #  @param self The object pointer
    def portDisConnect(self):
        if(globalvar.is_port_available == 1):
            logclass.logst('\nCOM port Disconnected')
            uartAPI.disConnectPort()
        else:
            logclass.logst('\nNo Ports are available to disconnect')