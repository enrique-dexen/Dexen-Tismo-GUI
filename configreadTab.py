##
# @file configureTab.py
#
# @brief To define the menu option and creating the commmands for the read option

# Imports
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
class configreadTab():
    
    ## to define the drop down menu with configuration and calibration read out commands
    def __init__(self, frame):
        self.configReadFrame = LabelFrame(frame,text = 'Read Commands',height=15,width=100) 
        self.configRead_B = Button(self.configReadFrame, text = "Read", command = self.readConfig).grid(row=3,column=2,padx=2,pady=5)
        self.config_val = StringVar()
        self.config_val.set('Select')
        self.configRead_list = ['Configuration','Calibration']
        self.configRead_dropdown = OptionMenu(self.configReadFrame,self.config_val,*self.configRead_list)
        self.configRead_dropdown.config (width = 15)
        self.configRead_dropdown.grid(row=3,column=1,padx=2, pady=2)
        self.configReadFrame.grid(row=3,column=4,columnspan =2,padx=2,pady=2,sticky = W)

    ##
    #  @brief to define the command to read out device configuration
    #  @param self The object pointer
    def readConfig(self):
        msg = io.StringIO()
        if(globalvar.is_port_available == 1 and globalvar.is_com_port_connected == 1):
            payload = 0;
            payload_len = 0;
            packet_in = []
            if 'Configuration' == self.config_val.get() : # check whether configuration is selected in the read command menu
                cmd_ID = commands.info_cmd.CONFIGURATION_INFORMATION.value  # add command ID to read device configuration
                packet_info = packetProcess.createPacket(cmd_ID,payload,payload_len)  # to send the command 
                msg.write('\nReq: Config Read: '+", ".join("0x{:02x}".format(num) for num in packet_info))
                packet_rcvd = uartAPI.uart_write_read(packet_info,15,5)  # receive the response command from the device
                if(len(packet_rcvd) > 0):
                    msg.write('\nRsp: Config Data: '+", ".join("0x{:02x}".format(num) for num in packet_rcvd))
                    rep_int = (packet_rcvd[3] << 8) | packet_rcvd[4]  # first two bytes representing the data reporting interval in seconds
                    baud_rate = packet_rcvd[5] # third byte represents the baud rate 
                    dev_mode = packet_rcvd[6]  # fourth byte represents the device operating mode
                    # next 4 bytes represents flow measurement interval in ms
                    flow_meas_interval = (  packet_rcvd[7]<<24 |  packet_rcvd[8]<<16 | packet_rcvd[9]<<8 | packet_rcvd[10] )
                    # next 2 bytes represents the gas compensation measurement interval in seconds
                    gas_comp_meas_interval = (packet_rcvd[11]<<8 | packet_rcvd[12] )
                    zigbee_test_mode = packet_rcvd[13]
                    msg.write('\nData rep interval : {} seconds'.format(rep_int))
                    utility.checkbaudrate(baud_rate,msg)
                    if dev_mode == 0x00 :
                        msg.write('\nDevice is in Normal Mode')
                    elif dev_mode == 0x01 :
                        msg.write('\nDevice is in Test Mode')
                    msg.write('\nFlow measurement interval is {} ms'.format(flow_meas_interval))
                    msg.write('\nGas compensation measurement interval is {} minutes'.format(gas_comp_meas_interval))
                    if zigbee_test_mode == 0x01 :
                        msg.write('\nZigbee Test mode is ON in device')
                    elif zigbee_test_mode == 0x00 :
                        msg.write('\nZigbee Test mode is OFF in device')
                else:
                    msg.write('\nNO RESPONSE')

            elif 'Calibration' == self.config_val.get() : # check whether calibration is selected in the rrad command menu
                cmd_ID = commands.info_cmd.CALIBRATION_INFORMATION.value # add command ID to read out calibraion data from the device
                packet_info = packetProcess.createPacket(cmd_ID,payload,payload_len) # to send out the command
                msg.write('\nReq: Calib Read: '+", ".join("0x{:02x}".format(num) for num in packet_info))
                packet_rcvd = uartAPI.uart_write_read(packet_info,85,5) # to receive response command from the device
                if(len(packet_rcvd) > 0):
                    msg.write('\nRsp: Calibration Data: '+", ".join("0x{:02x}".format(num) for num in packet_rcvd))
                    len_of_chart = packet_rcvd[3]
                    msg.write('\nLength of calibraton chart is {}'.format(len_of_chart))
                    if(len_of_chart > 0):
                        itr = 0
                        limit = len_of_chart * 4
                        while(itr < limit):
                            supp_point = (packet_rcvd[itr+4] << 8) | packet_rcvd[itr+5]
                            corr_value = utility.converttosigned(((packet_rcvd[itr+6] << 8) | packet_rcvd[itr+7]),16)
                            msg.write('\n{},{}'.format(supp_point,corr_value))
                            itr = itr + 4
                    else:
                        msg.write('\nCalibration data is not available in the device')
                else:
                    msg.write('\nNO RESPONSE')

            else :
                msg.write('\nINVALID REQUEST')
        else:
            msg.write('\nCOM Port is not available')

        logclass.logst(msg.getvalue())