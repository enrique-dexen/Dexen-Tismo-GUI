##
# @file infoReadTab.py
#
# @brief To define the option to select the information command

# Imports
from tkinter import *
import uartAPI
import commands
import packetProcess
import logclass
import utility
import globalvar
import io
from io import StringIO

##
# @class meterInfoTab
# @brief To define the drop down menu option for the information commands and create a command with the selected option
#        App version , sensor info, Run time , power type, system errors , qlong/qshort and sensor offset values can be read from the device
class meterInfoTab():

    ## To deisgn the drop down menu with the information commands option
    def __init__(self, frame):
        self.infoTabFrame = LabelFrame(frame,text = 'Info Commands',height=15,width=100) 
        self.infobutton = Button(self.infoTabFrame, text = "Send", command = self.getcommand).grid(row=3,column=6,padx=2,pady=5)
        #self._logger = logclass.debuglog()
        self.infoName = StringVar()
        self.infoName.set('Select')
        self.infoName_list = ['App Version', 'Sensor Info' , 'Run Time', 'Power Type', 'System Errors', 'Power Level','Q-Long/Short', 'Sensor Offsets']
        self.infoName_dropdown = OptionMenu(self.infoTabFrame,self.infoName,*self.infoName_list)
        self.infoName_dropdown.config (width = 14)
        self.infoName_dropdown.grid(row=3,column=5,padx=2, pady=2)
        self.infoTabFrame.grid(row=3,column=6,columnspan =2,padx=2,pady=2,sticky = W)

    ##
    #  @brief To create and send the command depends upon the option selected in the drop down menu
    #  @param self The object pointer
    def getcommand(self):
        msg = io.StringIO()
        
        if(globalvar.is_port_available == 1 and globalvar.is_com_port_connected == 1):
            payload = 0;
            payload_len = 0;
            packet_RECV = []

            if 'App Version' == self.infoName.get(): # when the app version option is selected 
                cmd_ID = commands.info_cmd.DEVICE_INFORMATION.value # to append the command ID
                packet_info = packetProcess.createPacket(cmd_ID,payload,payload_len) # to send the command
                msg.write('\nReq: Dev Ver: '+", ".join("0x{:02x}".format(num) for num in packet_info))
                packet_rcvd = uartAPI.uart_write_read(packet_info,6,5) # to get response from the device
                if(len(packet_rcvd) > 0):
                    msg.write("\nRsp: Dev Ver: "+", ".join("0x{:02x}".format(num) for num in packet_rcvd))
                    msg.write("\nVersion Info : {}.{}".format(packet_rcvd[3],packet_rcvd[4])) # first byte represents the major version and the second byte represents minor version
                else:
                    msg.write('\nNO RESPONSE')

            elif 'Sensor Info' == self.infoName.get(): # When the sensor info option is selected
                cmd_ID = commands.info_cmd.SENSOR_INFORMATION.value # to append the command ID
                packet_info = packetProcess.createPacket(cmd_ID,payload,payload_len) # to send the command
                msg.write('\nReq: Sensor Info: '+", ".join("0x{:02x}".format(num) for num in packet_info))
                packet_rcvd = uartAPI.uart_write_read(packet_info,14,5) # to ge response command
                msg.write('\nRsp: Sensor Info: '+", ".join("0x{:02x}".format(num) for num in packet_rcvd))
                if(packet_rcvd[3] == 0x05) :
                    msg.write('\nProduct ID is SGM{}{}V{}'.format(packet_rcvd[4],packet_rcvd[5],packet_rcvd[6]))
                    ser_num = ( packet_rcvd[7]<<40 | packet_rcvd[8]<<32 | packet_rcvd[9]<<24 | packet_rcvd[10]<<16 | packet_rcvd[11]<<8 | packet_rcvd[12] )
                    msg.write('\nSerial number is {}'.format(ser_num))
                else :
                    msg.write('\nSensor Serial number is not as expected')

            elif 'Run Time' == self.infoName.get(): # to read out the device run time
                cmd_ID = commands.info_cmd.DEVICE_RUNTIME_INFORMATION.value # to append the command ID
                packet_info = packetProcess.createPacket(cmd_ID,payload,payload_len)# to send the command
                msg.write('\nReq: Run time'+", ".join("0x{:02x}".format(num) for num in packet_info))
                packet_rcvd = uartAPI.uart_write_read(packet_info,8,5) # to ge response command
                #uartAPI.uart_write(packet_info)
                #packet_recv = uartAPI.uart_read(10)
                msg.write('\nRsp: Run time: '+", ".join("0x{:02x}".format(num) for num in packet_rcvd))
                # run time in payload is 4 bytes (in minutes)
                run_time = (packet_rcvd[3] << 24) | (packet_rcvd[4] << 16) | (packet_rcvd[5] << 8) | packet_rcvd[6]
                msg.write('\nRun time is {} minutes'.format(run_time))

            elif 'Power Type' == self.infoName.get(): # to read out the power source of the device
                cmd_ID = commands.info_cmd.POWER_SEL_INFORMATION.value # to append the command ID
                packet_info = packetProcess.createPacket(cmd_ID,payload,payload_len) # to send the command
                msg.write('\nReq: Power Type: '+", ".join("0x{:02x}".format(num) for num in packet_info))
                packet_rcvd = uartAPI.uart_write_read(packet_info,5,5) # to ge response command
                #uartAPI.uart_write(packet_info)
                #packet_recv = uartAPI.uart_read(10)
                msg.write('\nRsp: Power Type: '+", ".join("0x{:02x}".format(num) for num in packet_rcvd))
                if packet_rcvd[3] == 0x00 :
                    msg.write('\nDevice Powered with DC supply')
                elif packet_rcvd[3] == 0x01 :
                    msg.write('\nDevice Powered with Battery')

            elif 'System Errors' == self.infoName.get(): # to get the system error codes
                cmd_ID = commands.info_cmd.SYSTEM_ERR_INFORMATION.value # to append the command ID
                packet_info = packetProcess.createPacket(cmd_ID,payload,payload_len) # to send the command
                msg.write('\nReq: Sys Err: '+", ".join("0x{:02x}".format(num) for num in packet_info))
                packet_rcvd = uartAPI.uart_write_read(packet_info,6,5) # to ge response command
                msg.write('\nRsp: Sys Err: '+", ".join("0x{:02x}".format(num) for num in packet_rcvd))
                utility.checksystemerror( (packet_rcvd[3]<<8) | packet_rcvd[4] ,msg) # system error in payload is 2 bytes

            elif 'Power Level' == self.infoName.get(): # not implemented 
                cmd_ID = commands.info_cmd.POWER_LEVEL_INFORMATION.value # to append the command ID
                packet_info = packetProcess.createPacket(cmd_ID,payload,payload_len) # to send the command
                msg.write('\nReq: Power Lvl: '+", ".join("0x{:02x}".format(num) for num in packet_info))
                packet_rcvd = uartAPI.uart_write_read(packet_info,5,5) # to ge response command
                msg.write('\nRsp: Power Lvl: '+", ".join("0x{:02x}".format(num) for num in packet_rcvd))
                if (packet_rcvd[2] == 0xFF): # to check for the error code in the response command
                    utility.checkresponse(packet_rcvd[3],msg)

            elif 'Q-Long/Short' == self.infoName.get(): # to read out raw qlong and qshort values (directly read from the sensor)
                cmd_ID = commands.info_cmd.SENSOR_MES_DET_INFORMATION.value # to append the command ID
                packet_info = packetProcess.createPacket(cmd_ID,payload,payload_len) # to send the command
                msg.write('\nReq: Q-Long/Short: '+", ".join("0x{:02x}".format(num) for num in packet_info))
                packet_rcvd = uartAPI.uart_write_read(packet_info,8,5) # to ge response command
                msg.write('\nRsp: Q-Long/Short:  '+", ".join("0x{:02x}".format(num) for num in packet_rcvd))
                qlong_raw = (packet_rcvd[3]<<8) | packet_rcvd[4] # first two butes represents qlong value
                qshort_raw = (packet_rcvd[5]<<8) | packet_rcvd[6] # next two bytes represents qshort value
                msg.write('\nQ_Long Raw value is {}\nQ_Short Raw value is {}'.format(qlong_raw,qshort_raw))

            elif 'Sensor Offsets' == self.infoName.get():
                cmd_ID = commands.info_cmd.SENSOR_OFFSETS_INFORMATION.value # to append the command ID
                packet_info = packetProcess.createPacket(cmd_ID,payload,payload_len) # to send the command
                msg.write('\nReq: Sen Offset: '+", ".join("0x{:02x}".format(num) for num in packet_info))
                packet_rcvd = uartAPI.uart_write_read(packet_info,20,5) # to ge response command
                msg.write('\nRsp: Sen Offset:  '+", ".join("0x{:02x}".format(num) for num in packet_rcvd))
                lut_off = ((packet_rcvd[3] << 8) | packet_rcvd[4])
                scale_fac = utility.converttofloat( hex(((packet_rcvd[5] << 24) | (packet_rcvd[6] << 16) | (packet_rcvd[7] << 8) | packet_rcvd[8])) )
                vdd_off = utility.converttofloat( hex(((packet_rcvd[9] << 24) | (packet_rcvd[10] << 16) | (packet_rcvd[11] << 8) | packet_rcvd[12])) )
                k = ((packet_rcvd[13] << 8) | packet_rcvd[14])
                tcf = utility.converttofloat( hex(((packet_rcvd[15] << 24) | (packet_rcvd[16] << 16) | (packet_rcvd[17] << 8) | packet_rcvd[18])) )
                msg.write('\nLUT offset is {}\nScale factor is {}'.format(lut_off,round(scale_fac,4)))
                msg.write('\nVDD offset is {}\nGas specific parameter value (K)is {}\nThermal characteristic factor (TCF) value is {}'.format(round(vdd_off,4),k,round(tcf,4)))

            else:
                msg.write('\nINVALID INFO REQUEST COMMAND')
        else:
            msg.write('\nCOM Port is not available')
        
        logclass.logst(msg.getvalue())