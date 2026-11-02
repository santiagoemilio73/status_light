import serial, time

ser = serial.Serial("/dev/ttyACM0", 115200, timeout=0.5)
time.sleep(2)

ser.write(b"MODE RAINBOW\n")
ser.flush()
time.sleep(1)
print("Pico replied:", ser.read(500))
ser.close()