from collections.abc import Callable
import time
from pynrfjprog import LowLevel

# Constants
RTT_CONTROL_BLOCK_ADDRESS = 0x200000a4
DEVICE_NAME = "nRF52840_xxAA"  # Device name for the nRF52840
SERIAL_NO = 1050202199

def rtt():
    with LowLevel.API('NRF52') as api:
        # print(api.enum_emu_snr())
        api.connect_to_emu_without_snr()
        # api.disconnect_from_emu()
        api.connect_to_device()
        print("Connected to nRF52840.")

        
        print("Initializing RTT (automatic address discovery).")
        api.rtt_start()

        # Wait for RTT to be ready
        while not api.rtt_is_control_block_found():
            time.sleep(0.5)
        control_block = api.rtt_get_control_block_info()[1]
        print(f"RTT control block found and initialized. {control_block:x}")

        print("Reading RTT data...")
        while True:
            data = api.rtt_read(channel_index=0, length=256, encoding='latin-1')
            yield data

