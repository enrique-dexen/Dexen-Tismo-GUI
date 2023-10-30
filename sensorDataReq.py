##
# @file sensorDataReq.py
#
# @brief To implement the options to get the sensor data from the device 

# Imports
from tkinter import *
import uartAPI
import commands
import packetProcess
import utility
import globalvar
import logclass
import io
from io import StringIO

##
# @class sensorDataReqTab
# @brief To define the option to create a command to get the sensor data from the device
class sensorDataReqTab():
    ## To design the tool for the sensor data requestiong option
    def __init__(self, frame):
        self.dataReqTabFrame = LabelFrame(frame,text = "Data-Req", height=15,width=100) 
        self.dataReqbutton = Button(self.dataReqTabFrame, text = "Sensor Data Req", command = self.dataReqcommand).grid(row=3,column=8,padx=2,pady=5)
        self.dataReqTabFrame.grid(row=3,column=8,columnspan =2,padx=2,pady=2,sticky = W)

    ##
    #  @brief To create a command to receive the sensor data from the device 
    #  @param self The object pointer
    def dataReqcommand(self):
        msg = io.StringIO()

        if(globalvar.is_port_available == 1 and globalvar.is_com_port_connected == 1):
            payload = 0;
            payload_len = 0;
            packet_in = []
            cmd_ID = commands.info_cmd.SENSOR_DATA_INFORMATION.value # command ID corresponds to the sensor data information
            packet_info = packetProcess.createPacket(cmd_ID,payload,payload_len) # to send the command 
            msg.write('\nReq: Data Req: '+", ".join("0x{:02x}".format(num) for num in packet_info))
            packet_rcvd = uartAPI.uart_write_read(packet_info,24,5) # to receive the response command
            if(len(packet_rcvd) > 0):
                    msg.write('\nRsp: Sensor Data: '+", ".join("0x{:02x}".format(num) for num in packet_rcvd))
                    # response command has the following data - flow (4 bytes), volume (8 bytes) , pressure (4 bytes) , temperature (4 bytes)
                    flow = utility.converttofloat( hex(((packet_rcvd[3] << 24) | (packet_rcvd[4] << 16) | (packet_rcvd[5] << 8) | packet_rcvd[6])) )
                    #volume = utility.converttodouble( hex(((packet_rcvd[7] << 56)  | (packet_rcvd[8] << 48) | (packet_rcvd[9] << 40) | (packet_rcvd[10] << 32) | (packet_rcvd[11] << 24) | (packet_rcvd[12] << 16) | (packet_rcvd[13] << 8) | packet_rcvd[14])) )
                    volume = utility.converttodouble( (((packet_rcvd[7] << 56)  | (packet_rcvd[8] << 48) | (packet_rcvd[9] << 40) | (packet_rcvd[10] << 32) | (packet_rcvd[11] << 24) | (packet_rcvd[12] << 16) | (packet_rcvd[13] << 8) | packet_rcvd[14])) )
                    pressure = utility.converttofloat( hex(((packet_rcvd[15] << 24) | (packet_rcvd[16] << 16) | (packet_rcvd[17] << 8) | packet_rcvd[18])) )
                    temperature = utility.converttofloat( hex(((packet_rcvd[19] << 24) | (packet_rcvd[20] << 16) | (packet_rcvd[21] << 8) | packet_rcvd[22])) )
                    msg.write('\nFlow value is {} std. litre/min \nVolume value is {} m^3'.format(round(flow,4),round(volume,4)))
                    msg.write('\nPressure value is {} hpa \nTemperature value is {} Degree Celcius'.format(round(pressure,4),round(temperature,4)))
            else:
                    msg.write('\nNO RESPONSE')
        else:
            msg.write('\nCOM Port is not available')
        
        logclass.logst(msg.getvalue())
