from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
import uartAPI
import commands
import packetProcess
import utility
import globalvar
import logclass
import io
from io import StringIO

##
# @class configreadTab
# @brief To define the options to read calibration and configuration from device
#        Calibration - to read out the calibration data stored in the device
#        configuration - to read out the device configuration from the device
class gasCompTab():
    
    ## to define the drop down menu with configuration and calibration read out commands
    def __init__(self, frame):
        self.gasCompFrame = LabelFrame(frame,text = 'Gas Measurement time',height=15,width=50) 
        self.gasComp_txt = Message(self.gasCompFrame, text="min", relief=FLAT ).grid(row=4,column=2,padx=2,pady=5)
        self.gasComp_B = Button(self.gasCompFrame, text = "Send", command = self.setgascompttime).grid(row=4,column=4,padx=2,pady=5)
        self.ConfigValueEntry = Entry(self.gasCompFrame, width = 12)
        self.ConfigValueEntry.configure(state = 'normal')
        self.ConfigValueEntry.grid(row=4,column=1,padx=4,pady=5)
        self.gasCompFrame.grid(row=4,column=5,columnspan =2,padx=2,pady=2,sticky = W)

    def setgascompttime(self):
        msg = io.StringIO()
        if(globalvar.is_port_available == 1 and globalvar.is_com_port_connected == 1):
            payload = []
            byte_val = self.ConfigValueEntry.get() # to get the user selected interval from the menu option
            #if((int(byte_val) <= 0)):
            if((int(byte_val) < 1) or (int(byte_val) > 1440)):
                msg.write('\nInvalid input ')
            else:
                payload = (re.findall("..",((utility.tohex((int(byte_val)),16)[2:].zfill(4)))))
                payload = [int(val,16) for val in payload]
                payload_len = 2 # payload length 
                cmd_ID = commands.config_cmd.GAS_CMP_MES_INTERVAL_CONFIG.value # command ID coresponds to set the TX interval 
                packet_info = packetProcess.createPacket(cmd_ID,payload,payload_len) # to send the command ID
                msg.write('\nReq: TX Interval : '+", ".join("0x{:02x}".format(num) for num in packet_info))
                packet_rcvd = uartAPI.uart_write_read(packet_info,5,5) # to get the response from the device
                if(len(packet_rcvd) > 0):
                    msg.write('\nRsp: ACK: '+", ".join("0x{:02x}".format(num) for num in packet_rcvd))
                    if (packet_rcvd[2] == 0xFF): # to check for the error code in the response command
                        utility.checkresponse(packet_rcvd[3],msg)
                    else :
                        msg.write('\nGas Compensation measurement Interval changed to {} minutes'.format(byte_val))
                else:
                    msg.write('\nNO RESPONSE')
        else:
            msg.write('\nCOM Port is not available')

        logclass.logst(msg.getvalue())