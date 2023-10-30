##
# @file calibrationTab.py
#
# @brief To define the menu option to modify the baudrate in the device

# Imports
from tkinter import *
from tkinter import filedialog
import xlrd
import uartAPI
import utility
import commands
import packetProcess
import re
import globalvar
import logclass
import io
from io import StringIO

##
# @class calibrationTab
# @brief Class that contains the options to ge the calibration data and creating command for that 
#        Calibration data will be read from the ".xls" file which will be selected by the user using browse option
#        Each cell will be read from the xls file and will be converted into hex format to generate command
class calibrationTab():

    ## to define the Calibration option in the tool
    def __init__(self, frame):
        self.CalibrationFrame = LabelFrame(frame,text = "Calibration",height=15,width=100) 
        self.calibration_S = Button(self.CalibrationFrame, text = "Browse", command = self.SensorCalibrationFileSelect).grid(row=2,column=3,padx=2,pady=5)
        self.calibration_B = Button(self.CalibrationFrame, text = "Send", command = self.SensorCalibration).grid(row=2,column=4,padx=2,pady=5)
        self.ConfigValueEntry = Entry(self.CalibrationFrame, width = 24)
        self.ConfigValueEntry.configure(state = 'readonly')
        self.ConfigValueEntry.grid(row=2,column=2,padx=4,pady=5)
        self.CalibrationFrame.grid(row=2,column=3,columnspan =2,padx=2,pady=2,sticky = W)

    ##
    #  @brief to read data from the .xls file and create a command with that .. then send that command to the device
    #  @param self The object pointer
    def SensorCalibration(self):
        msg = io.StringIO()
        if(globalvar.is_port_available == 1 and globalvar.is_com_port_connected == 1):
                logclass.logst(self.filename)
                calib_data = []
                payload=[]
                wb = xlrd.open_workbook(self.filename) # to open the .xls file
                sheet = wb.sheet_by_index(0)
                sheet.cell_value(0, 0)
                for i in range(sheet.nrows): # to read data and conver into hex value
                    calib_data += (re.findall("..",((utility.tohex((int(sheet.cell_value(i, 0))),16)[2:].zfill(4)))))
                    calib_data += (re.findall("..",((utility.tohex((int(sheet.cell_value(i, 1))),16)[2:].zfill(4)))))
                calib_data = [int(val,16) for val in calib_data]
                payload_len = len(calib_data) + 1 # payload length  = calibration data length + 1 (for a bye to indicate the calibration length)
                payload.append(sheet.nrows)  # to append the number of calibration points in the payload
                payload += calib_data  # to append calibration data in the payload
                #print(payload)
                cmd_ID = commands.config_cmd.SENSOR_CALIBRATION_CONFIG.value
                packet_info = packetProcess.createPacket(cmd_ID,payload,payload_len) # to send out the command
                msg.write('\nReq: Calib Chart: '+", ".join("0x{:02x}".format(num) for num in packet_info))
                packet_rcvd = uartAPI.uart_write_read(packet_info,5,5) # to receive response command from the device
                if(len(packet_rcvd) > 0):
                        msg.write('\nRsp: ACK: '+", ".join("0x{:02x}".format(num) for num in packet_rcvd))
                        if (packet_rcvd[2] == 0xFF): # to check for the error code in the response command
                            utility.checkresponse(packet_rcvd[3],msg)
                        else :
                            msg.write('\nCalibration Data modified successfully')
                else:
                        msg.write('\nNO RESPONSE')
        else:
            msg.write('\nCOM Port is not available')

        logclass.logst(msg.getvalue())
        
    ##  
    #  @brief to define the browse option for the calibration chart
    #  @param self The object pointer
    def SensorCalibrationFileSelect(self):
        self.filename = []
        self.filename = filedialog.askopenfilename(initialdir = "/",title = "Select a File",filetypes = (("Text files","*.xls*"),("all files","*.*")))
        self.ConfigValueEntry.configure(state = 'normal')
        self.ConfigValueEntry.delete(0,END)
        self.ConfigValueEntry.insert(0,self.filename)
        self.ConfigValueEntry.configure(state = 'readonly')

    