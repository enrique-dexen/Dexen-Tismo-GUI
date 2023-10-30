##
# @file commands.py
#
# @brief To define the enum for the command s, baudrate and mode

# Imports
from enum import Enum

##
# @class info_cmd
# @brief to define the information commands
# @param enumueration (imported)
class info_cmd(Enum):
    DEVICE_INFORMATION = 1
    SENSOR_INFORMATION = 2
    SENSOR_DATA_INFORMATION = 3
    DEVICE_RUNTIME_INFORMATION = 4
    POWER_SEL_INFORMATION = 5
    SYSTEM_ERR_INFORMATION = 6
    POWER_LEVEL_INFORMATION = 7
    SENSOR_MES_DET_INFORMATION = 8
    SENSOR_OFFSETS_INFORMATION = 9
    CONFIGURATION_INFORMATION = 10
    CALIBRATION_INFORMATION = 11

##
# @class config_cmd
# @brief to define the configuration commands
# @param enumueration (imported)
class config_cmd(Enum):
    DATA_REPORTING_INTERVAL_CONFIG =17
    SENSOR_CALIBRATION_CONFIG = 18
    UART_BAUD_RATE_CONFIG = 19
    OPERATING_MODE_CONFIG = 20
    FLOW_MES_INTERVAL_CONFIG = 21
    GAS_CMP_MES_INTERVAL_CONFIG = 22


##
# @class control_cmd
# @brief to define the control commands
# @param enumueration (imported)
class control_cmd(Enum):
    SOFT_RESET = 33
    FACTORY_RESET = 34
    BOOT_MODE = 35
    FW_UPGRADE = 36
    ZIGBEE_TEST = 37

##
# @class baudrate
# @brief to define the baudrate in which the device will work
# @param enumueration (imported)
class baudrate(Enum):
    BAUD_9600 = 0
    BAUD_19200 = 1
    BAUD_38400 = 2
    BAUD_56000 = 3
    BAUD_57600 = 4

##
# @class mode
# @brief to define the device operating mode
# @param enumueration (imported)
class mode(Enum):
    MODE_NORMAL = 0
    MODE_TEST = 1
