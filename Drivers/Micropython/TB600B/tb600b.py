from machine import UART
import utime
#Commands
ACTIVE_MODE = b'\xFF\x01\x78\x40\x00\x00\x00\x00\x47'
PASSIVE_MODE = b'\xFF\x01\x78\x41\x00\x00\x00\x00\x46'
READ_GAS = b'\xFF\x01\x86\x00\x00\x00\x00\x00\x79'
READ_ALL = b'\xFF\x01\x87\x00\x00\x00\x00\x00\x78'
LIGHT_OFF = b'\xFF\x01\x88\x00\x00\x00\x00\x00\x77'
LIGHT_ON = b'\xFF\x01\x89\x00\x00\x00\x00\x00\x76'

class TB600B_CO:
    def __init__(self,uart):
        self.uart = uart
        self.qna = True
    
    def send_command(self,cmd):
        self.uart.write(cmd)
        utime.sleep(1)
        return self.uart.read()
    
    def changeMode(self):
        if self.qna==True:
            self.send_command(ACTIVE_MODE)
            self.qna = False
        else:
            self.send_command(PASSIVE_MODE)
            self.qna = True
    
    def led_off(self):
        self.send_command(LIGHT_OFF)
    
    def led_on(self):
        self.send_command(LIGHT_ON)
    
    def read_gas(self):
        if self.qna==True:
            gas_array = self.send_command(READ_GAS)
        else:
            utime.sleep(1)
            gas_array = self.uart.read()
        gas_array = list(gas_array)
        return gas_array[2]*256 + gas_array[3]
    
    def read_all(self):
        if self.qna==False:
            raise(Exception("You should be in QNA mode to do this. Call changeMode()?"))
        all_array = self.send_command(READ_ALL)
        all_array = list(all_array)
        readings = {}
        readings["gas_ugm3"] = all_array[2]*256 + all_array[3]
        readings["gas_ppb"] = all_array[6]*256 + all_array[7]
        readings["temperature"] = ((all_array[8] <<8) | all_array[9])/100
        readings["humidity"] = ((all_array[10]<<8) | all_array[11])/100
        return readings
