##
# @file ModeTab.py
#
# @brief To define the option to select the device opertaing mode

# Imports
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
import commands
import packetProcess
import uartAPI
import utility
import globalvar
import logclass
import io
from io import StringIO

##
# @class ModeTab
# @brief To define the drop down menu option for the device mode selection and create a command with the selected option
#         Device will operate in two modes - Normal and Test mode
#         Flow measurement timing and the continuous data transmission will differ in two modes
class ModeTab():
    
    ## To deisgn the drop down menu with the device operating mode option
    def __init__(self, frame):
        self.ModeFrame = LabelFrame(frame,text='Operating Mode',height=15,width=100) 
        self.mode_B = Button(self.ModeFrame, text = "Send", command = self.SetOperatingMode).grid(row=2,column=7,padx=2,pady=5)
        self.ModeName = StringVar()
        self.ModeName.set('Select')
        self.Mode_list = ['Normal','Test']
        self.Mode_dropdown = OptionMenu(self.ModeFrame,self.ModeName,*self.Mode_list)
        self.Mode_dropdown.config (width = 7)
        self.Mode_dropdown.grid(row=2,column=1,padx=2, pady=2)
        self.ModeFrame.grid(row=2,column=8,columnspan =2,padx=2,pady=2,sticky = W)

    ##
    #  @brief To create and send the command depends upon the option selected in the drop down menu for the operating mode
    #  @param self The object pointer
    def SetOperatingMode(self):
        msg = io.StringIO()

        if(globalvar.is_port_available == 1 and globalvar.is_com_port_connected == 1):
            payload = []
            packet_in = []
            if 'Normal' == self.ModeName.get(): # to set the device in normal operating mode
                payload.append(commands.mode.MODE_NORMAL.value) 
                payload_len = 1; # payload length is one 
                cmd_ID = commands.config_cmd.OPERATING_MODE_CONFIG.value # command ID corresponds to operating mode
                packet_info = packetProcess.createPacket(cmd_ID,payload,payload_len) # to send the command
                msg.write('\nReq: Normal Mode : '+", ".join("0x{:02x}".format(num) for num in packet_info))
                packet_rcvd = uartAPI.uart_write_read(packet_info,5,5) # to receive the  response command from the device
                if(len(packet_rcvd) > 0):
                    msg.write('\nRsp: ACK: '+", ".join("0x{:02x}".format(num) for num in packet_rcvd))
                    if (packet_rcvd[2] == 0xFF): # to check for the error code in the response command
                        utility.checkresponse(packet_rcvd[3],msg)
                    else :
                        msg.write('\nDevice Mode is changed to Normal Mode')
                else:
                    msg.write('\nNO RESPONSE')

            elif 'Test' == self.ModeName.get(): # to set the device in test operating mode
                payload.append(commands.mode.MODE_TEST.value) 
                payload_len = 1; # payload length is one 
                cmd_ID = commands.config_cmd.OPERATING_MODE_CONFIG.value # command ID corresponds to operating mode
                packet_info = packetProcess.createPacket(cmd_ID,payload,payload_len) # to send the command
                msg.write('\nReq: Test Mode : '+", ".join("0x{:02x}".format(num) for num in packet_info))
                packet_rcvd = uartAPI.uart_write_read(packet_info,5,5) # to receive the  response command from the device
                if(len(packet_rcvd) > 0):
                    msg.write('\nRsp: ACK: '+", ".join("0x{:02x}".format(num) for num in packet_rcvd))
                    if (packet_rcvd[2] == 0xFF): # to check for the error code in the response command
                        utility.checkresponse(packet_rcvd[3],msg)
                    else :
                        msg.write('\nDevice Mode is changed to Test Mode')
                else:
                    msg.write('\nNO RESPONSE')

            else:
                msg.write('\nINVALID OPERATING MODE')
        else:
            msg.write('\nCOM Port is not available')
        
        logclass.logst(msg.getvalue())