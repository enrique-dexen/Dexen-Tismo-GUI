##
# @file uartserial.py
#
# @brief To handles the serial communication

# Imports
import serial
import binascii

SER_COMPORT = 'COM4'
SER_BAUDRATE = 38400

##
# @class uartClass
# @brief To handles the serial communication -- setting the port number and baudrate, writing and reading in serial port
class uartClass():
    ## to define the serial communication
    def __init__(self):
        self.ser = serial.Serial()
    ##
    #  @brief To write into the serial port
    #  @param self The object pointer
    #         data - data to write into the serial port
    def serial_write(self,data):
        self.ser.port = SER_COMPORT
        self.ser.baudrate = SER_BAUDRATE
        self.ser.open()
        self.ser.write(data)
    ##
    #  @brief To read from the serial port
    #  @param self The object pointer
    #         number_of_bytes - number of bytes to be read from the serial port
    def serial_read(self, number_of_bytes):
        self.ser.port = SER_COMPORT
        self.ser.baudrate = SER_BAUDRATE
        self.ser.open()
        data = self.ser.read(number_of_bytes)
        hex_string = binascii.hexlify(data).decode('utf-8')
        return hex_string
    ##
    #  @brief To write a command into serial port and wait to read response from the device
    #  @param self The object pointer
    #         data - data to write into the serial port
    #         bytestoread - number of bytes to be read from the serial port
    #         timeout - timeout value to wait for the response from the UART
    def serial_write_read(self,data,bytestoread, timeout):
        self.ser.port = SER_COMPORT
        self.ser.baudrate = SER_BAUDRATE
        self.ser.timeout = timeout
        self.ser.open()
        self.ser.write(data)
        rcvdData = self.ser.read(bytestoread)
        hex_rcvdData = binascii.hexlify(rcvdData).decode('utf-8')
        self.ser.close()
        return hex_rcvdData

    ##
    #  @brief To set the port for the device connection
    #  @param self The object pointer
    #         portNum - serial COM port to be connected
    def serial_setPort(self, portNum):
        global SER_COMPORT
        SER_COMPORT = portNum

    ##
    #  @brief To get disconnected from the serial port connection
    #  @param self The object pointer
    def serial_disconnect(self):
        global SER_COMPORT
        self.ser.port = SER_COMPORT  # to select the COM port from which the connection needs to be disconnected
        self.ser.close()
        SER_COMPORT = 'None'

    ##
    #  @brief To set the baud rate for the device connection
    #  @param self The object pointer
    #         baudRateVal - serial baud rate to be connected
    def serial_setBaudrate(self, baudRateVal):
        global SER_BAUDRATE
        SER_BAUDRATE = baudRateVal



#t = uartClass()
#data1 = [int('FF', base=16)]
#t.serial_write(data1)
