from machine import UART
import time            
"""
Driver for SEN0177
authored by Arko Datta
"""
class SEN0177:
    #initialization of the class
    def __init__(self,interface=0):
        self.interface=interface # setting the UART interface: 0 or 1
        self.uart=UART(interface, baudrate=9600, bits=8, parity=None, stop=1)#Initializing the UART interface as specified in the datasheet
        self.data={
                'start_1': False,#Start byte 1 is OK
                'start_2': False,#Start byte 1 and 2 both are OK
                'pm10': None,#PM 1.0
                'pm25': None,#PM 2.5
                'pm100': None,#PM 10.0
                'um03': None,#Support not provided
                'um05': None,#Support not provided
                'um10': None,#Support not provided
                'um25': None,#Support not provided
                'um50': None,#Support not provided
                'um100': None#Support not provided
            }
    def read(self):
        reading = self.readData()#Reads a byte from the bytestream of the sensor
        while(True):
            while (True):
                if self.data['start_1'] == False and reading == b'\x42':
                    self.data['start_1'] = True
                    break
                else:
                    continue
            reading = self.readData(1)
            if reading == b'\x4d':
                self.data['start_2'] = True
                break
            else:
                data['start_1'] = False
                data['start_2'] = False
        data = self.readData(30)
        self.data['pm10']=int.from_bytes(bytearray(data[2:4]),"big")
        self.data['pm25']=int.from_bytes(bytearray(data[4:6]),"big")
        self.data['pm100']=int.from_bytes(bytearray(data[6:8]),"big")
        self.data['start_1'] = False
        self.data['start_2'] = False
            
    
    def readData(self,byte=1):
        reading = self.uart.read(byte)
        while(reading==None):
            #print(reading)
            reading = self.uart.read(byte)
        return reading
        

while(True):
    sensor = SEN0177(0)
    sensor.read()
    print("PM 1.0 = ",sensor.data['pm10'])
    print("PM 2.5 = ",sensor.data['pm25'])
    print("PM 10.0 = ",sensor.data['pm100'])
