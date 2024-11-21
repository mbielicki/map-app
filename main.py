import serial

ser = serial.Serial(
    port='COM14',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=0
)

print("Connected to:", ser.portstr)

array_tmp = []

while True:
    byte_read = ser.read()  # Read bytes from serial port
    if byte_read:#if not empty
        byte_char = byte_read.decode()  # Decode bytes to string
        array_tmp.append(byte_char)
        if byte_char == '\n':
            print(''.join(array_tmp))  # Print the received line
            print(array_tmp)  # Print the received line
            array_tmp = []

ser.close()