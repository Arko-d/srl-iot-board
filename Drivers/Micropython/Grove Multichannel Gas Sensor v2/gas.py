import machine
from time import sleep

class GAS:
    
    def __init__(self, sda, scl):
        
        self.i2c=machine.I2C(0,sda=machine.Pin(sda), scl=machine.Pin(scl), freq=400000)
        self.ADDR = 0x08
        self.GM_VERF = 3.3
        self.GM_RESOLUTION = 1023
        self.GM_102B = b'\x01'
        self.GM_302B = b'\x03'
        self.GM_502B = b'\x05'
        self.GM_702B = b'\x07'
        self.WARMING_UP = b'\xFE'
        self.WARMING_DOWN = 'b\FF'
        self.isPreheated = False
        
        self.preheated()
        self.isPreheated = True
        
    def writeByte(self, cmd):
        
        self.i2c.writeto(self.ADDR, cmd)
        sleep(0.01)
    
    def read4Bytes(self):
        
        byte_str = self.i2c.readfrom(self.ADDR, 4)
        result = 0
        for index, byte in enumerate(byte_str):
            result += byte << (8*index)
        return result
        
    def preheated(self):
        
        self.writeByte(self.WARMING_UP)
        self.isPreheated = True
        
    def unPreheated(self):
        
        self.writeByte(self.WARMING_DOWN)
        self.isPreheated = False
        
    def getGM102B(self):
        
        if not self.isPreheated:
            self.preheated()
            
        self.writeByte(self.GM_102B)
        return self.read4Bytes()
    
    def getGM302B(self):
        
        if not self.isPreheated:
            self.preheated()
            
        self.writeByte(self.GM_302B)
        return self.read4Bytes()
    
    def getGM502B(self):
        
        if not self.isPreheated:
            self.preheated()
            
        self.writeByte(self.GM_502B)
        return self.read4Bytes()
    
    def getGM702B(self):
        
        if not self.isPreheated:
            self.preheated()
            
        self.writeByte(self.GM_702B)
        return self.read4Bytes()
    
    def calVol(self, adc):
        
        return (adc*self.GM_VERF)/(self.GM_RESOLUTION*1.0)
    
    def measure_NO2(self):
        
        return self.getGM102B()
    
    def measure_C2H5OH(self):
        
        return self.getGM302B()
    
    def measure_VOC(self):
        
        return self.getGM502B()
    
    def measure_CO(self):
        
        return self.getGM702B()

