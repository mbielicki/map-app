# "J-Link OB-nRF5340-NordicSemi"
# 1050202199

import pylink
import time

# Constants
RTT_CONTROL_BLOCK_ADDRESS = 0x200000a4
DEVICE_NAME = "nRF52840_xxAA"  # Device name for the nRF52840
SERIAL_NO = 1050202199
RTT_BUFFER_SIZE = 1024  # Size of the RTT buffer to read

def read_rtt(jlink: pylink.JLink, rtt_address):
    """
    Read RTT data from the target device.
    """
    
    jlink.rtt_start(RTT_CONTROL_BLOCK_ADDRESS)
    print(jlink.rtt_get_num_up_buffers())

def main():
    # Initialize J-Link
    jlink = pylink.JLink()
    jlink.open(SERIAL_NO)
    jlink.set_tif(pylink.enums.JLinkInterfaces.SWD)
    jlink.connect(DEVICE_NAME)

    print(jlink.connected())

    # Halt the CPU to access memory safely
    # jlink.halt()

    # Start reading RTT data
    print("Reading RTT data...")
    read_rtt(jlink, RTT_CONTROL_BLOCK_ADDRESS)

if __name__ == "__main__":
    main()