##
# @file baudrateTab.py
#
# @brief To define the menu option to modify the baudrate in the device

# Imports
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
import commands
import packetProcess
import uartAPI
import globalvar
import logclass
import io
from io import StringIO

##
# @class baudrateTab
#
# @brief Class that contains the options to select the baudrate and creating command for that 
#        Baud rate option of 9600, 19200, 38400, 56000, 57600 will be available.
#        User needs to select the baud rate in the drop down menu and press enter to send the command
class baudrateTab():
    
    ## to define the baudrate drop down option in the tool
    def __init__(self, frame):
        self.badurateFrame = LabelFrame(frame,text='Baud Rate',height=15,width=100) 
        self.baudrate_B = Button(self.badurateFrame, text = "Send", command = self.SetBaudrate).grid(row=2,column=5,padx=2,pady=5)
        self.baud_val = StringVar()
        self.baud_val.set('Select ')
        self.baudrate_list = [9600, 19200, 38400, 56000, 57600]
        self.baudrate_dropdown = OptionMenu(self.badurateFrame,self.baud_val,*self.baudrate_list)
        self.baudrate_dropdown.config (width = 7)
        self.baudrate_dropdown.grid(row=2,column=1,padx=2, pady=2)
        self.badurateFrame.grid(row=2,column=5,columnspan =2,padx=2,pady=2,sticky = W)

    ## 
    #  @brief define to send a command with the selected baud rate to the device
    #  @param self The object pointer
    def SetBaudrate(self):
        msg = io.StringIO()
        if(globalvar.is_port_available == 1 and globalvar.is_com_port_connected == 1):
            payload = []
            packet_in = []
            byte_val = self.baud_val.get()
            if(byte_val == 'Select '):
                msg.write('\nPlease select valid value from the option')
            else:
                if byte_val == '9600':
                    payload.append(commands.baudrate.BAUD_9600.value) 
                elif byte_val == '19200':
                    payload.append(commands.baudrate.BAUD_19200.value)
                elif byte_val == '38400':
                    payload.append(commands.baudrate.BAUD_38400.value) 
                elif byte_val == '56000':
                    payload.append(commands.baudrate.BAUD_56000.value)
                elif byte_val == '57600':
                    payload.append(commands.baudrate.BAUD_57600.value)
                else:
                    msg.write('\nINVALID BAUDRATE COMMAND')
                payload_len = 1; # payload length is always one for the baud rae config command
                cmd_ID = commands.config_cmd.UART_BAUD_RATE_CONFIG.value # to append the command ID
                packet_info = packetProcess.createPacket(cmd_ID,payload,payload_len) # to send the command
                msg.write('\nReq: BD_Value : '+", ".join("0x{:02x}".format(num) for num in packet_info))
                packet_rcvd = uartAPI.uart_write_read(packet_info,5,5) # to receive the response command
                if(len(packet_rcvd) > 0):
                    msg.write('\nRsp: ACK: '+", ".join("0x{:02x}".format(num) for num in packet_rcvd))
                    if (packet_rcvd[2] == 0xFF): # if the command ID is xFF  in the response then there is some error in the command
                        utility.checkresponse(packet_rcvd[3],msg)
                    else :
                        msg.write('\nBaud rate changed to {}'.format(byte_val))
                else:
                    msg.write('\nNO RESPONSE')
        else:
            msg.write('\nCOM Port is not available')
        
        logclass.logst(msg.getvalue())
