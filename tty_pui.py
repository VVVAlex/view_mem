import serial

port = 'COM5'
tty = serial.Serial(port, timeout=0.8, baudrate='4800')
tty.reset_input_buffer()
while 1:
    if tty.read(2) == b"MR":
        break
tty.write(b'OK')
tty.baudrate = 115200
dat = b"\x00\x96\x28\x04\x10\x26\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
i = 0
while i < 52224:
    i += 1
    while 1:
        if tty.read(1) == b'N':
            data = tty.write(dat)
            break
while 1:
    if tty.read(1) == b'O':
        break
tty.close()
