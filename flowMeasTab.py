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
class flowMeasTab():
    
    ## to define the drop down menu with configuration and calibration read out commands
    def __init__(self, frame):
        self.flowMeasFrame = LabelFrame(frame,text = 'Flow Measurement time',height=15,width=50) 
        self.flowMeas_txt = Message(self.flowMeasFrame, text="ms", relief=FLAT).grid(row=4,column=2,padx=2,pady=5)
        self.flowMeas_B = Button(self.flowMeasFrame, text = "Send", command = self.setflowmeastime).grid(row=4,column=3,padx=2,pady=5)
        self.ConfigValueEntry = Entry(self.flowMeasFrame, width = 12)
        self.ConfigValueEntry.configure(state = 'normal')
        self.ConfigValueEntry.grid(row=4,column=1,padx=4,pady=5)
        self.flowMeasFrame.grid(row=4,column=3,columnspan =2,padx=2,pady=2,sticky = W)

    def setflowmeastime(self):
        msg = io.StringIO()

        if(globalvar.is_port_available == 1 and globalvar.is_com_port_connected == 1):
            payload = []
            byte_val = self.ConfigValueEntry.get() # to get the user selected interval from the menu option
            #if((int(byte_val) <= 0)):
            if((int(byte_val) < 1000) or (int(byte_val) > 3600000)):
                msg.write('\nInvalid input ')
            else:
                payload = (re.findall("..",((utility.tohex((int(byte_val)),32)[2:].zfill(8)))))
                payload = [int(val,16) for val in payload]
                payload_len = 4 # payload length 
                cmd_ID = commands.config_cmd.FLOW_MES_INTERVAL_CONFIG.value # command ID coresponds to set the TX interval 
                packet_info = packetProcess.createPacket(cmd_ID,payload,payload_len) # to send the command ID
                msg.write('\nReq: TX Interval : '+", ".join("0x{:02x}".format(num) for num in packet_info))
                packet_rcvd = uartAPI.uart_write_read(packet_info,5,5) # to get the response from the device
                if(len(packet_rcvd) > 0):
                    msg.write('\nRsp: ACK: '+", ".join("0x{:02x}".format(num) for num in packet_rcvd))
                    if (packet_rcvd[2] == 0xFF): # to check for the error code in the response command
                        utility.checkresponse(packet_rcvd[3],msg)
                    else :
                        msg.write('\nFlow measurement interval changed to {} milli seconds'.format(byte_val))
                else:
                    msg.write('\nNO RESPONSE')
        else:
            msg.write('\nCOM Port is not available')

        logclass.logst(msg.getvalue())