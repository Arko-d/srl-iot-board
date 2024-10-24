import machine, sdcard, os, vfs
from machine import Pin, SoftSPI
spi = SoftSPI(baudrate=100000, polarity=1, phase=0, sck=Pin(15), mosi=Pin(16), miso=Pin(13))
sd = sdcard.SDCard(spi, Pin(14))
#os.mount(sd, '/sd')
#vfs.mount(sd, '/sd')
#os.listdir('/')


# Mount filesystem
vfs = os.VfsFat(sd)
os.mount(vfs, "/sd")
print(os.listdir('/sd'))


# Create a file and write something to it
with open("/sd/test01.txt", "w") as file:
    file.write("Hello, SS ARMY!\r\n")
    file.write("This is a test\r\n")

# Open the file we just created and read from it
with open("/sd/test01.txt", "r") as file:
    data = file.read()
    print(data)