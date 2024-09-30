import utime
from machine import I2C, Pin
from mpu9250 import MPU9250
from ak8963 import AK8963
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
I2C_ADDR = i2c.scan()
print(I2C_ADDR)
dummy = MPU9250(i2c) # this opens the bypass to access to the AK8963
ak8963 = AK8963(i2c)
sensor = MPU9250(i2c, ak8963=ak8963)
print("MPU9250 id: " + hex(sensor.whoami))
while True:
    print(sensor.acceleration)
    print(sensor.gyro)
    print(sensor.magnetic)
    print(sensor.temperature)
    utime.sleep_ms(1000)
