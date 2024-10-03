from machine import Pin, I2C
from K30 import K30
# Example usage
# Replace 'I2C_ID' with the appropriate I2C bus (e.g., 'I2C(0, scl=Pin(22), sda=Pin(21))' on ESP32)
i2c = I2C(1, scl=Pin(39), sda=Pin(40), freq=100000)  # Modify pins as per your hardware setup

k30_sensor = K30(i2c)
co2_value = k30_sensor.read_co2()
if co2_value != -1:
    print("CO2 Value: ", co2_value, "ppm")
else:
    print("Failed to read CO2 value")