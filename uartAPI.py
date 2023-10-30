##
# @file uartAPI.py
#
# @brief To handles the UART operation (write,read, connection)

# Imports
import uartserial
import commands
import re
import utility
import globalvar

##
#  @brief To write data into the serial port (UART)
#  @param data - data to be send through the UART
def uart_write(data):
    interface = uartserial.uartClass()
    interface.serial_write(data)

##
#  @brief To read data from the serial port (UART)
#  @param numberofbytes - number of bytes to be read from the UART
def uart_read(numberofbytes):
    hex_n = []
    listl = []
    ind = 0
    interface = uartserial.uartClass()
    out = interface.serial_read(numberofbytes)
    out = re.findall("..",out)
    for i in out:
        a = int(i, 16)
        listl.append(a)
    return listl

##
#  @brief To send a command and waits to receive response for the command 
#  @param   data - data to be send through UART
#           num_of_bytes - number of bytes to be read from the UART
#           timeout - timeout value to wait for the response from the device
def uart_write_read(data, num_of_bytes, timeout):
    hex_n = []
    listl = []
    ind = 0
    interface = uartserial.uartClass()
    #interface.serial_write(data)
    out = interface.serial_write_read(data,num_of_bytes, timeout)
    out = re.findall("..",out)
    for i in out:
        a = int(i, 16)
        listl.append(a)
    return listl

##
#  @brief To connect to the selected port
#  @param portnumber - selected port by the user
def connectPort(portnumber):
    interface = uartserial.uartClass()
    interface.serial_setPort(portnumber)
    globalvar.is_com_port_connected = 1
##
#  @brief To disconnect from the port
def disConnectPort():
    interface = uartserial.uartClass()
    interface.serial_disconnect()
    globalvar.is_com_port_connected = 0

##
#  @brief To set the baud rate for the serial port connection
#  @param baudrate_val - selected baud rate by the user
def setBaudrate(baudrate_val):
    interface = uartserial.uartClass()
    interface.serial_setBaudrate(baudrate_val)