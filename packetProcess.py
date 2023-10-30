##
# @file packetProcess.py
#
# @brief To create packet with the data to send to the device

# Imports
import enum

# Global Variables
START_BYTE = 0X7E

packet_list = []

##
#  @brief To calculate CRC by XOR all the data in the buffer
#  @param listdata - buffer contains the data
#  @param listlength - length of the data buffer
def calculateCRC(listdata, listlength):
    crc = 0
    length = len(listdata)
    for x in listdata:
        crc = crc ^ x
    return crc

##
#  @brief To create a packet with the command ID and payload
#  @param cmdID - Command ID for the commands
#  @param payload - payload of the commands
#  @param payload_length - length of the payload
def createPacket(cmdID,payload, payload_length):
    packet_list = []
    packet_list.append(START_BYTE)
    packet_list.append(0)
    packet_list.append(cmdID)
    if payload_length !=0 :
        packet_list += payload
    packet_length = len(packet_list) - 1
    packet_list[1] = packet_length
    crc = calculateCRC(packet_list,packet_length)
    packet_list.append(crc)
    return packet_list