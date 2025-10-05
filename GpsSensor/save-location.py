import serial
import time

ser = serial.Serial("/dev/cu.usbserial-10", 9600)
time.sleep(2)

while True:
    try:
        line = ser.readline().decode().strip()
        if "," in line:
            with open("../location.txt", "w") as f:
                f.write(line)
            print("📍", line)
    except Exception as e:
        print("❌", e)