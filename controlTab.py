##
# @file controlTab.py
#
# @brief To define the menu option and creating the commmands for the control commmands

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
# @class meterControlTab
# @brief To define the options to reset the device , factory reset and boot mode commmand
#        Soft Reset - to just reboot the device (power on reset)
#        Factory reset - to reset the configuration in the device
#        Boot mode - tp keep the device in boot mode
class meterControlTab():
    ## to define the drop down menu option for the control commmands
    def __init__(self, frame):
        self.controlTabFrame = LabelFrame(frame,text = 'Control Commands',height=15,width=100) 
        self.controlbutton = Button(self.controlTabFrame, text = "Send", command = self.setcommand).grid(row=3,column=1,padx=2,pady=5)
        self.controlName = StringVar()
        self.controlName.set('Select')
        self.controlName_list = ['Soft Reset', 'Factory Reset' , 'Boot Mode' ,  'Zigbee Test ON', 'Zigbee Test OFF'] # to give drop down menu option of control commands
        self.controlName_dropdown = OptionMenu(self.controlTabFrame,self.controlName,*self.controlName_list)
        self.controlName_dropdown.config (width = 15)
        self.controlName_dropdown.grid(row=3,column=0,padx=2, pady=2)
        self.controlTabFrame.grid(row=3,column=2,columnspan =2,padx=2,pady=2,sticky = W)

    ##
    #  @brief to send the commands when user selects the option and presses enter
    #  @param self The object pointer
    def setcommand(self):
        msg = io.StringIO()
        if(globalvar.is_port_available == 1 and globalvar.is_com_port_connected == 1):
            payload = []
            payload_len = 0
            packet_in = []

            if 'Soft Reset' == self.controlName.get(): # to send the soft reset commmand
                cmd_ID = commands.control_cmd.SOFT_RESET.value # command ID corresponds to soft reset 
                packet_info = packetProcess.createPacket(cmd_ID,payload,payload_len) # to send the command
                msg.write('\nReq: Soft RST: '+", ".join("0x{:02x}".format(num) for num in packet_info))
                packet_rcvd = uartAPI.uart_write_read(packet_info,5,4) # to get response commands from the device
                if(len(packet_rcvd) > 0):
                    msg.write('\nRsp: ACK: '+", ".join("0x{:02x}".format(num) for num in packet_rcvd))
                    if (packet_rcvd[2] == 0xFF):  # check for the error codes in the respons command
                        utility.checkresponse(packet_rcvd[3],msg)
                    else :
                        msg.write('\nDevice is going to get reset')
                else:
                    msg.write('\nNO RESPONSE')

            elif 'Factory Reset' == self.controlName.get(): # to send the factory reset commmand
                cmd_ID = commands.control_cmd.FACTORY_RESET.value # command ID corresponds to factory reset 
                packet_info = packetProcess.createPacket(cmd_ID,payload,payload_len) # to send the command
                msg.write('\nReq: FCT RST: '+", ".join("0x{:02x}".format(num) for num in packet_info))
                packet_rcvd = uartAPI.uart_write_read(packet_info,5,4)  # to get response commands from the device
                if(len(packet_rcvd) > 0):
                    msg.write('\nRsp: ACK: '+", ".join("0x{:02x}".format(num) for num in packet_rcvd))
                    if (packet_rcvd[2] == 0xFF):  # check for the error codes in the respons command
                        utility.checkresponse(packet_rcvd[3],msg)
                    else :
                        msg.write('\nFactory Reset is going to happen')
                else:
                    msg.write('\nNO RESPONSE')

            elif 'Boot Mode' == self.controlName.get(): # to send the boot mode commmand
                cmd_ID = commands.control_cmd.BOOT_MODE.value # command ID corresponds to boot mode 
                packet_info = packetProcess.createPacket(cmd_ID,payload,payload_len) # to send the command
                msg.write('\nReq: Boot: '+", ".join("0x{:02x}".format(num) for num in packet_info))
                packet_rcvd = uartAPI.uart_write_read(packet_info,5,4)  # to get response commands from the device
                if(len(packet_rcvd) > 0):  # check for the error codes in the respons command
                    msg.write('\nRsp: ACK: '+", ".join("0x{:02x}".format(num) for num in packet_rcvd))
                    if (packet_rcvd[2] == 0xFF):  # check for the error codes in the respons command
                        utility.checkresponse(packet_rcvd[3],msg)
                    else :
                        msg.write('\nDevice is going to Boot mode')
                else:
                    msg.write('\nNO RESPONSE')
                        
            elif 'Zigbee Test ON' == self.controlName.get(): # to send the Zigbee Test ON commmand
                cmd_ID = commands.control_cmd.ZIGBEE_TEST.value # command ID corresponds to Zigbee Test ON
                payload.append(1)
                payload_len = 1
                packet_info = packetProcess.createPacket(cmd_ID,payload,payload_len) # to send the command
                msg.write('\nReq: Zigbee Test ON: '+", ".join("0x{:02x}".format(num) for num in packet_info))
                packet_rcvd = uartAPI.uart_write_read(packet_info,5,4)  # to get response commands from the device
                if(len(packet_rcvd) > 0):  # check for the error codes in the respons command
                    msg.write('\nRsp: ACK: '+", ".join("0x{:02x}".format(num) for num in packet_rcvd))
                    if (packet_rcvd[2] == 0xFF):  # check for the error codes in the respons command
                        utility.checkresponse(packet_rcvd[3],msg)
                    else :
                        msg.write('\nZigbee Test mode is ON')
                else:
                    msg.write('\nNO RESPONSE')

            elif 'Zigbee Test OFF' == self.controlName.get(): # to send the Zigbee Test OFF commmand
                cmd_ID = commands.control_cmd.ZIGBEE_TEST.value # command ID corresponds to Zigbee Test OFF
                payload.append(0)
                payload_len = 1
                packet_info = packetProcess.createPacket(cmd_ID,payload,payload_len) # to send the command
                msg.write('\nReq: Zigbee Test OFF: '+", ".join("0x{:02x}".format(num) for num in packet_info))
                packet_rcvd = uartAPI.uart_write_read(packet_info,5,4)  # to get response commands from the device
                if(len(packet_rcvd) > 0):  # check for the error codes in the respons command
                    msg.write('\nRsp: ACK: '+", ".join("0x{:02x}".format(num) for num in packet_rcvd))
                    if (packet_rcvd[2] == 0xFF):  # check for the error codes in the respons command
                        utility.checkresponse(packet_rcvd[3],msg)
                    else :
                        msg.write('\nZigbee Test mode is OFF') 
                else:
                    msg.write('\nNO RESPONSE')
            else:
                msg.write('\nINVALID REQUEST')
        else:
            msg.write('\nCOM Port is not available')

        logclass.logst(msg.getvalue())