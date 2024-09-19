from machine import I2C,Pin
import mpu6050
import bmp180
import utime

i2c = I2C(id=0, scl=Pin(1), sda=Pin(0), freq=400000)
#Performing a scan to see the peripherals
print([a for a in list(i2c.scan())])
#0x68 is the IMU sensor and 0x77 is the barometer

#initializing the IMU sensor
imu_sensor = mpu6050.MPU6050(i2c)
pressure_sensor = bmp180.BMP180(i2c)
imu_sensor.wake()

while True:
    print(imu_sensor.read_gyro_data())
    print(imu_sensor.read_accel_data())
    print("Pressure: ",(float(pressure_sensor.pressure)/10))
    print("Alitude: ",pressure_sensor.altitude)
    utime.sleep_ms(300)

