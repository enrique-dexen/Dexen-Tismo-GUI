##
# @file utility.py
#
# @brief To handles uility functions to convert the values , checking the responses

# Imports
from ctypes import *
import commands
import struct
import binascii
import logclass
import io
from io import StringIO

##
#  @brief To convert the value into hex
#  @param val - value to be get converted into the hex format
#         nbits - number of bits in hex value
def tohex(val, nbits):
        return hex((val + (1 << nbits)) % (1 << nbits))

##
#  @brief To convert the hex value into float value
#  @param hex_val - value to be get converted into the float value
def converttofloat(hex_val):
    integer = int(hex_val, 16)                        # convert from hex to a Python int
    c_pointer = pointer(c_int(integer))           # make this into a c integer
    f_pointer = cast(c_pointer, POINTER(c_float)) # cast the int pointer to a float pointer
    return f_pointer.contents.value               # dereference the pointer, get the float

def converttodouble(hex_val): 
    value = hex(hex_val).lstrip("0x").rstrip("L")
    if (hex_val == 0):
        conv_value = 0
    else:
        #conv_value = struct.unpack('d', binascii.unhexlify(str(value)))
        conv_value = struct.unpack('!d', bytes.fromhex(value))[0]
    return conv_value

def converttosigned(unsigned_num, bit_length):
    mask = (2 ** bit_length) - 1
    if unsigned_num & (1 << (bit_length - 1)):
        return unsigned_num | ~mask
    else:
        return unsigned_num & mask

##
#  @brief To check the error code in the response received from the device
#  @param val - error code received from the device
def checkresponse(val,msg):
        if val == 0x01 :
                msg.write('\nInvalid command ID')
        elif val == 0x02 :
                msg.write('\nInvalid Payload length ')
        elif val == 0x03 :
                msg.write('\nInvalid Payload') 
        elif val == 0x04 :
                msg.write('\nInvalid checksum ')

##
#  @brief To check the system error code of the device
#  @param error_code - system error code received from the device
def checksystemerror(error_code,msg):
        if (error_code & 0x01) :
                msg.write('\nSensor Communication error')
        if (error_code & 0x02) :
                msg.write('\nSensor Vdd is out of range')
        if (error_code & 0x04) :
                msg.write('\nGas is not valid')
        if (error_code & 0x08) :
                msg.write('\nSensor temperature is out of range')
        if (error_code == 0x00) :
                msg.write('\nNo Error in the device')

##
#  @brief To check for the baud rate sets in the device
#  @param baud - baud rate value received from the device
def checkbaudrate(baud,msg):
        if baud == commands.baudrate.BAUD_9600.value :
                msg.write('\nBaud Rate is 9600')
        elif baud == commands.baudrate.BAUD_19200.value :
                msg.write('\nBaud Rate is 19200')
        elif baud == commands.baudrate.BAUD_38400.value :
                msg.write('\nBaud Rate is 38400')
        elif baud == commands.baudrate.BAUD_56000.value :
                msg.write('\nBaud Rate is 56000')
        elif baud == commands.baudrate.BAUD_57600.value :
                msg.write('\nBaud Rate is 57600')
