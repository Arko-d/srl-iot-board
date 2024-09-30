from machine import SoftI2C
from time import sleep
from bme688 import BME680_I2C

bme = BME680_I2C(I2C(1, scl=Pin(7), sda=Pin(6)))

temp = bme.temperature
hum = bme.humidity
pres = bme.pressure
gas = bme.gas

print(temp, hum, pres, gas)