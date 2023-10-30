##
# @file dataTxIntTab.py
#
# @brief To define the menu option and creating the commmands to modify the data transmission interval

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
# @class dataTxIntervalTab
# @brief To define the menu option to modify data TX interval
#        TX interval options are - 0, 2, 10, 30, 60, 300, 600, 1500, 3600 seconds
#        When user selects 0 as the interval - then no data will be send from the device
class dataTxIntervalTab():
    
    ## To create a drop down menu for the options of data txn interval
    def __init__(self, frame):
        self.txIntervalFrame = LabelFrame(frame,text='Tx Interval(Sec)',height=15,width=80) 
        self.txInterval_B = Button(self.txIntervalFrame, text = "Send", command = self.SettxInterval).grid(row=2,column=1,padx=2,pady=5)
        self.txInterval_val = StringVar()
        self.txInterval_val.set('Select ')
        self.txInterval_list = [0, 2, 10, 30, 60, 300, 600, 1500, 3600]  # menu with tx interval option in seconds
        self.txInterval_dropdown = OptionMenu(self.txIntervalFrame,self.txInterval_val,*self.txInterval_list)
        self.txInterval_dropdown.config (width = 5)
        self.txInterval_dropdown.grid(row=2,column=0,padx=2, pady=2)
        self.txIntervalFrame.grid(row=2,column=1,columnspan =2,padx=2,pady=2,sticky = W)

    ##
    #  @brief to send the commands when user selects the option and presses enter
    #  @param self The object pointer
    def SettxInterval(self):
        msg = io.StringIO()
        if(globalvar.is_port_available == 1 and globalvar.is_com_port_connected == 1):
            payload = []
            packet_in = []
            byte_val = self.txInterval_val.get() # to get the user selected interval from the menu option
            if(byte_val == 'Select '):
                msg.write('\nPlease select valid value from the option')
            else:
                payload = (re.findall("..",((utility.tohex((int(byte_val)),16)[2:].zfill(4)))))
                payload = [int(val,16) for val in payload]
                payload_len = 2; # payload length 
                cmd_ID = commands.config_cmd.DATA_REPORTING_INTERVAL_CONFIG.value # command ID coresponds to set the TX interval 
                packet_info = packetProcess.createPacket(cmd_ID,payload,payload_len) # to send the command ID
                msg.write('\nReq: TX Interval : '+", ".join("0x{:02x}".format(num) for num in packet_info))
                packet_rcvd = uartAPI.uart_write_read(packet_info,5,5) # to get the response from the device
                if(len(packet_rcvd) > 0):
                    msg.write('\nRsp: ACK: '+", ".join("0x{:02x}".format(num) for num in packet_rcvd))
                    if (packet_rcvd[2] == 0xFF): # to check for the error code in the response command
                        utility.checkresponse(packet_rcvd[3],msg)
                    else :
                        msg.write('\nTX Interval changed to {} seconds'.format(byte_val))
                else:
                    msg.write('\nNO RESPONSE')
        else:
            msg.write('\nCOM Port is not available')

        logclass.logst(msg.getvalue())