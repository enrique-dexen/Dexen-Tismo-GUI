##
# @file fwupgrade.py
#
# @brief To handle the option for FW upgrade

# Imports
from tkinter import *
import uartAPI
import utility
import commands
import packetProcess
import globalvar
import time

fw_file_selected = 0

##
# @class fwupgradeTab
# @brief To define the menu option to select the FW upgrade file and create commands with that file
class fwupgradeTab():

   ## To create a option to get the FW file 
    def __init__(self, frame):
        self.fwupgradeFrame = LabelFrame(frame,text = "Meter Firmware Upgrade",height=15,width=100) 
        self.fwupgrade_B = Button(self.fwupgradeFrame, text = "Browse", command = self.SensorfwupgradeFileSelect).grid(row=4,column=3,padx=2,pady=5)
        self.fwupgrade_ST = Button(self.fwupgradeFrame, text = "Start", command = self.Sensorfwupgrade).grid(row=4,column=4,padx=2,pady=5)
        self.fwupgrade_SP = Button(self.fwupgradeFrame, text = "Stop", command = self.Sensorfwupgrade).grid(row=4,column=5,padx=2,pady=5)
        self.ConfigValueEntry = Entry(self.fwupgradeFrame, width = 28)
        self.ConfigValueEntry.configure(state = 'readonly')
        self.ConfigValueEntry.grid(row=4,column=2,padx=4,pady=5)
        self.fwupgradeFrame.grid(row=4,column=3,columnspan =2,padx=2,pady=2,sticky = W)

    ##
    #  @brief to create a command with the FW file and send that command to the device
    #  @param self The object pointer
    def Sensorfwupgrade(self):
        if(globalvar.is_port_available == 1 and globalvar.is_com_port_connected == 1):
                payload = []
                length = 0
                parse_len = 0
                cmd_start_byte = 126
                start_byte = 58

                file_hex = open(self.filename, "r")
                all_lines = file_hex.readlines()
                for line_n in all_lines:
                    length = length + 1    
                #print(all_lines)

                cmd_ID = commands.control_cmd.FW_UPGRADE.value # command ID corresponds to FW Upgrade command
                payload = (re.findall("..",((utility.tohex((int(length)),16)[2:].zfill(4)))))
                payload = [int(val,16) for val in payload]
                payload_len = 2; # payload length 
                packet_info = packetProcess.createPacket(cmd_ID,payload,payload_len) # to send the command
                print('Req: FW Upgrade: '+", ".join("0x{:02x}".format(num) for num in packet_info))
                packet_rcvd = uartAPI.uart_write_read(packet_info,5,4) # to get response commands from the device

                if(len(packet_rcvd) > 0):
                    print('Rsp: ACK: '+", ".join("0x{:02x}".format(num) for num in packet_rcvd), "\n")
                    if (packet_rcvd[2] == 0xFF):  # check for the error codes in the response command
                        utility.checkresponse(packet_rcvd[3],msg)
                    else :
                        print("FW Upgrade started\n")
                        print("Length of file is ",length)  
                        fw_upgrade_status = 0
                        while(parse_len < length):
                            packet_ack = []
                            list_lines = []
                            cmd_length = []
                            total_length = 0
                            if(parse_len+5 > length):
                                limit = length - 1
                            else:
                                limit = parse_len+5
                            list_lines.append(cmd_start_byte)
                            for line_num in range(parse_len,limit):
                                length_read = ( (int(all_lines[line_num][1],base=16)<<4) | int(all_lines[line_num][2],base=16) )
                                length_of_cmd = length_read + 6
                                total_length = total_length + length_of_cmd
                            #print("Total length is ",total_length)
                            cmd_length = (re.findall("..",((utility.tohex((int(total_length)),16)[2:].zfill(4)))))
                            cmd_length = [int(val,16) for val in cmd_length]
                            #print("CMD length is ",cmd_length[0],cmd_length[1])
                            list_lines.append(cmd_length[0])
                            list_lines.append(cmd_length[1])
                            for line_num in range(parse_len,limit):
                                #line_to_parse = all_lines[line_num]
                                length_of_line = len(all_lines[line_num])
                                line_to_parse = all_lines[line_num][1:(length_of_line-1)]
                                #print("Parsing line:",line_to_parse)
                                list_lines.append(start_byte)
                                for i in range(0,len(line_to_parse),2):       
                                    data_byte = line_to_parse[i:i+2]
                                    list_lines.append((int(data_byte,base=16)))
                            #print(list_lines)  
                            packet_ack = uartAPI.uart_write_read(list_lines,1,60)
                            if(len(packet_ack) <= 0):
                                print("Error in sending lines of",parse_len+5)
                                fw_upgrade_status = 1
                                break
                                #print("CMD length is ",cmd_length[0],cmd_length[1])
                                #print("Total length is ",total_length)
                                #print(list_lines)  
                            else:
                                print('ACK:',packet_ack[0])
                                if(packet_ack[0] == 0):
                                    print("FW file sent till ",parse_len+5,"lines") 
                                    parse_len = parse_len + 5
                                else:
                                    fw_upgrade_status = 1
                                    break
                            time.sleep(0.1)
                        if(0 == fw_upgrade_status):
                            print("FW file has been sent successfully\n")
                        else:
                            print("FW Upgrade Failed\n")
                else:
                    print('NO RESPONSE')
        else:
            print('COM Port is not available')

    ##
    #  @brief To get the FW upgrade file by using the browse option
    #  @param self The object pointer
    def SensorfwupgradeFileSelect(self):
        self.filename = []
        self.filename = filedialog.askopenfilename(initialdir = "/",title = "Select a File",filetypes = (("Text files","*.hex*"),("all files","*.*")))
        self.ConfigValueEntry.configure(state = 'normal')
        self.ConfigValueEntry.delete(0,END)
        self.ConfigValueEntry.insert(0,self.filename)
        self.ConfigValueEntry.configure(state = 'readonly')