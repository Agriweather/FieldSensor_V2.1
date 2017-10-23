import serial
s = serial.Serial("/dev/ttyS0", 57600)

while True:
    s.write('1')
    rawString= s.readline()

    print(rawString)

